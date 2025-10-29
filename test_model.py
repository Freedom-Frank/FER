#!/usr/bin/env python3
"""
模型测试脚本
用于快速验证模型是否可以正常加载和推理
"""

import sys
import os

# 添加 src 目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

def test_model(ckpt_path, device='CPU'):
    """测试模型加载和推理"""
    print(f"{'='*70}")
    print("模型测试工具")
    print(f"{'='*70}\n")

    # 检查文件是否存在
    if not os.path.exists(ckpt_path):
        print(f"❌ 模型文件不存在: {ckpt_path}")
        return False

    # 显示文件信息
    file_size = os.path.getsize(ckpt_path) / (1024 * 1024)  # MB
    print(f"✓ 模型文件: {ckpt_path}")
    print(f"  大小: {file_size:.1f} MB")
    print()

    # 测试加载模型
    print("正在加载模型...")
    try:
        import mindspore as ms
        from mindspore import context
        from mindspore.train.serialization import load_checkpoint, load_param_into_net
        from model import SimpleCNN

        # 设置设备
        context.set_context(mode=context.GRAPH_MODE, device_target=device)

        # 加载检查点
        param_dict = load_checkpoint(ckpt_path)

        # 检查模型版本
        classifier_key = 'classifier.0.weight'
        if classifier_key in param_dict:
            classifier_shape = param_dict[classifier_key].shape
            print(f"  分类器形状: {classifier_shape}")

            # 判断模型版本
            if classifier_shape == (128, 128):
                print(f"  模型版本: 旧版 (128 -> 128 -> 7)")
                try:
                    from model_legacy import SimpleCNN_Legacy
                    net = SimpleCNN_Legacy(7)
                except ImportError:
                    print("  ⚠ 旧版模型但 model_legacy.py 不存在")
                    net = SimpleCNN(7)
            elif classifier_shape == (256, 512):
                print(f"  模型版本: 新版 (512 -> 256 -> 128 -> 7)")
                net = SimpleCNN(7)
            else:
                print(f"  ⚠ 未知分类器形状: {classifier_shape}")
                net = SimpleCNN(7)
        else:
            print("  ⚠ 无法确定模型版本")
            net = SimpleCNN(7)

        # 加载参数
        load_param_into_net(net, param_dict)
        net.set_train(False)

        print("✓ 模型加载成功！")
        print()

    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False

    # 测试推理
    print("正在测试推理...")
    try:
        import numpy as np

        # 创建测试输入 (48x48 灰度图)
        test_input = np.random.randn(1, 1, 48, 48).astype('float32')
        test_tensor = ms.Tensor(test_input)

        # 推理
        output = net(test_tensor)
        probs = ms.ops.softmax(output)[0].asnumpy()

        # 显示结果
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        print("✓ 推理成功！")
        print()
        print("测试输出（随机输入）：")
        for emotion, prob in zip(emotions, probs):
            bar = '█' * int(prob * 50)
            print(f"  {emotion:10s}: {bar} {prob:.2%}")
        print()

    except Exception as e:
        print(f"❌ 推理失败: {e}")
        return False

    print(f"{'='*70}")
    print("✓ 所有测试通过！模型可以正常使用。")
    print(f"{'='*70}\n")

    return True

def find_best_model():
    """查找最佳模型"""
    model_paths = [
        'checkpoints_50epoch/best_model.ckpt',
        'checkpoints/best_model.ckpt',
        'checkpoints_50epoch/fer-50_299.ckpt',
        'checkpoints/fer-5_449.ckpt',
    ]

    for path in model_paths:
        if os.path.exists(path):
            return path

    return None

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='测试模型加载和推理')
    parser.add_argument('--ckpt', type=str,
                       help='模型检查点路径（不指定则自动查找）')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='计算设备')

    args = parser.parse_args()

    # 确定模型路径
    if args.ckpt:
        ckpt_path = args.ckpt
    else:
        print("正在自动查找模型...\n")
        ckpt_path = find_best_model()
        if not ckpt_path:
            print("❌ 未找到任何模型文件！")
            print("\n请指定模型路径或确保以下文件存在：")
            print("  - checkpoints_50epoch/best_model.ckpt")
            print("  - checkpoints/best_model.ckpt")
            sys.exit(1)
        print(f"✓ 自动选择: {ckpt_path}\n")

    # 测试模型
    success = test_model(ckpt_path, args.device)

    if success:
        print("使用方法：")
        print(f"  python tools/demo_visualization.py --mode webcam --ckpt {ckpt_path}")

    sys.exit(0 if success else 1)
