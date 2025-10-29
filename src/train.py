# train.py
import argparse
import os
import numpy as np

from mindspore.train import Model
from mindspore.train.callback import LossMonitor, ModelCheckpoint, CheckpointConfig, TimeMonitor, Callback
from mindspore.train.serialization import save_checkpoint
from mindspore import nn
from mindspore import context
from mindspore.dataset import GeneratorDataset
from mindspore import ops, Tensor
import mindspore.numpy as mnp

from dataset import FER2013Dataset
from model import SimpleCNN


class LabelSmoothingCrossEntropy(nn.Cell):
    """Label Smoothing损失函数（不使用Mixup时）"""
    def __init__(self, num_classes=7, smoothing=0.1):
        super(LabelSmoothingCrossEntropy, self).__init__()
        self.smoothing = smoothing
        self.num_classes = num_classes
        self.confidence = 1.0 - smoothing
        self.log_softmax = nn.LogSoftmax(axis=1)
        self.nll_loss = nn.NLLLoss(reduction='mean')

    def construct(self, logits, labels):
        # 计算log softmax
        log_probs = self.log_softmax(logits)

        # 标准NLL损失
        nll = self.nll_loss(log_probs, labels)

        # 平滑损失：所有类别的平均log概率
        smooth_loss = -log_probs.mean()

        # 组合损失
        loss = self.confidence * nll + self.smoothing * smooth_loss
        return loss


class SoftTargetCrossEntropy(nn.Cell):
    """支持软标签的交叉熵损失（用于Mixup）"""
    def __init__(self):
        super(SoftTargetCrossEntropy, self).__init__()
        self.log_softmax = nn.LogSoftmax(axis=1)

    def construct(self, logits, labels):
        """
        logits: (batch_size, num_classes)
        labels: (batch_size, num_classes) 软标签（one-hot或mixup）
        """
        log_probs = self.log_softmax(logits)
        # 交叉熵：-sum(labels * log_probs)
        loss = -ops.reduce_mean(ops.reduce_sum(labels * log_probs, 1))
        return loss


class MixupLoss(nn.Cell):
    """支持Mixup的损失函数"""
    def __init__(self, base_loss):
        super(MixupLoss, self).__init__()
        self.base_loss = base_loss

    def construct(self, logits, labels_a, labels_b, lam):
        # 对两个标签分别计算损失
        loss_a = self.base_loss(logits, labels_a)
        loss_b = self.base_loss(logits, labels_b)

        # 按lambda加权混合
        lam_mean = ops.mean(lam)
        return lam_mean * loss_a + (1 - lam_mean) * loss_b


class EvalCallback(Callback):
    """验证集评估回调函数"""
    def __init__(self, model, val_dataset, save_dir='checkpoints', eval_per_epoch=1):
        super(EvalCallback, self).__init__()
        self.model = model
        self.val_dataset = val_dataset
        self.eval_per_epoch = eval_per_epoch
        self.save_dir = save_dir
        self.best_acc = 0.0
        self.best_epoch = 0

    def on_train_epoch_end(self, run_context):
        cb_params = run_context.original_args()
        cur_epoch = cb_params.cur_epoch_num

        if cur_epoch % self.eval_per_epoch == 0:
            result = self.model.eval(self.val_dataset, dataset_sink_mode=False)
            acc = result['accuracy']
            print(f"\nEpoch {cur_epoch} - Validation Accuracy: {acc:.4f}")

            if acc > self.best_acc:
                self.best_acc = acc
                self.best_epoch = cur_epoch
                print(f"New best accuracy: {self.best_acc:.4f} at epoch {cur_epoch}")

                # 保存最佳模型
                best_model_path = os.path.join(self.save_dir, 'best_model.ckpt')
                save_checkpoint(cb_params.train_network, best_model_path)
                print(f"Saved best model to: {best_model_path}")


