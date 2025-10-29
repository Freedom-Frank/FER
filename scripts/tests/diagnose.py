#!/usr/bin/env python3
"""
诊断脚本 - 检查所有依赖和配置
"""

import sys
import os

def print_section(title):
    """打印分隔线"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_python():
    """检查 Python 版本"""
    print_section("Python 版本")
    print(f"Python: {sys.version}")
    print(f"路径: {sys.executable}")

def check_opencv():
    """检查 OpenCV"""
    print_section("OpenCV")
    try:
        import cv2
        print(f"✓ OpenCV 已安装")
        print(f"  版本: {cv2.__version__}")
        print(f"  路径: {cv2.__file__}")

        # 检查 cv2.data
        if hasattr(cv2, 'data'):
            print(f"✓ cv2.data 可用")
            print(f"  路径: {cv2.data.haarcascades}")
        else:
            print(f"✗ cv2.data 不可用")
            print(f"  这可能导致人脸检测失败")

        # 检查摄像头
        print("\n测试摄像头访问...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ 摄像头可访问")
            cap.release()
        else:
            print("✗ 无法打开摄像头")

    except ImportError as e:
        print(f"✗ OpenCV 未安装: {e}")
        print("  安装: pip install opencv-python")

def check_mindspore():
    """检查 MindSpore"""
    print_section("MindSpore")
    try:
        import mindspore as ms
        print(f"✓ MindSpore 已安装")
        print(f"  版本: {ms.__version__}")
        print(f"  路径: {ms.__file__}")
    except ImportError as e:
        print(f"✗ MindSpore 未安装: {e}")
    except AttributeError as e:
        print(f"✗ MindSpore 导入错误（PIL 兼容性问题）")
        print(f"  错误: {e}")
        print(f"  修复: pip install Pillow==9.5.0")

def check_pillow():
    """检查 Pillow"""
    print_section("Pillow")
    try:
        from PIL import Image
        import PIL
        print(f"✓ Pillow 已安装")
        print(f"  版本: {PIL.__version__}")

        # 检查 ANTIALIAS
        if hasattr(Image, 'ANTIALIAS'):
            print(f"✓ Image.ANTIALIAS 可用")
        else:
            print(f"✗ Image.ANTIALIAS 不可用（Pillow >= 10.0）")
            print(f"  推荐降级: pip install Pillow==9.5.0")

    except ImportError as e:
        print(f"✗ Pillow 未安装: {e}")

def check_other_deps():
    """检查其他依赖"""
    print_section("其他依赖")

    deps = [
        ('numpy', 'NumPy'),
        ('matplotlib', 'Matplotlib'),
        ('pandas', 'Pandas'),
    ]

    for module, name in deps:
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {name}: {version}")
        except ImportError:
            print(f"✗ {name}: 未安装")

def check_model_files():
    """检查模型文件"""
    print_section("模型文件")

    model_paths = [
        'checkpoints_50epoch/best_model.ckpt',
        'checkpoints/best_model.ckpt',
        'checkpoints_50epoch/fer-50_449.ckpt',
    ]

    found = False
    for path in model_paths:
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)  # MB
            print(f"✓ {path} ({size:.1f} MB)")
            found = True
        else:
            print(f"✗ {path} (不存在)")

    if not found:
        print("\n⚠ 警告：未找到任何模型文件！")

def check_directories():
    """检查目录结构"""
    print_section("目录结构")

    dirs = [
        'src',
        'tools',
        'checkpoints_50epoch',
        'output',
        'output/webcam',
    ]

    for d in dirs:
        if os.path.exists(d):
            print(f"✓ {d}/")
        else:
            print(f"✗ {d}/ (不存在)")

def suggest_fixes():
    """建议修复方案"""
    print_section("修复建议")

    print("""
如果遇到问题，按以下步骤修复：

1. PIL/Pillow 错误：
   pip install Pillow==9.5.0

2. OpenCV 问题：
   pip uninstall opencv-python
   pip install opencv-python

3. MindSpore 问题：
   pip install mindspore==2.0.0

4. 摄像头问题：
   - WSL: 在 Windows 上运行（查看 WSL_WEBCAM_SETUP.md）
   - Windows: 检查摄像头权限和驱动

5. 重新安装所有依赖：
   pip install -r requirements.txt

详细文档：
- FIX_PIL_ERROR.md - PIL 错误修复
- OPENCV_FIX.md - OpenCV 错误修复
- WINDOWS_SETUP.md - Windows 配置
- WSL_WEBCAM_SETUP.md - WSL 配置
    """)

def main():
    """主函数"""
    print("\n" + "="*70)
    print("  FER 项目诊断工具")
    print("="*70)

    check_python()
    check_opencv()
    check_mindspore()
    check_pillow()
    check_other_deps()
    check_model_files()
    check_directories()
    suggest_fixes()

    print("\n" + "="*70)
    print("  诊断完成")
    print("="*70)
    print()

if __name__ == '__main__':
    main()
