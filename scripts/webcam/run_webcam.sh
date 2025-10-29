#!/bin/bash
# 快速启动实时摄像头表情识别
# 使用方法：bash run_webcam.sh

echo "========================================"
echo "FER2013 实时摄像头表情识别"
echo "========================================"
echo ""
echo "功能说明："
echo "  - 实时检测人脸并识别表情"
echo "  - 按 'q' 键退出"
echo "  - 按 's' 键保存当前帧"
echo ""
echo "正在启动摄像头..."
echo ""

# 检查模型文件是否存在（按优先级顺序）
if [ -f "checkpoints_50epoch/best_model.ckpt" ]; then
    CKPT_PATH="checkpoints_50epoch/best_model.ckpt"
elif [ -f "checkpoints/best_model.ckpt" ]; then
    CKPT_PATH="checkpoints/best_model.ckpt"
elif [ -f "checkpoints_50epoch/fer-50_449.ckpt" ]; then
    CKPT_PATH="checkpoints_50epoch/fer-50_449.ckpt"
elif [ -f "checkpoints/fer-5_449.ckpt" ]; then
    CKPT_PATH="checkpoints/fer-5_449.ckpt"
else
    echo "[ERROR] 未找到模型文件！"
    echo "请先训练模型或确保以下文件存在："
    echo "  - checkpoints_50epoch/best_model.ckpt"
    echo "  - checkpoints_50epoch/fer-50_449.ckpt"
    echo "  - checkpoints/best_model.ckpt"
    echo "  - checkpoints/fer-5_449.ckpt"
    exit 1
fi

echo "使用模型: $CKPT_PATH"
echo ""

# 检测是否有GPU
if command -v nvidia-smi &> /dev/null; then
    echo "[INFO] 检测到GPU，使用GPU模式"
    DEVICE="GPU"
else
    echo "[INFO] 未检测到GPU，使用CPU模式"
    DEVICE="CPU"
fi

# 运行摄像头识别
python tools/demo_visualization.py --mode webcam --ckpt "$CKPT_PATH" --device "$DEVICE"

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] 运行失败！可能的原因："
    echo "  1. 摄像头未连接或被占用"
    echo "  2. 缺少依赖库（需要 opencv-python）"
    echo "  3. WSL环境需要配置摄像头访问权限"
    echo ""
    echo "解决方法："
    echo "  1. 确保摄像头已连接并正常工作"
    echo "  2. 运行: pip install opencv-python"
    echo "  3. WSL用户参考: docs/visualization_setup.md"
fi
