#!/usr/bin/env python3
"""
生成预测正确的样例
持续从数据集中随机抽取样例，直到找到预测正确的样例并保存
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import mindspore as ms
from mindspore import context
from inference import load_model_auto

# 表情类别映射
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_LABELS_CN = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def predict_emotion(model, image):
    """使用模型预测表情"""
    # 预处理图像
    image_norm = image.astype('float32') / 255.0
    input_tensor = ms.Tensor(image_norm, dtype=ms.float32)
    input_tensor = input_tensor.reshape(1, 1, 48, 48)

    # 预测
    output = model(input_tensor)
    probs = ms.ops.softmax(output, axis=1).asnumpy()[0]

    pred_idx = int(np.argmax(probs))
    confidence = float(probs[pred_idx])

    return pred_idx, EMOTION_LABELS[pred_idx], confidence, probs


def create_sample_visualization(image, true_emotion_id, pred_emotion, confidence, probs,
                                output_path):
    """创建样例可视化"""
    fig = plt.figure(figsize=(14, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.5], wspace=0.3)

    # 左侧：原图
    ax1 = plt.subplot(gs[0])
    ax1.imshow(image, cmap='gray')
    ax1.axis('off')
    ax1.set_title(f'True: {EMOTION_LABELS_CN[true_emotion_id]} ({EMOTION_LABELS[true_emotion_id]})',
                 fontsize=14, fontweight='bold', color='green', pad=10)

    # 右侧：识别结果
    ax2 = plt.subplot(gs[1])
    colors = ['#FF6B6B' if i == true_emotion_id else '#4ECDC4' for i in range(7)]
    bars = ax2.barh(range(7), probs, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    ax2.set_yticks(range(7))
    ax2.set_yticklabels([f'{EMOTION_LABELS_CN[i]}\n({EMOTION_LABELS[i]})' for i in range(7)],
                        fontsize=11)
    ax2.set_xlabel('Probability', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    # 添加数值标签
    for i, (bar, prob) in enumerate(zip(bars, probs)):
        width = bar.get_width()
        label_x_pos = width + 0.02
        ax2.text(label_x_pos, bar.get_y() + bar.get_height()/2,
                f'{prob:.1%}',
                va='center', ha='left', fontsize=10, fontweight='bold')

    ax2.set_title(f'Pred: {pred_emotion} ({confidence:.1%}) [CORRECT]',
                 fontsize=14, fontweight='bold', color='green', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def find_correct_sample(df_emotion, model, emotion_id, max_attempts=1000, verbose=False):
    """
    从指定表情的数据中随机抽取，直到找到预测正确的样例

    Args:
        df_emotion: 该表情的数据子集
        model: 预测模型
        emotion_id: 表情ID
        max_attempts: 最大尝试次数
        verbose: 是否显示详细调试信息

    Returns:
        tuple: (image, pred_emotion, confidence, probs, attempts) 或 None
    """
    attempts = 0
    predictions_count = {}  # 统计预测结果分布

    while attempts < max_attempts:
        attempts += 1

        try:
            # 随机选择一个样本
            idx = np.random.randint(0, len(df_emotion))
            row = df_emotion.iloc[idx]
            pixels = np.array([int(p) for p in row['pixels'].split()], dtype=np.uint8)
            image = pixels.reshape(48, 48)

            # 预测
            pred_idx, pred_emotion, confidence, probs = predict_emotion(model, image)

            # 统计预测结果
            predictions_count[pred_emotion] = predictions_count.get(pred_emotion, 0) + 1

            # 调试信息
            if verbose and attempts <= 10:
                print(f"    Attempt {attempts}: predicted {pred_emotion} (confidence: {confidence:.1%})")

            # 检查是否预测正确
            if pred_idx == emotion_id:
                print(f"  ✓ Found correct sample after {attempts} attempts! "
                      f"(confidence: {confidence:.1%})")
                return image, pred_emotion, confidence, probs, attempts

            # 每100次尝试显示一次进度和预测分布
            if attempts % 100 == 0:
                if predictions_count:
                    top_pred = max(predictions_count.items(), key=lambda x: x[1])
                    print(f"  Attempt {attempts}... still searching... "
                          f"(most predicted: {top_pred[0]} {top_pred[1]} times)")
                else:
                    print(f"  Attempt {attempts}... still searching...")

        except Exception as e:
            if verbose:
                print(f"    Error at attempt {attempts}: {e}")
            continue

    # 失败后显示预测分布
    print(f"  ✗ Failed to find correct sample after {max_attempts} attempts")
    if predictions_count:
        print(f"  Prediction distribution: {predictions_count}")
    return None


def generate_correct_samples(csv_path, model, output_dir, num_samples_per_emotion,
                            usage='PublicTest', max_attempts=1000, verbose=False):
    """
    为每种表情生成指定数量的预测正确的样例

    Args:
        csv_path: 数据集路径
        model: 模型
        output_dir: 输出目录
        num_samples_per_emotion: 每种表情的样例数量
        usage: 数据集用途
        max_attempts: 每个样例的最大尝试次数
        verbose: 是否显示详细调试信息
    """
    print("\n" + "="*60)
    print("Generating CORRECT prediction samples only")
    print("="*60 + "\n")

    # 读取数据集
    df = pd.read_csv(csv_path)
    df_subset = df[df['Usage'] == usage]

    # 统计信息
    total_samples = 0
    total_attempts = 0
    failed_emotions = []

    for emotion_id in range(7):
        emotion_name = EMOTION_LABELS[emotion_id]
        emotion_dir = os.path.join(output_dir, emotion_name)
        os.makedirs(emotion_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Processing: {EMOTION_LABELS_CN[emotion_id]} ({emotion_name})")
        print(f"Target: {num_samples_per_emotion} correct samples")
        print(f"{'='*60}")

        # 获取该表情的所有数据
        df_emotion = df_subset[df_subset['emotion'] == emotion_id]

        if len(df_emotion) == 0:
            print(f"[WARNING] No data found for {emotion_name}")
            failed_emotions.append(emotion_name)
            continue

        print(f"Available samples in dataset: {len(df_emotion)}")

        # 生成指定数量的正确样例
        samples_found = 0

        for sample_idx in range(num_samples_per_emotion):
            print(f"\nGenerating sample {sample_idx + 1}/{num_samples_per_emotion}...")

            result = find_correct_sample(df_emotion, model, emotion_id, max_attempts, verbose)

            if result is None:
                print(f"[WARNING] Could not find correct sample {sample_idx + 1}")
                failed_emotions.append(f"{emotion_name} (sample {sample_idx + 1})")
                continue

            image, pred_emotion, confidence, probs, attempts = result
            total_attempts += attempts

            # 保存样例
            output_path = os.path.join(emotion_dir, f'correct_sample_{sample_idx + 1}.png')
            create_sample_visualization(image, emotion_id, pred_emotion, confidence,
                                       probs, output_path)

            samples_found += 1
            total_samples += 1
            print(f"  Saved: {output_path}")

        print(f"\nCompleted: {samples_found}/{num_samples_per_emotion} correct samples found")

    # 最终统计
    print("\n" + "="*60)
    print("Generation Complete!")
    print("="*60)
    print(f"\nStatistics:")
    print(f"  Total correct samples generated: {total_samples}")
    print(f"  Total attempts needed: {total_attempts}")
    print(f"  Average attempts per sample: {total_attempts/max(total_samples, 1):.1f}")

    if failed_emotions:
        print(f"\n[WARNING] Failed to generate for:")
        for item in failed_emotions:
            print(f"  - {item}")

    print(f"\nOutput directory: {output_dir}/")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Generate CORRECT prediction samples only',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 3 correct samples per emotion
  python generate_correct_samples.py \\
      --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \\
      --ckpt checkpoints/best_model.ckpt \\
      --num_samples 3

  # Use GPU for faster processing
  python generate_correct_samples.py \\
      --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \\
      --ckpt checkpoints/best_model.ckpt \\
      --device GPU \\
      --num_samples 5

  # Increase max attempts for difficult emotions
  python generate_correct_samples.py \\
      --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \\
      --ckpt checkpoints/best_model.ckpt \\
      --max_attempts 2000 \\
      --num_samples 3
        """
    )

    parser.add_argument('--csv', type=str, required=True,
                       help='FER2013 dataset CSV path')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='Model checkpoint path')
    parser.add_argument('--output', type=str, default='correct_samples',
                       help='Output directory (default: correct_samples)')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='Device (default: CPU)')
    parser.add_argument('--num_samples', type=int, default=3,
                       help='Number of correct samples per emotion (default: 3)')
    parser.add_argument('--usage', type=str, default='PublicTest',
                       choices=['Training', 'PublicTest', 'PrivateTest'],
                       help='Dataset split (default: PublicTest)')
    parser.add_argument('--max_attempts', type=int, default=1000,
                       help='Max attempts per sample (default: 1000)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show verbose debug information')

    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.csv):
        print(f"[ERROR] Dataset not found: {args.csv}")
        return 1

    if not os.path.exists(args.ckpt):
        print(f"[ERROR] Model not found: {args.ckpt}")
        return 1

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    # 设置 MindSpore 上下文
    context.set_context(mode=context.GRAPH_MODE, device_target=args.device)

    # 加载模型
    print(f"\n[INFO] Loading model: {args.ckpt}")
    model = load_model_auto(args.ckpt)
    print("[INFO] Model loaded successfully")

    # 生成正确样例
    generate_correct_samples(
        args.csv,
        model,
        args.output,
        args.num_samples,
        args.usage,
        args.max_attempts,
        args.verbose
    )

    return 0


if __name__ == '__main__':
    sys.exit(main())
