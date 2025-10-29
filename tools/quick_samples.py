#!/usr/bin/env python3
"""
快速生成样例展示
从数据集中提取样例图片，保存为图片文件，然后使用 demo_visualization.py 处理
"""

import os
import sys
import numpy as np
import pandas as pd
import cv2
import argparse

# 表情类别
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


def extract_samples(csv_path, output_dir='test_samples', num_samples=2, usage='PublicTest'):
    """从数据集中提取样例并保存为图片文件"""

    print("\n" + "="*60)
    print("Extracting sample images from dataset...")
    print("="*60 + "\n")

    # 读取数据集
    df = pd.read_csv(csv_path)
    df_subset = df[df['Usage'] == usage]

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    extracted_files = []

    for emotion_id in range(7):
        emotion_name = EMOTION_LABELS[emotion_id]
        emotion_dir = os.path.join(output_dir, emotion_name)
        os.makedirs(emotion_dir, exist_ok=True)

        # 获取该表情的所有样本
        emotion_data = df_subset[df_subset['emotion'] == emotion_id]

        if len(emotion_data) == 0:
            print(f"[WARNING] No samples found for {emotion_name}")
            continue

        # 随机选择样例
        num_to_extract = min(num_samples, len(emotion_data))
        sample_indices = np.random.choice(len(emotion_data), num_to_extract, replace=False)

        print(f"Extracting {num_to_extract} samples for {emotion_name}...")

        for idx, sample_idx in enumerate(sample_indices):
            row = emotion_data.iloc[sample_idx]
            pixels = np.array([int(p) for p in row['pixels'].split()], dtype=np.uint8)
            image = pixels.reshape(48, 48)

            # 保存图片
            filename = f"{emotion_name}_{idx+1}.jpg"
            filepath = os.path.join(emotion_dir, filename)
            cv2.imwrite(filepath, image)

            extracted_files.append(filepath)
            print(f"  Saved: {filepath}")

    print(f"\n[INFO] Total {len(extracted_files)} images extracted to {output_dir}/")
    return output_dir


def process_with_visualization(samples_dir, ckpt_path, device='CPU'):
    """使用现有的可视化工具处理样例"""

    print("\n" + "="*60)
    print("Processing samples with FER model...")
    print("="*60 + "\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    sys.path.insert(0, os.path.join(project_root, 'src'))
    from visualize import FERVisualizer

    # 初始化可视化器
    output_dir = 'samples_results'
    visualizer = FERVisualizer(ckpt_path, device_target=device, output_dir=output_dir)

    # 处理所有样例
    for emotion_name in EMOTION_LABELS:
        emotion_dir = os.path.join(samples_dir, emotion_name)

        if not os.path.exists(emotion_dir):
            continue

        print(f"\nProcessing {emotion_name} samples...")

        # 获取该表情目录下的所有图片
        image_files = [f for f in os.listdir(emotion_dir) if f.endswith(('.jpg', '.png'))]

        for image_file in image_files:
            image_path = os.path.join(emotion_dir, image_file)
            print(f"  Processing: {image_path}")

            try:
                visualizer.process_image(image_path, save_result=True)
            except Exception as e:
                print(f"  [ERROR] Failed to process {image_path}: {e}")

    print("\n" + "="*60)
    print("Processing complete!")
    print("="*60)
    print(f"\nResults saved to: {output_dir}/")
    print(f"  Annotated images: {output_dir}/*_annotated.jpg")
    print(f"  Probability charts: {output_dir}/*_result.png")
    print()


def main():
    parser = argparse.ArgumentParser(description='Quick sample generator')
    parser.add_argument('--csv', type=str, default='data/FER2013/fer2013.csv',
                       help='FER2013 dataset CSV path')
    parser.add_argument('--ckpt', type=str, default='checkpoints/best_model.ckpt',
                       help='Model checkpoint path')
    parser.add_argument('--samples_dir', type=str, default='test_samples',
                       help='Directory to extract samples to')
    parser.add_argument('--num_samples', type=int, default=2,
                       help='Number of samples per emotion')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='Device')
    parser.add_argument('--skip_extract', action='store_true',
                       help='Skip extraction, only process existing samples')

    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.csv):
        print(f"[ERROR] Dataset not found: {args.csv}")
        return

    if not os.path.exists(args.ckpt):
        print(f"[ERROR] Model not found: {args.ckpt}")
        # 尝试查找其他模型
        alt_model = 'checkpoints/fer-5_449.ckpt'
        if os.path.exists(alt_model):
            print(f"[INFO] Using alternative model: {alt_model}")
            args.ckpt = alt_model
        else:
            print("[ERROR] No valid model found")
            return

    # 步骤1：提取样例图片
    if not args.skip_extract:
        samples_dir = extract_samples(args.csv, args.samples_dir, args.num_samples)
    else:
        samples_dir = args.samples_dir
        print(f"[INFO] Using existing samples in {samples_dir}")

    # 步骤2：使用模型处理样例
    process_with_visualization(samples_dir, args.ckpt, args.device)


if __name__ == '__main__':
    main()
