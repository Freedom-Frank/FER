#!/usr/bin/env python3
"""
测试 OpenCV Haar Cascade 加载
"""
import cv2
import os
import sys

print("=" * 70)
print("  测试 OpenCV Haar Cascade 加载")
print("=" * 70)

# 测试加载 Haar Cascade
cascade_path = None
try:
    # 方法 1：使用 cv2.data（OpenCV 4.x）
    try:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        print(f"✓ 方法 1 成功：cv2.data.haarcascades")
        print(f"  路径: {cascade_path}")
    except AttributeError:
        print(f"✗ 方法 1 失败：cv2.data 不可用")

        # 方法 2：使用 OpenCV 安装路径
        cv2_base = os.path.dirname(cv2.__file__)
        cascade_path = os.path.join(cv2_base, 'data', 'haarcascade_frontalface_default.xml')

        if os.path.exists(cascade_path):
            print(f"✓ 方法 2 成功：OpenCV 安装路径")
            print(f"  路径: {cascade_path}")
        else:
            print(f"✗ 方法 2 失败：{cascade_path} 不存在")

            # 方法 3：尝试其他常见位置
            possible_paths = [
                os.path.join(sys.prefix, 'Library', 'etc', 'haarcascades', 'haarcascade_frontalface_default.xml'),
                os.path.join(sys.prefix, 'share', 'opencv4', 'haarcascades', 'haarcascade_frontalface_default.xml'),
                os.path.join(cv2_base, '..', 'data', 'haarcascade_frontalface_default.xml'),
            ]

            print(f"\n尝试方法 3：检查常见位置")
            for i, path in enumerate(possible_paths, 1):
                if os.path.exists(path):
                    cascade_path = path
                    print(f"✓ 方法 3.{i} 成功：{path}")
                    break
                else:
                    print(f"✗ 方法 3.{i} 失败：{path} 不存在")

    # 验证文件存在
    if cascade_path and os.path.exists(cascade_path):
        print(f"\n✓ Cascade 文件存在")
        print(f"  完整路径: {cascade_path}")
        print(f"  文件大小: {os.path.getsize(cascade_path) / 1024:.1f} KB")

        # 尝试加载
        face_cascade = cv2.CascadeClassifier(cascade_path)

        if face_cascade.empty():
            print(f"\n✗ Cascade 加载失败（文件可能损坏）")
            sys.exit(1)
        else:
            print(f"\n✓ Cascade 加载成功！")
            print(f"\n🎉 OpenCV Haar Cascade 完全正常！")
            sys.exit(0)
    else:
        print(f"\n✗ 无法找到 Cascade 文件")
        print(f"\n建议：重新安装 OpenCV")
        print(f"  pip uninstall opencv-python")
        print(f"  pip install opencv-python")
        sys.exit(1)

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 70)
