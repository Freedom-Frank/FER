#!/usr/bin/env python3
"""
诊断 generate_correct_samples.py 的问题
检查模型准确率和数据集
"""

import os
import sys
import numpy as np
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, os.path.join(project_root, 'src'))

import mindspore as ms
from mindspore import context
from inference import load_model_auto

EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def test_model_predictions(csv_path, ckpt_path, num_test=100):
    """测试模型在每种表情上的准确率"""

    print("\n" + "="*60)
    print("诊断模型预测性能")
    print("="*60 + "\n")

    # 设置上下文
    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')

    # 加载模型
    print(f"加载模型: {ckpt_path}")
    try:
        model = load_model_auto(ckpt_path)
        print("✓ 模型加载成功\n")
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return

    # 读取数据集
    print(f"读取数据集: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
        df_test = df[df['Usage'] == 'PublicTest']
        print(f"✓ 数据集加载成功 (PublicTest: {len(df_test)} 样本)\n")
    except Exception as e:
        print(f"✗ 数据集加载失败: {e}")
        return

    # 测试每种表情
    print("="*60)
    print("测试每种表情的准确率")
    print("="*60 + "\n")

    for emotion_id in range(7):
        emotion_name = EMOTION_LABELS[emotion_id]
        df_emotion = df_test[df_test['emotion'] == emotion_id]

        if len(df_emotion) == 0:
            print(f"{emotion_name:10s} - 无数据")
            continue

        # 随机选择测试样本
        test_count = min(num_test, len(df_emotion))
        test_indices = np.random.choice(len(df_emotion), test_count, replace=False)

        correct = 0
        total = test_count

        for idx in test_indices:
            row = df_emotion.iloc[idx]
            pixels = np.array([int(p) for p in row['pixels'].split()], dtype=np.uint8)
            image = pixels.reshape(48, 48)

            # 预测
            image_norm = image.astype('float32') / 255.0
            input_tensor = ms.Tensor(image_norm, dtype=ms.float32)
            input_tensor = input_tensor.reshape(1, 1, 48, 48)

            output = model(input_tensor)
            probs = ms.ops.softmax(output, axis=1).asnumpy()[0]
            pred_idx = int(np.argmax(probs))

            if pred_idx == emotion_id:
                correct += 1

        accuracy = correct / total * 100
        expected_attempts = 1 / (correct / total) if correct > 0 else float('inf')

        print(f"{emotion_name:10s} - 准确率: {accuracy:5.1f}% ({correct:3d}/{total:3d}) - "
              f"预期尝试: {expected_attempts:6.1f} 次")

    print("\n" + "="*60)
    print("诊断完成")
    print("="*60)
    print("\n建议:")
    print("1. 如果准确率 < 10%，模型可能有问题")
    print("2. 如果准确率在 10-50%，增加 --max_attempts 到 2000-5000")
    print("3. 如果准确率 > 50%，默认设置应该可以工作")
    print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='诊断模型性能')
    parser.add_argument('--csv', type=str,
                       default='/mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv',
                       help='数据集路径')
    parser.add_argument('--ckpt', type=str,
                       default='checkpoints/best_model.ckpt',
                       help='模型路径')
    parser.add_argument('--num_test', type=int, default=100,
                       help='每种表情测试样本数')

    args = parser.parse_args()

    test_model_predictions(args.csv, args.ckpt, args.num_test)
