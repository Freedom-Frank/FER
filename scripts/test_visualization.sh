#!/bin/bash
# 可视化功能测试脚本
# 用于 WSL/Linux 环境

set -e

echo "======================================"
echo "FER2013 可视化功能测试脚本"
echo "======================================"
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查模型文件
CKPT_PATH="checkpoints/best.ckpt"
if [ ! -f "$CKPT_PATH" ]; then
    echo -e "${RED}[错误] 未找到模型文件: $CKPT_PATH${NC}"
    echo "请先训练模型或下载预训练模型"
    echo ""
    echo "训练命令示例:"
    echo "  python src/train.py --data_csv data/FER2013/fer2013.csv --epochs 50"
    exit 1
fi

echo -e "${GREEN}[✓] 找到模型文件: $CKPT_PATH${NC}"
echo ""

# 检查 Python 依赖
echo "检查 Python 依赖..."
python3 -c "import cv2; import matplotlib; import mindspore" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] Python 依赖已安装${NC}"
else
    echo -e "${RED}[错误] 缺少依赖库${NC}"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi
echo ""

# 创建测试目录
echo "创建测试目录..."
mkdir -p output/test
mkdir -p test_images
echo -e "${GREEN}[✓] 测试目录已创建${NC}"
echo ""

# 测试选项
echo "请选择要测试的功能："
echo ""
echo "  1. 测试摄像头识别 (需要摄像头)"
echo "  2. 测试图片处理 (需要提供图片路径)"
echo "  3. 测试批量处理 (需要提供图片目录)"
echo "  4. 显示帮助信息"
echo "  5. 运行完整测试 (需要测试文件)"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}启动摄像头测试...${NC}"
        echo "按 'q' 退出，按 's' 保存帧"
        echo ""
        python3 demo_visualization.py --mode webcam --ckpt "$CKPT_PATH"
        ;;

    2)
        echo ""
        read -p "请输入图片路径: " image_path
        if [ ! -f "$image_path" ]; then
            echo -e "${RED}[错误] 图片不存在: $image_path${NC}"
            exit 1
        fi
        echo ""
        echo -e "${YELLOW}处理图片: $image_path${NC}"
        python3 demo_visualization.py --mode image --ckpt "$CKPT_PATH" --input "$image_path"
        echo ""
        echo -e "${GREEN}[✓] 处理完成！${NC}"
        echo "查看结果: output/images/"
        ;;

    3)
        echo ""
        read -p "请输入图片目录: " image_dir
        if [ ! -d "$image_dir" ]; then
            echo -e "${RED}[错误] 目录不存在: $image_dir${NC}"
            exit 1
        fi
        echo ""
        echo -e "${YELLOW}批量处理: $image_dir${NC}"
        python3 demo_visualization.py --mode batch --ckpt "$CKPT_PATH" --input "$image_dir"
        echo ""
        echo -e "${GREEN}[✓] 批量处理完成！${NC}"
        echo "查看结果: output/batch/"
        echo "统计图表: output/batch/statistics.png"
        ;;

    4)
        echo ""
        python3 demo_visualization.py --mode menu --ckpt "$CKPT_PATH"
        ;;

    5)
        echo ""
        echo -e "${YELLOW}运行完整测试...${NC}"
        echo ""

        # 检查测试文件
        if [ ! -d "test_images" ] || [ -z "$(ls -A test_images/*.jpg 2>/dev/null)" ]; then
            echo -e "${RED}[错误] 未找到测试图片${NC}"
            echo "请在 test_images/ 目录中放置一些 .jpg 图片"
            exit 1
        fi

        echo "1/3 测试单张图片处理..."
        TEST_IMAGE=$(ls test_images/*.jpg | head -n 1)
        python3 demo_visualization.py --mode image --ckpt "$CKPT_PATH" --input "$TEST_IMAGE"
        echo -e "${GREEN}[✓] 单张图片测试完成${NC}"
        echo ""

        echo "2/3 测试批量处理..."
        python3 demo_visualization.py --mode batch --ckpt "$CKPT_PATH" --input "test_images"
        echo -e "${GREEN}[✓] 批量处理测试完成${NC}"
        echo ""

        echo "3/3 测试 GPU 模式 (如果可用)..."
        python3 demo_visualization.py --mode image --ckpt "$CKPT_PATH" --input "$TEST_IMAGE" --device GPU 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[✓] GPU 模式测试完成${NC}"
        else
            echo -e "${YELLOW}[!] GPU 不可用或出错，跳过 GPU 测试${NC}"
        fi
        echo ""

        echo -e "${GREEN}======================================"
        echo "所有测试完成！"
        echo "======================================${NC}"
        echo ""
        echo "查看输出:"
        echo "  - 单张图片: output/images/"
        echo "  - 批量处理: output/batch/"
        echo "  - 统计图表: output/batch/statistics.png"
        ;;

    *)
        echo -e "${RED}[错误] 无效的选项${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}测试完成！${NC}"