class EarlyStoppingCallback(Callback):
    """早停回调函数"""
    def __init__(self, model, val_dataset, patience=10, min_delta=0.001):
        super(EarlyStoppingCallback, self).__init__()
        self.model = model
        self.val_dataset = val_dataset
        self.patience = patience
        self.min_delta = min_delta
        self.best_acc = 0.0
        self.counter = 0

    def on_train_epoch_end(self, run_context):
        result = self.model.eval(self.val_dataset, dataset_sink_mode=False)
        acc = result['accuracy']

        if acc > self.best_acc + self.min_delta:
            self.best_acc = acc
            self.counter = 0
        else:
            self.counter += 1
            print(f"EarlyStopping counter: {self.counter}/{self.patience}")

            if self.counter >= self.patience:
                print(f"\nEarly stopping triggered! Best accuracy: {self.best_acc:.4f}")
                run_context.request_stop()






def mixup_batch(images, labels, alpha=0.2):
    """Mixup数据增强"""
    batch_size = images.shape[0]
    lam = np.random.beta(alpha, alpha, batch_size).astype(np.float32)

    # 随机打乱索引
    index = np.random.permutation(batch_size)

    # 混合图像
    lam_expanded = lam.reshape(-1, 1, 1, 1)
    mixed_images = lam_expanded * images + (1 - lam_expanded) * images[index]

    # 混合标签（one-hot）
    labels_a = labels
    labels_b = labels[index]

    return mixed_images, labels_a, labels_b, lam


def create_dataset(csv_path, usage, batch_size, shuffle=True, augment=False, mixup=False, mixup_alpha=0.2, use_soft_labels=False):
    """创建数据集，支持数据增强和Mixup

    Args:
        use_soft_labels: 如果为True，验证集也返回one-hot标签（用于兼容SoftTargetCrossEntropy）
    """
    # 如果使用Mixup训练，验证集也需要返回软标签以兼容loss函数
    if use_soft_labels and not mixup and usage != 'Training':
        # 验证集：不使用mixup，但返回one-hot标签
        ds_generator = FER2013Dataset(csv_path, usage=usage, augment=False,
                                      mixup=False, mixup_alpha=0.0)

        def to_onehot(image, label):
            """将硬标签转换为one-hot软标签"""
            onehot = np.zeros(7, dtype=np.float32)
            onehot[label] = 1.0
            return image, onehot

        ds = GeneratorDataset(ds_generator, column_names=['image', 'label'], shuffle=shuffle)
        ds = ds.map(operations=to_onehot, input_columns=['image', 'label'],
                   output_columns=['image', 'label'])
    else:
        # 正常模式（训练集使用mixup或不使用）
        ds_generator = FER2013Dataset(csv_path, usage=usage, augment=augment,
                                      mixup=mixup, mixup_alpha=mixup_alpha)
        ds = GeneratorDataset(ds_generator, column_names=['image', 'label'], shuffle=shuffle)

    ds = ds.batch(batch_size, drop_remainder=True)
    return ds


def parse_args():
    parser = argparse.ArgumentParser(description='Train FER2013 emotion recognition model')
    parser.add_argument('--data_csv', type=str, required=True, help='Path to fer2013.csv')
    parser.add_argument('--device_target', type=str, default='CPU', choices=['CPU', 'GPU', 'Ascend'])
    parser.add_argument('--batch_size', type=int, default=96, help='Batch size')
    parser.add_argument('--epochs', type=int, default=200, help='Number of training epochs')
    parser.add_argument('--save_dir', type=str, default='checkpoints', help='Directory to save checkpoints')
    parser.add_argument('--lr', type=float, default=7e-4, help='Initial learning rate')
    parser.add_argument('--patience', type=int, default=30, help='Early stopping patience')
    parser.add_argument('--augment', action='store_true', help='Enable data augmentation')
    parser.add_argument('--weight_decay', type=float, default=3e-5, help='Weight decay')
    parser.add_argument('--label_smoothing', type=float, default=0.12, help='Label smoothing factor')
    parser.add_argument('--mixup', action='store_true', help='Enable Mixup augmentation')
    parser.add_argument('--mixup_alpha', type=float, default=0.4, help='Mixup alpha (default=0.4)')
    return parser.parse_args()




