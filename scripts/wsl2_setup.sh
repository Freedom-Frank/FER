#!/bin/bash
# WSL2自动配置脚本 - 在WSL2 Ubuntu中运行

set -e  # 遇到错误立即退出

echo "=========================================="
echo "MindSpore GPU WSL2 自动配置脚本"
echo "=========================================="
echo ""

# 检查是否在WSL2中运行
if ! grep -qi microsoft /proc/version; then
    echo "错误：此脚本必须在WSL2中运行！"
    exit 1
fi

echo "步骤1: 更新系统..."
sudo apt update && sudo apt upgrade -y

echo ""
echo "步骤2: 安装基础工具..."
sudo apt install -y build-essential wget git vim curl

echo ""
echo "步骤3: 验证GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi
    echo "✓ GPU检测成功！"
else
    echo "⚠ 警告：nvidia-smi未找到，请确保Windows已安装NVIDIA驱动"
fi

echo ""
echo "步骤4: 安装CUDA 11.8..."
if [ ! -f "cuda-keyring_1.0-1_all.deb" ]; then
    wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
fi
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-11-8

# 配置CUDA环境变量
if ! grep -q "cuda-11.8" ~/.bashrc; then
    echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
fi
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH

echo ""
echo "步骤5: 验证CUDA安装..."
if command -v nvcc &> /dev/null; then
    nvcc --version
    echo "✓ CUDA安装成功！"
else
    echo "⚠ CUDA安装可能未完成，请手动检查"
fi

echo ""
echo "步骤6: 安装Miniconda..."
if [ ! -d "$HOME/miniconda3" ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda3
    rm miniconda.sh
    ~/miniconda3/bin/conda init bash
    source ~/.bashrc
    echo "✓ Miniconda安装完成！"
else
    echo "✓ Miniconda已安装"
fi

echo ""
echo "步骤7: 创建Python环境..."
source ~/miniconda3/etc/profile.d/conda.sh
conda create -n fer python=3.8 -y || echo "环境已存在"
conda activate fer

echo ""
echo "步骤8: 安装Python依赖..."
pip install numpy pandas opencv-python scikit-learn

echo ""
echo "步骤9: 安装MindSpore GPU版本..."
echo "正在下载MindSpore 2.2.14..."
pip install https://ms-release.obs.cn-north-4.myhuaweicloud.com/2.2.14/MindSpore/unified/x86_64/mindspore-2.2.14-cp38-cp38-linux_x86_64.whl || \
pip install mindspore==2.2.14 || \
pip install mindspore

echo ""
echo "步骤10: 验证MindSpore GPU..."
python -c "import mindspore as ms; print('MindSpore version:', ms.__version__); ms.set_context(device_target='GPU'); print('✓ MindSpore GPU配置成功！')" || \
echo "⚠ MindSpore GPU验证失败，可能需要手动配置"

echo ""
echo "步骤11: 复制项目文件..."
PROJECT_DIR="$HOME/FER"
if [ ! -d "$PROJECT_DIR" ]; then
    if [ -d "/mnt/e/Users/Meng/Projects/VScodeProjects/FER" ]; then
        echo "正在复制项目文件到WSL2..."
        cp -r /mnt/e/Users/Meng/Projects/VScodeProjects/FER "$HOME/"
        echo "✓ 项目文件已复制到 $PROJECT_DIR"
    else
        echo "⚠ 未找到项目源目录"
    fi
else
    echo "✓ 项目目录已存在"
fi

echo ""
echo "=========================================="
echo "✓ 安装完成！"
echo "=========================================="
echo ""
echo "下一步操作："
echo "1. 重新加载环境变量："
echo "   source ~/.bashrc"
echo ""
echo "2. 激活conda环境："
echo "   conda activate fer"
echo ""
echo "3. 进入项目目录："
echo "   cd ~/FER"
echo ""
echo "4. 运行GPU训练："
echo "   python train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 64 --epochs 100 --augment"
echo ""
echo "或快速测试（2个epoch）："
echo "   python train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 32 --epochs 2 --augment"
echo ""
