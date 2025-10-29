#!/usr/bin/env python3
"""
摄像头测试脚本
用于验证摄像头是否可用
"""

import cv2
import sys

def test_camera(camera_id=0):
    """测试指定的摄像头"""
    print(f"正在测试摄像头 {camera_id}...")

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print(f"❌ 无法打开摄像头 {camera_id}")
        return False

    # 读取一帧
    ret, frame = cap.read()

    if not ret:
        print(f"❌ 无法从摄像头 {camera_id} 读取画面")
        cap.release()
        return False

    # 获取摄像头信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"✅ 摄像头 {camera_id} 可用！")
    print(f"   分辨率: {width}x{height}")
    print(f"   帧率: {fps} FPS")

    cap.release()
    return True

def test_all_cameras(max_cameras=5):
    """测试所有可用的摄像头"""
    print("="*50)
    print("摄像头检测工具")
    print("="*50)
    print()

    available_cameras = []

    for i in range(max_cameras):
        if test_camera(i):
            available_cameras.append(i)
        print()

    print("="*50)
    print("检测结果汇总")
    print("="*50)

    if len(available_cameras) == 0:
        print("❌ 未检测到可用的摄像头")
        print()
        print("可能的原因：")
        print("  1. 摄像头未连接")
        print("  2. 摄像头被其他程序占用")
        print("  3. 驱动程序问题")
        print("  4. 权限不足")
        return False
    else:
        print(f"✅ 检测到 {len(available_cameras)} 个可用摄像头：")
        for cam_id in available_cameras:
            print(f"   - 摄像头 {cam_id}")
        print()
        print("使用方法：")
        print(f"  python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --camera_id {available_cameras[0]}")
        return True

def test_opencv():
    """测试OpenCV是否已安装"""
    try:
        import cv2
        print("✅ OpenCV 已安装")
        print(f"   版本: {cv2.__version__}")
        return True
    except ImportError:
        print("❌ OpenCV 未安装")
        print("   请运行: pip install opencv-python")
        return False

if __name__ == '__main__':
    print()

    # 测试OpenCV
    if not test_opencv():
        sys.exit(1)

    print()

    # 测试摄像头
    test_all_cameras()
