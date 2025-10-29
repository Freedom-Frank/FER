# 模型保存问题修复说明

## 问题诊断

你的直觉是对的！**模型保存逻辑确实有问题**。

### 发现的问题

在原来的 [src/train.py](src/train.py:77-100) 中，`EvalCallback` 类：

```python
class EvalCallback(Callback):
    def on_train_epoch_end(self, run_context):
        # ...
        if acc > self.best_acc:
            self.best_acc = acc
            self.best_epoch = cur_epoch
            print(f"New best accuracy: {self.best_acc:.4f} at epoch {cur_epoch}")
            # ❌ 问题：这里没有保存模型！
```

**问题**：
- 代码只是**记录**了最佳准确率和epoch
- 但**从未保存** `best_model.ckpt` 文件
- 只有 `ModelCheckpoint` 会定期保存 `fer-*_*.ckpt` 文件
- 训练结束时只保存 `final_model.ckpt`

这就解释了为什么：
1. `best_model.ckpt` 只有 434KB（可能是某次不完整的训练残留）
2. `fer-5_449.ckpt` 有 1.3MB（这是 ModelCheckpoint 自动保存的）

## 修复方案

### 已修复的代码

```python
class EvalCallback(Callback):
    """验证集评估回调函数"""
    def __init__(self, model, val_dataset, save_dir='checkpoints', eval_per_epoch=1):
        super(EvalCallback, self).__init__()
        self.model = model
        self.val_dataset = val_dataset
        self.eval_per_epoch = eval_per_epoch
        self.save_dir = save_dir  # ✓ 添加保存目录参数
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

                # ✓ 修复：立即保存最佳模型
                best_model_path = os.path.join(self.save_dir, 'best_model.ckpt')
                save_checkpoint(cb_params.train_network, best_model_path)
                print(f"Saved best model to: {best_model_path}")
```

### 修复后的行为

现在训练时会：
1. **每个epoch**评估验证集准确率
2. **如果准确率提升**，立即保存为 `best_model.ckpt`
3. **持续更新** `best_model.ckpt` 为最佳模型
4. 训练结束时，`best_model.ckpt` 就是准确率最高的模型

## 验证修复

### 训练输出示例

修复后，训练时会看到：

```
Epoch 10 - Validation Accuracy: 0.6234
New best accuracy: 0.6234 at epoch 10
Saved best model to: checkpoints_50epoch/best_model.ckpt

Epoch 15 - Validation Accuracy: 0.6523
New best accuracy: 0.6523 at epoch 15
Saved best model to: checkpoints_50epoch/best_model.ckpt

Epoch 20 - Validation Accuracy: 0.6821
New best accuracy: 0.6821 at epoch 20
Saved best model to: checkpoints_50epoch/best_model.ckpt
```

### 检查保存的模型

```bash
# 训练完成后检查
ls -lh checkpoints_50epoch/

# 应该看到：
# -rw-r--r-- 1 user user 1.3M ... best_model.ckpt      <- 最佳模型（准确率最高）
# -rw-r--r-- 1 user user 1.3M ... fer-50_449.ckpt      <- 第50轮的模型
# -rw-r--r-- 1 user user 1.3M ... final_model.ckpt     <- 最终模型（可能不是最佳）
```

**关键点**：`best_model.ckpt` 现在会是 **1.3MB**，而不是 434KB！

## 重新训练

由于修复了保存逻辑，建议重新训练：

### 快速测试修复（5轮）
```bash
python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 5 \
  --lr 5e-4 \
  --save_dir test_save_fix

# 检查是否正确保存
ls -lh test_save_fix/best_model.ckpt
python verify_model.py --ckpt test_save_fix/best_model.ckpt
```

### 完整训练（50轮）
```bash
# GPU（推荐）
bash train_50_epochs.sh

# 或 CPU
train_50_epochs.bat
```

## 为什么之前的 fer-5_449.ckpt 是可用的？

`fer-5_449.ckpt` 是由 `ModelCheckpoint` 回调自动保存的：

```python
# train.py 中的这段代码
config_ck = CheckpointConfig(save_checkpoint_steps=train_size, keep_checkpoint_max=5)
ckpoint_cb = ModelCheckpoint(prefix='fer', directory=args.save_dir, config=config_ck)
```

它**每个epoch结束时都会保存**模型，命名格式为：
- `fer-{epoch}_{step}.ckpt`
- 例如：`fer-5_449.ckpt` = 第5轮，第449步

这些模型是完整的，但可能不是准确率最高的那个。

## 总结

### 问题根源
- ❌ `best_model.ckpt` 从未被正确保存
- ❌ 只有 epoch 检查点被保存（`fer-*_*.ckpt`）
- ❌ 旧的 `best_model.ckpt` (434KB) 是某次失败训练的残留

### 修复方案
- ✓ 修改 `EvalCallback` 在准确率提升时自动保存 `best_model.ckpt`
- ✓ 每次准确率创新高就更新 `best_model.ckpt`
- ✓ 训练结束后 `best_model.ckpt` 保证是最佳模型

### 下一步
1. 删除旧的 `best_model.ckpt`（避免混淆）
2. 使用修复后的代码重新训练
3. 验证新的 `best_model.ckpt` 大小约 1.3MB
4. 使用新模型进行可视化

## 快速命令

```bash
# 1. 清理旧模型（可选）
rm checkpoints/best_model.ckpt

# 2. 重新训练（GPU推荐）
bash train_50_epochs.sh

# 3. 验证新模型
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt

# 4. 使用新模型可视化
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3
```

现在模型保存逻辑已经修复，重新训练后应该能得到正确的 `best_model.ckpt`！
