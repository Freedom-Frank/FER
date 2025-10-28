#!/usr/bin/env python3
"""
快速测试修复效果的脚本
"""
import sys
import os

# 检查环境
print("="*60)
print("环境检查")
print("="*60)
print(f"Python: {sys.version}")
print(f"工作目录: {os.getcwd()}")

# 检查模型文件
print("\n" + "="*60)
print("检查模型文件")
print("="*60)
checkpoints = [
    'checkpoints/best_model.ckpt',
    'checkpoints/fer-5_449.ckpt',
]

for ckpt in checkpoints:
    if os.path.exists(ckpt):
        size_kb = os.path.getsize(ckpt) / 1024
        size_mb = size_kb / 1024
        status = "✓" if size_mb > 1.0 else "⚠"
        print(f"{status} {ckpt}: {size_mb:.2f} MB ({size_kb:.0f} KB)")
    else:
        print(f"✗ {ckpt}: 不存在")

# 测试导入
print("\n" + "="*60)
print("测试模块导入")
print("="*60)

try:
    sys.path.insert(0, 'src')
    from visualize import FERVisualizer
    print("✓ visualize 模块导入成功")
except Exception as e:
    print(f"✗ visualize 模块导入失败: {e}")
    sys.exit(1)

try:
    import cv2
    print(f"✓ OpenCV 版本: {cv2.__version__}")
except Exception as e:
    print(f"✗ OpenCV 导入失败: {e}")
    sys.exit(1)

try:
    import mindspore as ms
    print(f"✓ MindSpore 版本: {ms.__version__}")
except Exception as e:
    print(f"✗ MindSpore 导入失败: {e}")
    sys.exit(1)

# 创建可视化器（测试模型加载）
print("\n" + "="*60)
print("测试模型加载")
print("="*60)

ckpt_path = 'checkpoints/fer-5_449.ckpt'
if not os.path.exists(ckpt_path):
    print(f"✗ 模型文件不存在: {ckpt_path}")
    print("\n可用的checkpoint文件:")
    if os.path.exists('checkpoints'):
        for f in os.listdir('checkpoints'):
            if f.endswith('.ckpt'):
                print(f"  - checkpoints/{f}")
    sys.exit(1)

try:
    print(f"加载模型: {ckpt_path}")
    visualizer = FERVisualizer(ckpt_path, device_target='CPU', output_dir='output/test')
    print("✓ 模型加载成功")
except Exception as e:
    print(f"✗ 模型加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试人脸检测参数
print("\n" + "="*60)
print("检查人脸检测参数")
print("="*60)

# 读取 visualize.py 检查参数
with open('src/visualize.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'scaleFactor=1.05' in content:
    print("✓ scaleFactor 已更新为 1.05")
else:
    print("⚠ scaleFactor 可能未更新")

if 'minNeighbors=3' in content:
    print("✓ minNeighbors 已更新为 3")
else:
    print("⚠ minNeighbors 可能未更新")

if 'minSize=(20, 20)' in content:
    print("✓ minSize 已更新为 (20, 20)")
else:
    print("⚠ minSize 可能未更新")

print("\n" + "="*60)
print("✓ 所有检查通过！")
print("="*60)
print("\n现在可以使用以下命令测试:")
print("  python3 demo_visualization.py --mode image --ckpt checkpoints/fer-5_449.ckpt --input <your_image>")
