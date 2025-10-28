#!/usr/bin/env python3
"""
生成简单的样例图片和识别结果展示
格式：（原图）-（识别结果）
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Arial']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import mindspore as ms
from mindspore import context
from inference import load_model_auto

# 表情类别映射
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_LABELS_CN = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def load_sample_images(csv_path, num_samples_per_emotion=2, usage='PublicTest'):
    """从数据集中加载每种表情的样例图片"""
    print(f"[INFO] Loading samples from {csv_path}...")

    df = pd.read_csv(csv_path)
    df_subset = df[df['Usage'] == usage]

    samples = {}
    for emotion_id in range(7):
        emotion_data = df_subset[df_subset['emotion'] == emotion_id]

        # 随机选择样例
        sample_indices = np.random.choice(len(emotion_data),
                                         min(num_samples_per_emotion, len(emotion_data)),
                                         replace=False)

        samples[emotion_id] = []
        for idx in sample_indices:
            row = emotion_data.iloc[idx]
            pixels = np.array([int(p) for p in row['pixels'].split()], dtype=np.uint8)
            image = pixels.reshape(48, 48)
            samples[emotion_id].append((image, emotion_id))

        print(f"  {EMOTION_LABELS[emotion_id]}: {len(samples[emotion_id])} samples")

    return samples


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

    return EMOTION_LABELS[pred_idx], confidence, probs


def create_sample_visualization(image, true_emotion, pred_emotion, confidence, probs,
                                output_path, emotion_id):
    """创建单个样例的可视化：（原图）-（识别结果）"""
    fig = plt.figure(figsize=(14, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.5], wspace=0.3)

    # 左侧：原图
    ax1 = plt.subplot(gs[0])
    ax1.imshow(image, cmap='gray')
    ax1.axis('off')

    is_correct = (true_emotion == pred_emotion)
    title_color = 'green' if is_correct else 'red'
    ax1.set_title(f'True: {EMOTION_LABELS_CN[emotion_id]} ({true_emotion})',
                 fontsize=14, fontweight='bold', color=title_color, pad=10)

    # 右侧：识别结果（概率分布柱状图）
    ax2 = plt.subplot(gs[1])

    colors = ['#FF6B6B' if i == emotion_id else '#4ECDC4' for i in range(7)]
    if not is_correct:
        pred_idx = EMOTION_LABELS.index(pred_emotion)
        colors[pred_idx] = '#FFA500'

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

    result_symbol = 'OK' if is_correct else 'X'
    ax2.set_title(f'Pred: {pred_emotion} ({confidence:.1%}) [{result_symbol}]',
                 fontsize=14, fontweight='bold', color=title_color, pad=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"  Saved: {output_path}")


def create_grid_visualization(samples_info, output_path, grid_cols=4):
    """创建网格展示"""
    n_samples = len(samples_info)
    grid_rows = (n_samples + grid_cols - 1) // grid_cols

    fig = plt.figure(figsize=(5*grid_cols, 4*grid_rows))

    for idx, (image, true_emotion, pred_emotion, confidence, emotion_id) in enumerate(samples_info):
        ax = plt.subplot(grid_rows, grid_cols, idx + 1)
        ax.imshow(image, cmap='gray')
        ax.axis('off')

        is_correct = (true_emotion == pred_emotion)
        result_symbol = 'OK' if is_correct else 'X'
        title_color = 'green' if is_correct else 'red'

        title = f'{EMOTION_LABELS_CN[emotion_id]} -> {pred_emotion}\n{confidence:.1%} [{result_symbol}]'
        ax.set_title(title, fontsize=12, fontweight='bold', color=title_color)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\n[INFO] Grid visualization saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate FER2013 sample visualizations')
    parser.add_argument('--csv', type=str, required=True,
                       help='FER2013 dataset CSV path')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='Model checkpoint path')
    parser.add_argument('--output', type=str, default='samples_output',
                       help='Output directory')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='Device')
    parser.add_argument('--num_samples', type=int, default=2,
                       help='Number of samples per emotion')
    parser.add_argument('--usage', type=str, default='PublicTest',
                       choices=['Training', 'PublicTest', 'PrivateTest'],
                       help='Dataset split')

    args = parser.parse_args()

    print("\n" + "="*60)
    print("FER2013 Sample Generator")
    print("="*60)

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    print(f"[INFO] Output directory: {args.output}")

    # 检查文件
    if not os.path.exists(args.csv):
        print(f"[ERROR] Dataset file not found: {args.csv}")
        return

    if not os.path.exists(args.ckpt):
        print(f"[ERROR] Model file not found: {args.ckpt}")
        return

    # 设置 MindSpore 上下文
    context.set_context(mode=context.GRAPH_MODE, device_target=args.device)

    # 加载样例图片
    samples_dict = load_sample_images(args.csv, args.num_samples, args.usage)

    # 加载模型
    print(f"\n[INFO] Loading model: {args.ckpt}")
    model = load_model_auto(args.ckpt)

    # 生成样例展示
    print("\n[INFO] Generating sample visualizations...")
    all_samples_info = []

    for emotion_id in range(7):
        emotion_dir = os.path.join(args.output, EMOTION_LABELS[emotion_id])
        os.makedirs(emotion_dir, exist_ok=True)

        print(f"\nProcessing: {EMOTION_LABELS_CN[emotion_id]} ({EMOTION_LABELS[emotion_id]})")

        for idx, (image, true_id) in enumerate(samples_dict[emotion_id]):
            # 预测
            pred_emotion, confidence, probs = predict_emotion(model, image)

            # 生成单个样例展示
            output_path = os.path.join(emotion_dir, f'sample_{idx+1}.png')
            create_sample_visualization(image, EMOTION_LABELS[true_id],
                                       pred_emotion, confidence, probs,
                                       output_path, emotion_id)

            all_samples_info.append((image, EMOTION_LABELS[true_id], pred_emotion,
                                    confidence, emotion_id))

    # 生成网格展示
    print("\n[INFO] Generating grid visualization...")
    grid_path = os.path.join(args.output, 'all_samples_grid.png')
    create_grid_visualization(all_samples_info, grid_path, grid_cols=4)

    # 统计信息
    print("\n" + "="*60)
    print("Generation Complete!")
    print("="*60)

    correct = sum(1 for _, true, pred, _, _ in all_samples_info if true == pred)
    total = len(all_samples_info)
    accuracy = correct / total * 100

    print(f"\nStatistics:")
    print(f"  Total samples: {total}")
    print(f"  Correct predictions: {correct}")
    print(f"  Accuracy: {accuracy:.1f}%")

    print(f"\nOutput files:")
    print(f"  Detailed samples: {args.output}/<emotion>/sample_*.png")
    print(f"  Grid visualization: {grid_path}")
    print()


if __name__ == '__main__':
    main()
