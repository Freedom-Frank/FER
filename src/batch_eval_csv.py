#!/usr/bin/env python3
"""
从 CSV 文件批量评估 FER2013 模型
直接使用 CSV 中的像素数据，不需要人脸检测，避免漏检问题
"""

import argparse
import numpy as np
import pandas as pd
import mindspore as ms
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os
from tqdm import tqdm

# 添加 src 目录到路径
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from model import SimpleCNN
try:
    from model_legacy import SimpleCNN_Legacy
except ImportError:
    SimpleCNN_Legacy = None

# 表情标签
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_COLORS = {
    'angry': (0, 0, 255),
    'disgust': (0, 255, 0),
    'fear': (255, 0, 255),
    'happy': (0, 255, 255),
    'sad': (255, 0, 0),
    'surprise': (255, 165, 0),
    'neutral': (128, 128, 128)
}


class CSVBatchEvaluator:
    """CSV 批量评估器"""

    def __init__(self, ckpt_path, device_target='CPU', output_dir='output/batch'):
        """
        初始化评估器

        Args:
            ckpt_path: 模型检查点路径
            device_target: 设备类型
            output_dir: 输出目录
        """
        context.set_context(mode=context.GRAPH_MODE, device_target=device_target)

        print(f"[INFO] Loading model from {ckpt_path}")
        self.net = self._load_model_with_auto_detection(ckpt_path)
        self.net.set_train(False)

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        print(f"[INFO] Evaluator initialized. Output: {output_dir}")

    def _load_model_with_auto_detection(self, ckpt_path):
        """自动检测并加载正确版本的模型"""
        param_dict = load_checkpoint(ckpt_path)
        classifier_key = 'classifier.0.weight'

        if classifier_key in param_dict:
            classifier_shape = param_dict[classifier_key].shape
            print(f"[INFO] Detected classifier shape: {classifier_shape}")

            if classifier_shape == (128, 128):
                if SimpleCNN_Legacy is None:
                    print("[ERROR] Legacy model detected but model_legacy.py not found")
                    raise ImportError("Please ensure model_legacy.py exists in src/")
                print("[INFO] Loading legacy model (128 -> 128 -> 7)")
                net = SimpleCNN_Legacy(7)
            else:
                print("[INFO] Loading current model (512 -> 256 -> 128 -> 7)")
                net = SimpleCNN(7)

            load_param_into_net(net, param_dict)
            return net
        else:
            print("[WARNING] Cannot determine model version, using current model")
            net = SimpleCNN(7)
            load_param_into_net(net, param_dict)
            return net

    def preprocess_pixels(self, pixels_str):
        """
        预处理像素字符串

        Args:
            pixels_str: 空格分隔的像素字符串

        Returns:
            预处理后的张量 [1, 1, 48, 48]
        """
        # 解析像素
        pixels = np.array([int(p) for p in pixels_str.split()], dtype='float32')
        # 重塑为 48x48
        img = pixels.reshape(48, 48)
        # 归一化
        img = img / 255.0
        # 扩展维度
        tensor = np.expand_dims(img, (0, 1))
        return tensor

    def predict(self, pixels_str):
        """
        预测表情

        Args:
            pixels_str: 像素字符串

        Returns:
            (emotion_idx, probability, all_probs)
        """
        tensor = self.preprocess_pixels(pixels_str)
        output = self.net(ms.Tensor(tensor))
        probs = ms.ops.softmax(output)[0].asnumpy()

        idx = int(np.argmax(probs))
        probability = float(probs[idx])

        return idx, probability, probs

    def evaluate_category(self, df_category, category_name):
        """
        评估单个类别

        Args:
            df_category: 该类别的数据框
            category_name: 类别名称

        Returns:
            结果字典
        """
        print(f"\n{'='*70}")
        print(f"Evaluating category: {category_name.upper()}")
        print(f"{'='*70}")

        emotion_counts = {emotion: 0 for emotion in EMOTIONS}
        total = len(df_category)
        correct = 0

        # 使用 tqdm 显示进度
        for idx, row in tqdm(df_category.iterrows(), total=total, desc=f"Processing {category_name}"):
            try:
                pixels = row['pixels']
                true_label = int(row['emotion'])

                # 预测
                pred_idx, prob, probs = self.predict(pixels)

                # 统计
                pred_emotion = EMOTIONS[pred_idx]
                emotion_counts[pred_emotion] += 1

                if pred_idx == true_label:
                    correct += 1

            except Exception as e:
                print(f"\n[WARNING] Error processing row {idx}: {e}")
                continue

        # 计算准确率
        accuracy = correct / total if total > 0 else 0

        print(f"\n[INFO] Category: {category_name.upper()}")
        print(f"[INFO] Total images: {total}")
        print(f"[INFO] Correct predictions: {correct}")
        print(f"[INFO] Accuracy: {accuracy:.2%}")
        print("\n[STATISTICS] Prediction distribution:")
        for emotion, count in emotion_counts.items():
            percentage = count / total * 100 if total > 0 else 0
            marker = " ← TRUE LABEL" if emotion == category_name else ""
            print(f"  {emotion}: {count} ({percentage:.1f}%){marker}")

        return {
            'category': category_name,
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'distribution': emotion_counts
        }

    def evaluate_all_categories(self, csv_path, usage='PrivateTest'):
        """
        评估所有类别

        Args:
            csv_path: CSV 文件路径
            usage: 使用哪个数据集 (Training/PublicTest/PrivateTest)
        """
        print("\n" + "="*70)
        print("CSV BATCH EVALUATION - ALL CATEGORIES")
        print("="*70)
        print(f"[INFO] CSV file: {csv_path}")
        print(f"[INFO] Usage: {usage}")

        # 读取 CSV
        print("\n[INFO] Loading CSV file...")
        df = pd.read_csv(csv_path)

        # 过滤指定的数据集
        df = df[df['Usage'] == usage]
        print(f"[INFO] Found {len(df)} images in {usage} set")

        # 按类别分组
        all_results = []
        for emotion_idx, emotion_name in enumerate(EMOTIONS):
            df_category = df[df['emotion'] == emotion_idx]

            if len(df_category) == 0:
                print(f"\n[WARNING] No data found for {emotion_name}")
                continue

            # 评估该类别
            result = self.evaluate_category(df_category, emotion_name)
            all_results.append(result)

            # 保存统计图
            self.save_statistics(
                result['distribution'],
                result['category'],
                result['accuracy']
            )

        # 生成总体报告
        if len(all_results) > 0:
            self.generate_overall_report(all_results)

        print(f"\n{'='*70}")
        print("ALL CATEGORIES EVALUATED!")
        print(f"Results saved to: {self.output_dir}")
        print(f"{'='*70}\n")

    def save_statistics(self, emotion_counts, category_name, accuracy):
        """保存统计图"""
        fig, ax = plt.subplots(figsize=(10, 6))

        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())

        # 颜色：真实类别用绿色
        colors = []
        for e in emotions:
            if e == category_name:
                colors.append((0.2, 0.8, 0.2))
            else:
                color = EMOTION_COLORS[e]
                colors.append((color[2]/255, color[1]/255, color[0]/255))

        bars = ax.bar(emotions, counts, color=colors, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Predicted Emotion', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')

        title = f'Prediction Distribution - TRUE LABEL: {category_name.upper()}'
        title += f'\nAccuracy: {accuracy:.2%}'
        ax.set_title(title, fontsize=14, fontweight='bold')

        # 添加数值标签
        total = sum(counts)
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            percentage = count / total * 100 if total > 0 else 0
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}\n({percentage:.1f}%)',
                   ha='center', va='bottom', fontsize=9)

        # 图例
        legend_elements = [
            Patch(facecolor=(0.2, 0.8, 0.2), edgecolor='black', label='True Label'),
            Patch(facecolor=(0.5, 0.5, 0.5), edgecolor='black', label='Other Emotions')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f'statistics_{category_name}.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Statistics saved to {output_path}")

    def generate_overall_report(self, results):
        """生成总体报告"""
        print("\n" + "="*70)
        print("OVERALL ACCURACY REPORT")
        print("="*70)

        # 排序
        sorted_results = sorted(results, key=lambda x: x['accuracy'], reverse=True)

        # 打印表格
        print(f"\n{'Category':<12} {'Total':<8} {'Correct':<8} {'Accuracy':<10} {'Rank':<6}")
        print("-" * 70)
        for i, result in enumerate(sorted_results, 1):
            print(f"{result['category']:<12} {result['total']:<8} "
                  f"{result['correct']:<8} {result['accuracy']:<10.2%} #{i}")

        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        print("-" * 70)
        print(f"{'AVERAGE':<12} {'':<8} {'':<8} {avg_accuracy:<10.2%}")
        print()

        # 保存对比图
        self.save_accuracy_comparison(sorted_results)

    def save_accuracy_comparison(self, results):
        """保存准确率对比图"""
        fig, ax = plt.subplots(figsize=(12, 7))

        categories = [r['category'] for r in results]
        accuracies = [r['accuracy'] * 100 for r in results]

        # 颜色编码
        colors = []
        for acc in accuracies:
            if acc >= 70:
                colors.append((0.2, 0.8, 0.2))
            elif acc >= 50:
                colors.append((1.0, 0.8, 0.0))
            else:
                colors.append((1.0, 0.2, 0.2))

        bars = ax.bar(categories, accuracies, color=colors, edgecolor='black', linewidth=2)

        ax.set_xlabel('Emotion Category', fontsize=13, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
        ax.set_title('Accuracy Comparison by Category\n(Ranked from Highest to Lowest)',
                    fontsize=15, fontweight='bold')
        ax.set_ylim(0, 100)

        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # 标注
        for i, (bar, acc, result) in enumerate(zip(bars, accuracies, results), 1):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{acc:.1f}%',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
            ax.text(bar.get_x() + bar.get_width()/2., height - 5,
                   f'#{i}',
                   ha='center', va='top', fontsize=10, color='white', fontweight='bold')
            ax.text(bar.get_x() + bar.get_width()/2., 3,
                   f'n={result["total"]}',
                   ha='center', va='bottom', fontsize=8, color='black')

        # 平均线
        avg_acc = sum(accuracies) / len(accuracies)
        ax.axhline(y=avg_acc, color='blue', linestyle='--', linewidth=2,
                  label=f'Average: {avg_acc:.1f}%')
        ax.legend(loc='lower left', fontsize=11)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'accuracy_comparison.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Accuracy comparison saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='批量评估 FER2013 模型（使用 CSV 数据）',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--csv', type=str, required=True,
                       help='FER2013 CSV 文件路径')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='模型检查点路径')
    parser.add_argument('--usage', type=str, default='PrivateTest',
                       choices=['Training', 'PublicTest', 'PrivateTest'],
                       help='使用哪个数据集 (默认: PrivateTest)')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='计算设备')
    parser.add_argument('--output', type=str, default='output/batch_csv',
                       help='输出目录')

    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.csv):
        print(f"[ERROR] CSV 文件不存在: {args.csv}")
        return

    if not os.path.exists(args.ckpt):
        print(f"[ERROR] 模型文件不存在: {args.ckpt}")
        return

    # 创建评估器
    evaluator = CSVBatchEvaluator(
        ckpt_path=args.ckpt,
        device_target=args.device,
        output_dir=args.output
    )

    # 评估所有类别
    evaluator.evaluate_all_categories(args.csv, args.usage)


if __name__ == '__main__':
    main()
