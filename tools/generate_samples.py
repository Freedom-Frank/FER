#!/usr/bin/env python3
"""
生成样例图片和识别结果展示
格式：（原图）-（识别结果）
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image, ImageDraw, ImageFont

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from visualize import FERVisualizer

# 表情类别映射
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_LABELS_CN = ['生气', '厌恶', '恐惧', '开心', '悲伤', '惊讶', '中性']


def load_sample_images(csv_path, num_samples_per_emotion=3, usage='PublicTest'):
    """
    从数据集中加载每种表情的样例图片

    Args:
        csv_path: FER2013 数据集路径
        num_samples_per_emotion: 每种表情的样例数量
        usage: 数据集用途 (Training/PublicTest/PrivateTest)

    Returns:
        dict: {emotion_id: [(image, emotion_id), ...]}
    """
    print(f"[INFO] 正在从 {csv_path} 加载样例图片...")

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

        print(f"  {EMOTION_LABELS[emotion_id]}: 加载了 {len(samples[emotion_id])} 个样例")

    return samples


def predict_emotion(visualizer, image):
    """
    使用模型预测表情

    Args:
        visualizer: FERVisualizer 实例
        image: 48x48 灰度图像

    Returns:
        tuple: (predicted_label, confidence, probabilities)
    """
    import mindspore as ms

    # 预处理图像：归一化到 [0, 1]
    image_norm = image.astype('float32') / 255.0

    # 转换为 MindSpore 张量格式 (batch, channel, height, width)
    input_tensor = ms.Tensor(image_norm, dtype=ms.float32)
    input_tensor = input_tensor.reshape(1, 1, 48, 48)

    # 预测
    output = visualizer.model(input_tensor)
    probs = ms.ops.softmax(output, axis=1).asnumpy()[0]

    pred_idx = int(np.argmax(probs))
    confidence = float(probs[pred_idx])

    return EMOTION_LABELS[pred_idx], confidence, probs


def create_sample_visualization(image, true_emotion, pred_emotion, confidence, probs,
                                output_path, emotion_id):
    """
    创建单个样例的可视化图片：（原图）-（识别结果）

    Args:
        image: 48x48 灰度图像
        true_emotion: 真实表情标签
        pred_emotion: 预测表情标签
        confidence: 置信度
        probs: 概率分布
        output_path: 输出路径
        emotion_id: 表情ID
    """
    fig = plt.figure(figsize=(14, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.5], wspace=0.3)

    # 左侧：原图
    ax1 = plt.subplot(gs[0])
    ax1.imshow(image, cmap='gray')
    ax1.axis('off')

    # 标题显示真实表情
    is_correct = (true_emotion == pred_emotion)
    title_color = 'green' if is_correct else 'red'
    ax1.set_title(f'真实表情: {EMOTION_LABELS_CN[emotion_id]} ({true_emotion})',
                 fontsize=14, fontweight='bold', color=title_color, pad=10)

    # 右侧：识别结果（概率分布柱状图）
    ax2 = plt.subplot(gs[1])

    # 颜色设置
    colors = ['#FF6B6B' if i == emotion_id else '#4ECDC4' for i in range(7)]
    if not is_correct:
        pred_idx = EMOTION_LABELS.index(pred_emotion)
        colors[pred_idx] = '#FFA500'  # 橙色表示错误预测

    bars = ax2.barh(range(7), probs, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    # 设置标签
    ax2.set_yticks(range(7))
    ax2.set_yticklabels([f'{EMOTION_LABELS_CN[i]}\n({EMOTION_LABELS[i]})' for i in range(7)],
                        fontsize=11)
    ax2.set_xlabel('概率', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    # 添加数值标签
    for i, (bar, prob) in enumerate(zip(bars, probs)):
        width = bar.get_width()
        label_x_pos = width + 0.02
        ax2.text(label_x_pos, bar.get_y() + bar.get_height()/2,
                f'{prob:.1%}',
                va='center', ha='left', fontsize=10, fontweight='bold')

    # 标题显示预测结果
    result_symbol = '✓' if is_correct else '✗'
    ax2.set_title(f'预测结果: {pred_emotion} (置信度: {confidence:.1%}) {result_symbol}',
                 fontsize=14, fontweight='bold', color=title_color, pad=10)

    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"  保存样例: {output_path}")


def create_grid_visualization(samples_info, output_path, grid_cols=3):
    """
    创建网格展示：多个样例排列在一起

    Args:
        samples_info: [(image, true_emotion, pred_emotion, confidence), ...]
        output_path: 输出路径
        grid_cols: 每行显示的样例数量
    """
    n_samples = len(samples_info)
    grid_rows = (n_samples + grid_cols - 1) // grid_cols

    fig = plt.figure(figsize=(6*grid_cols, 4*grid_rows))

    for idx, (image, true_emotion, pred_emotion, confidence, emotion_id) in enumerate(samples_info):
        # 创建子图：每个样例占2列（图片+结果）
        ax = plt.subplot(grid_rows, grid_cols, idx + 1)

        # 显示图片
        ax.imshow(image, cmap='gray')
        ax.axis('off')

        # 标题
        is_correct = (true_emotion == pred_emotion)
        result_symbol = '✓' if is_correct else '✗'
        title_color = 'green' if is_correct else 'red'

        title = f'{EMOTION_LABELS_CN[emotion_id]} → {pred_emotion}\n{confidence:.1%} {result_symbol}'
        ax.set_title(title, fontsize=12, fontweight='bold', color=title_color)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\n[INFO] 网格展示已保存: {output_path}")


def create_comparison_sheet(samples_dict, visualizer, output_dir):
    """
    创建对比表：每种表情一行，展示多个样例

    Args:
        samples_dict: {emotion_id: [(image, emotion_id), ...]}
        visualizer: FERVisualizer 实例
        output_dir: 输出目录
    """
    print("\n[INFO] 创建表情对比表...")

    n_emotions = 7
    n_samples = 3  # 每种表情显示3个样例

    fig = plt.figure(figsize=(18, 14))

    for emotion_id in range(n_emotions):
        samples = samples_dict[emotion_id][:n_samples]

        for sample_idx, (image, true_id) in enumerate(samples):
            # 预测
            pred_emotion, confidence, probs = predict_emotion(visualizer, image)

            # 计算子图位置
            row = emotion_id
            col = sample_idx * 2  # 每个样例占2列

            # 左侧：显示图片
            ax_img = plt.subplot(n_emotions, n_samples*2, row * n_samples*2 + col + 1)
            ax_img.imshow(image, cmap='gray')
            ax_img.axis('off')

            if sample_idx == 0:
                ax_img.set_ylabel(f'{EMOTION_LABELS_CN[emotion_id]}',
                                 fontsize=12, fontweight='bold', rotation=0,
                                 ha='right', va='center', labelpad=20)

            # 右侧：显示预测结果文字
            ax_text = plt.subplot(n_emotions, n_samples*2, row * n_samples*2 + col + 2)
            ax_text.axis('off')

            is_correct = (pred_emotion == EMOTION_LABELS[emotion_id])
            result_color = 'green' if is_correct else 'red'
            result_symbol = '✓' if is_correct else '✗'

            text_content = f'{result_symbol} {pred_emotion}\n{confidence:.1%}'
            ax_text.text(0.5, 0.5, text_content,
                        ha='center', va='center',
                        fontsize=11, fontweight='bold', color=result_color,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))

    plt.suptitle('FER2013 表情识别样例展示', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'emotion_comparison_sheet.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"[INFO] 对比表已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='生成 FER2013 样例展示')
    parser.add_argument('--csv', type=str, required=True,
                       help='FER2013 数据集路径')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='模型检查点路径')
    parser.add_argument('--output', type=str, default='samples_output',
                       help='输出目录')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='计算设备')
    parser.add_argument('--num_samples', type=int, default=3,
                       help='每种表情的样例数量')
    parser.add_argument('--usage', type=str, default='PublicTest',
                       choices=['Training', 'PublicTest', 'PrivateTest'],
                       help='使用哪个数据集')

    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    print(f"[INFO] 输出目录: {args.output}")

    # 检查文件
    if not os.path.exists(args.csv):
        print(f"[ERROR] 数据集文件不存在: {args.csv}")
        return

    if not os.path.exists(args.ckpt):
        print(f"[ERROR] 模型文件不存在: {args.ckpt}")
        return

    # 加载样例图片
    samples_dict = load_sample_images(args.csv, args.num_samples, args.usage)

    # 初始化可视化器
    print(f"\n[INFO] 加载模型: {args.ckpt}")
    visualizer = FERVisualizer(args.ckpt, device_target=args.device, output_dir=args.output)

    # 生成单个样例的详细展示
    print("\n[INFO] 生成单个样例的详细展示...")
    all_samples_info = []

    for emotion_id in range(7):
        emotion_dir = os.path.join(args.output, EMOTION_LABELS[emotion_id])
        os.makedirs(emotion_dir, exist_ok=True)

        print(f"\n处理表情: {EMOTION_LABELS_CN[emotion_id]} ({EMOTION_LABELS[emotion_id]})")

        for idx, (image, true_id) in enumerate(samples_dict[emotion_id]):
            # 预测
            pred_emotion, confidence, probs = predict_emotion(visualizer, image)

            # 生成单个样例展示
            output_path = os.path.join(emotion_dir, f'sample_{idx+1}.png')
            create_sample_visualization(image, EMOTION_LABELS[true_id],
                                       pred_emotion, confidence, probs,
                                       output_path, emotion_id)

            all_samples_info.append((image, EMOTION_LABELS[true_id], pred_emotion,
                                    confidence, emotion_id))

    # 生成网格展示
    print("\n[INFO] 生成网格展示...")
    grid_path = os.path.join(args.output, 'all_samples_grid.png')
    create_grid_visualization(all_samples_info, grid_path, grid_cols=4)

    # 生成对比表
    create_comparison_sheet(samples_dict, visualizer, args.output)

    # 生成统计信息
    print("\n" + "="*60)
    print("样例生成完成！")
    print("="*60)

    # 计算准确率
    correct = sum(1 for _, true, pred, _, _ in all_samples_info if true == pred)
    total = len(all_samples_info)
    accuracy = correct / total * 100

    print(f"\n样例统计:")
    print(f"  总样例数: {total}")
    print(f"  正确预测: {correct}")
    print(f"  准确率: {accuracy:.1f}%")

    print(f"\n输出文件:")
    print(f"  详细样例: {args.output}/<emotion>/sample_*.png")
    print(f"  网格展示: {grid_path}")
    print(f"  对比表: {os.path.join(args.output, 'emotion_comparison_sheet.png')}")
    print()


if __name__ == '__main__':
    main()
