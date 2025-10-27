#!/usr/bin/env python3
"""
FER2013 可视化功能快速演示脚本
用于在 WSL/Linux 环境中快速测试各种可视化功能
"""

import os
import sys
import argparse

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from visualize import FERVisualizer


def demo_webcam(ckpt_path, device='CPU'):
    """演示实时摄像头识别"""
    print("\n" + "="*60)
    print("演示：实时摄像头表情识别")
    print("="*60)
    print("按 'q' 退出，按 's' 保存当前帧")
    print()

    visualizer = FERVisualizer(ckpt_path, device_target=device, output_dir='output/webcam')
    visualizer.process_webcam(camera_id=0, save_frames=True)


def demo_image(ckpt_path, image_path, device='CPU'):
    """演示单张图片处理"""
    print("\n" + "="*60)
    print(f"演示：图片表情识别")
    print("="*60)
    print(f"输入图片: {image_path}")
    print()

    visualizer = FERVisualizer(ckpt_path, device_target=device, output_dir='output/images')
    visualizer.process_image(image_path, save_result=True)

    print("\n结果已保存到 output/images/ 目录")


def demo_video(ckpt_path, video_path, device='CPU'):
    """演示视频处理"""
    print("\n" + "="*60)
    print("演示：视频表情识别")
    print("="*60)
    print(f"输入视频: {video_path}")
    print()

    visualizer = FERVisualizer(ckpt_path, device_target=device, output_dir='output/videos')
    visualizer.process_video(video_path, save_video=True)

    print("\n处理后的视频已保存到 output/videos/ 目录")


def demo_batch(ckpt_path, image_dir, device='CPU'):
    """演示批量图片处理"""
    print("\n" + "="*60)
    print("演示：批量图片处理与统计")
    print("="*60)
    print(f"输入目录: {image_dir}")
    print()

    visualizer = FERVisualizer(ckpt_path, device_target=device, output_dir='output/batch')
    visualizer.process_batch(image_dir, pattern='*.jpg')

    print("\n批量处理结果已保存到 output/batch/ 目录")
    print("查看 output/batch/statistics.png 了解表情分布统计")


def create_test_structure():
    """创建测试目录结构"""
    dirs = [
        'output/webcam',
        'output/images',
        'output/videos',
        'output/batch',
        'test_images'
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    print("[INFO] 测试目录结构已创建")


def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("FER2013 可视化功能演示菜单")
    print("="*60)
    print("\n可用的演示模式:")
    print("  1. webcam  - 实时摄像头表情识别 (需要摄像头)")
    print("  2. image   - 单张图片处理")
    print("  3. video   - 视频文件处理")
    print("  4. batch   - 批量图片处理与统计")
    print("  5. all     - 运行所有演示 (除了 webcam)")
    print("\n使用示例:")
    print("  python demo_visualization.py --mode webcam --ckpt checkpoints/best.ckpt")
    print("  python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input test.jpg")
    print("  python demo_visualization.py --mode video --ckpt checkpoints/best.ckpt --input test.mp4")
    print("  python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input test_images/")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='FER2013 可视化功能演示',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--mode', type=str, required=True,
                       choices=['webcam', 'image', 'video', 'batch', 'all', 'menu'],
                       help='演示模式')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='模型检查点路径')
    parser.add_argument('--input', type=str,
                       help='输入文件/目录 (根据模式不同)')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='计算设备')

    args = parser.parse_args()

    # 创建测试目录
    create_test_structure()

    # 检查模型文件
    if not os.path.exists(args.ckpt):
        print(f"[ERROR] 模型文件不存在: {args.ckpt}")
        print("\n请先训练模型或下载预训练模型:")
        print("  python src/train.py --data_csv data/FER2013/fer2013.csv --epochs 50")
        return

    # 根据模式运行演示
    if args.mode == 'menu':
        print_menu()

    elif args.mode == 'webcam':
        demo_webcam(args.ckpt, args.device)

    elif args.mode == 'image':
        if not args.input:
            print("[ERROR] image 模式需要 --input 参数")
            return
        if not os.path.exists(args.input):
            print(f"[ERROR] 图片不存在: {args.input}")
            return
        demo_image(args.ckpt, args.input, args.device)

    elif args.mode == 'video':
        if not args.input:
            print("[ERROR] video 模式需要 --input 参数")
            return
        if not os.path.exists(args.input):
            print(f"[ERROR] 视频不存在: {args.input}")
            return
        demo_video(args.ckpt, args.input, args.device)

    elif args.mode == 'batch':
        if not args.input:
            print("[ERROR] batch 模式需要 --input 参数")
            return
        if not os.path.isdir(args.input):
            print(f"[ERROR] 目录不存在: {args.input}")
            return
        demo_batch(args.ckpt, args.input, args.device)

    elif args.mode == 'all':
        print("\n运行所有演示 (除了 webcam)...")

        # 检查测试文件
        if args.input:
            if os.path.isfile(args.input):
                demo_image(args.ckpt, args.input, args.device)
            elif os.path.isdir(args.input):
                demo_batch(args.ckpt, args.input, args.device)
            else:
                print("[WARNING] 未找到有效的测试文件/目录")
        else:
            print("[INFO] 使用 --input 参数指定测试文件/目录以运行所有演示")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_menu()
        print("\n使用 --help 查看详细帮助")
    else:
        main()