def main():
    args = parse_args()

    # 设置运行环境
    context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)

    print("=" * 60)
    print("Training Configuration:")
    print(f"  Device: {args.device_target}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Epochs: {args.epochs}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Data augmentation: {args.augment}")
    print(f"  Early stopping patience: {args.patience}")
    print("=" * 60)

    # 创建保存目录
    os.makedirs(args.save_dir, exist_ok=True)

    # 创建数据集
    print("\nLoading datasets...")
    train_ds = create_dataset(args.data_csv, usage='Training', batch_size=args.batch_size,
                             shuffle=True, augment=args.augment,
                             mixup=args.mixup, mixup_alpha=args.mixup_alpha)
    # 如果训练使用Mixup（软标签），验证集也需要返回one-hot标签以兼容loss函数
    val_ds = create_dataset(args.data_csv, usage='PublicTest', batch_size=args.batch_size,
                           shuffle=False, augment=False, mixup=False, use_soft_labels=args.mixup)

    train_size = train_ds.get_dataset_size()
    val_size = val_ds.get_dataset_size()
    print(f"Training batches: {train_size}")
    print(f"Validation batches: {val_size}")

    # 创建模型
    print("\nBuilding model...")
    net = SimpleCNN(num_classes=7)

    # 定义损失函数：Mixup模式使用软标签交叉熵
    if args.mixup:
        loss = SoftTargetCrossEntropy()
        print(f"Using Soft Target Cross Entropy for Mixup (alpha={args.mixup_alpha})")
    else:
        loss = LabelSmoothingCrossEntropy(num_classes=7, smoothing=args.label_smoothing)
        print(f"Using Label Smoothing Cross Entropy (smoothing={args.label_smoothing})")

    # 使用warmup + cosine decay学习率调度
    warmup_epochs = 5
    total_steps = train_size * args.epochs

    # 只在训练轮数大于warmup_epochs时使用warmup
    if args.epochs > warmup_epochs:
        warmup_steps = train_size * warmup_epochs
        # Warmup阶段：线性增加学习率
        warmup_lr = [args.lr * (i + 1) / warmup_steps for i in range(warmup_steps)]

        # Cosine decay阶段
        decay_steps = total_steps - warmup_steps
        cosine_lr = nn.cosine_decay_lr(min_lr=1e-6, max_lr=args.lr,
                                       total_step=decay_steps,
                                       step_per_epoch=train_size,
                                       decay_epoch=args.epochs - warmup_epochs)

        # 组合学习率
        lr_schedule = warmup_lr + cosine_lr
    else:
        # 训练轮数较少，直接使用cosine decay
        lr_schedule = nn.cosine_decay_lr(min_lr=1e-6, max_lr=args.lr,
                                         total_step=total_steps,
                                         step_per_epoch=train_size,
                                         decay_epoch=args.epochs)

    # 使用AdamW优化器（带权重衰减）
    opt = nn.AdamWeightDecay(params=net.trainable_params(),
                             learning_rate=lr_schedule,
                             weight_decay=args.weight_decay)

    # 创建模型
    model = Model(net, loss_fn=loss, optimizer=opt, metrics={'accuracy'})

    # 配置回调函数
    callbacks = [
        LossMonitor(per_print_times=train_size),  # 每个epoch打印一次loss
        TimeMonitor(),
    ]

    # Checkpoint回调
    config_ck = CheckpointConfig(save_checkpoint_steps=train_size, keep_checkpoint_max=5)
    ckpoint_cb = ModelCheckpoint(prefix='fer', directory=args.save_dir, config=config_ck)
    callbacks.append(ckpoint_cb)

    # 验证集评估回调（会自动保存最佳模型）
    eval_cb = EvalCallback(model, val_ds, save_dir=args.save_dir, eval_per_epoch=1)
    callbacks.append(eval_cb)

    # 早停回调
    early_stop_cb = EarlyStoppingCallback(model, val_ds, patience=args.patience)
    callbacks.append(early_stop_cb)

    # 开始训练
    print("\nStarting training...")
    print("=" * 60)

    model.train(epoch=args.epochs, train_dataset=train_ds, callbacks=callbacks,
                dataset_sink_mode=False)

    # 保存最终模型
    final_path = os.path.join(args.save_dir, 'final_model.ckpt')
    save_checkpoint(net, final_path)

    print("\n" + "=" * 60)
    print("Training finished!")
    print(f"Best validation accuracy: {eval_cb.best_acc:.4f} at epoch {eval_cb.best_epoch}")
    print(f"Final checkpoint saved to: {final_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()