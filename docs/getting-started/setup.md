# 环境配置指南

本指南详细说明如何在不同平台上配置 FER2013 项目的运行环境。

## 目录

- [Windows CPU 环境](#windows-cpu-环境)
- [WSL2 GPU 环境](#wsl2-gpu-环境)
- [自动化配置脚本](#自动化配置脚本)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

## 环境选择

| 环境 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Windows CPU** | 配置简单 | 训练慢(20分钟/epoch) | 快速测试、代码验证 |
| **WSL2 GPU** | 训练快(1-2分钟/epoch) | 配置复杂 | 完整训练、生产环境 |

**推荐**: 首次测试使用 Windows CPU,完整训练使用 WSL2 GPU。

## Windows CPU 环境

### 系统要求

- Windows 10/11
- Python 3.7-3.9
- 4GB+ RAM (推荐 8GB)
- 10GB+ 磁盘空间

### 安装步骤

#### 1. 安装 Python

从 [Python官网](https://www.python.org/downloads/) 下载并安装 Python 3.7-3.9。

```bash
# 验证安装
python --version
```

#### 2. 创建虚拟环境(可选但推荐)

```bash
# 使用 conda
conda create -n fer python=3.8 -y
conda activate fer

# 或使用 venv
python -m venv fer_env
fer_env\Scripts\activate
```

#### 3. 安装依赖

```bash
# 进入项目目录
cd E:\Users\Meng\Projects\VScodeProjects\FER

# 安装 MindSpore CPU 版本
pip install mindspore==2.0.0

# 安装其他依赖
pip install pandas opencv-python scikit-learn numpy
```

#### 4. 验证安装

```bash
python -c "import mindspore as ms; print('MindSpore version:', ms.__version__)"
python -c "import pandas; import cv2; import sklearn; print('All dependencies OK')"
```

### 快速测试

```bash
python src/train.py --data_csv data/FER2013/fer2013.csv --device_target CPU --batch_size 32 --epochs 2
```

## WSL2 GPU 环境

### 前置条件

- Windows 10 (版本 2004+) 或 Windows 11
- NVIDIA GPU (支持 CUDA)
- 最新 NVIDIA 驱动 (已安装)

### 步骤 1: 安装 WSL2

#### 1.1 启用 WSL 功能

以管理员身份运行 PowerShell:

```powershell
# 启用 WSL 和虚拟机平台
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启电脑
shutdown /r /t 0
```

#### 1.2 设置 WSL2 为默认版本

重启后,再次以管理员身份运行 PowerShell:

```powershell
wsl --set-default-version 2
```

#### 1.3 安装 Ubuntu 22.04

```powershell
# 查看可用发行版
wsl --list --online

# 安装 Ubuntu 22.04(推荐)
wsl --install -d Ubuntu-22.04
```

安装完成后,按提示设置 Ubuntu 用户名和密码。

#### 1.4 验证安装

```powershell
wsl --list --verbose
```

确认 `VERSION` 列显示 `2`。

### 步骤 2: 配置 WSL2 中的 CUDA 环境

#### 2.1 进入 WSL2

```powershell
wsl
```

#### 2.2 更新系统

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential wget git vim
```

#### 2.3 验证 GPU 可用性

```bash
nvidia-smi
```

**重要**: WSL2 自动使用 Windows 主机的 NVIDIA 驱动,无需单独安装驱动!

应该能看到类似输出:

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 576.83       Driver Version: 576.83       CUDA Version: 12.9    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ... Off  | 00000000:01:00.0  On |                  N/A |
```

#### 2.4 安装 CUDA Toolkit 11.8

```bash
# 添加 NVIDIA 包仓库
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update

# 安装 CUDA 11.8
sudo apt install -y cuda-11-8

# 配置环境变量
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 验证 CUDA 安装
nvcc --version
```

### 步骤 3: 安装 Python 和 MindSpore

#### 3.1 安装 Miniconda

```bash
# 下载 Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 安装
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# 初始化
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

#### 3.2 创建 Python 环境

```bash
# 创建 Python 3.8 环境
conda create -n fer python=3.8 -y
conda activate fer
```

#### 3.3 安装 MindSpore GPU 版本

```bash
# 安装基础依赖
pip install numpy pandas opencv-python scikit-learn

# 安装 MindSpore GPU 版本(CUDA 11.8)
pip install https://ms-release.obs.cn-north-4.myhuaweicloud.com/2.2.14/MindSpore/unified/x86_64/mindspore-2.2.14-cp38-cp38-linux_x86_64.whl
```

如果上述链接失效,访问 [MindSpore官网](https://www.mindspore.cn/install) 获取最新链接。

#### 3.4 配置库路径(重要!)

每次训练前需要设置:

```bash
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/lib/wsl/lib:$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-11.8/bin:$PATH
```

或添加到 `~/.bashrc` 以自动设置:

```bash
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/lib/wsl/lib:$CONDA_PREFIX/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 步骤 4: 复制项目到 WSL2

#### 方案 A: 直接访问 Windows 文件(简单但较慢)

```bash
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER
```

#### 方案 B: 复制到 WSL2 本地(推荐,性能更好)

```bash
# 复制项目
cp -r /mnt/e/Users/Meng/Projects/VScodeProjects/FER ~/FER
cd ~/FER
```

**注意**: 方案 B 文件读写速度快约 10 倍!

### 步骤 5: 运行 GPU 训练

```bash
# 激活环境
conda activate fer

# 快速测试(2 epochs)
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 2 \
  --augment

# 完整训练(200 epochs)
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 200 \
  --lr 7e-4 \
  --patience 30 \
  --weight_decay 3e-5 \
  --label_smoothing 0.12 \
  --augment \
  --mixup \
  --mixup_alpha 0.4
```

## 自动化配置脚本

### 使用自动配置脚本(推荐)

项目提供了自动配置脚本 `scripts/wsl2_setup.sh`,可以自动完成 WSL2 环境配置。

#### 使用方法

```bash
# 1. 进入 WSL2
wsl

# 2. 复制并运行脚本
cp /mnt/e/Users/Meng/Projects/VScodeProjects/FER/scripts/wsl2_setup.sh ~/
bash ~/wsl2_setup.sh
```

脚本会自动完成:
- ✅ 安装 CUDA 11.8
- ✅ 安装 Miniconda
- ✅ 创建 Python 环境
- ✅ 安装 MindSpore GPU
- ✅ 复制项目文件
- ✅ 配置环境变量

## VSCode 集成(可选)

### 在 VSCode 中使用 WSL2

#### 1. 安装扩展

在 Windows VSCode 中安装:
- Remote - WSL
- Remote Development

#### 2. 连接到 WSL

1. 按 `Ctrl+Shift+P`
2. 选择 "WSL: Connect to WSL"
3. 打开项目文件夹: `~/FER`

现在可以在 VSCode 中直接编辑和运行 WSL2 中的代码!

#### 3. 配置 Python 解释器

1. 按 `Ctrl+Shift+P`
2. 选择 "Python: Select Interpreter"
3. 选择 conda 环境: `~/miniconda3/envs/fer/bin/python`

## 验证安装

### Windows CPU

```bash
# 验证 MindSpore
python -c "import mindspore as ms; ms.set_context(device_target='CPU'); print('MindSpore CPU is ready!')"

# 验证依赖
python -c "import pandas; import cv2; import sklearn; print('All dependencies OK')"
```

### WSL2 GPU

```bash
# 验证 GPU 可见
nvidia-smi

# 验证 CUDA
nvcc --version

# 验证 MindSpore GPU
python -c "import mindspore as ms; ms.set_context(device_target='GPU'); print('MindSpore GPU is ready!')"
```

## 性能对比

| 环境 | 每 epoch 时间 | 100 epochs 总时间 | 配置难度 |
|------|--------------|------------------|---------|
| **Windows CPU** | 15-20分钟 | 25-33小时 | ⭐ 简单 |
| **WSL2 GPU** | 1-2分钟 | 2-3小时 | ⭐⭐⭐ 中等 |

**速度提升**: GPU 比 CPU 快 **5-10 倍**!

## 常见问题

### Q1: nvidia-smi 显示 "command not found"

**原因**: Windows 主机上未安装 NVIDIA 驱动

**解决**:
1. 访问 [NVIDIA官网](https://www.nvidia.com/drivers) 下载最新驱动
2. 安装驱动并重启
3. 在 WSL2 中运行 `nvidia-smi` 验证

### Q2: CUDA 版本不匹配

**症状**: `CUDA version mismatch`

**解决**: 确保安装的是 CUDA 11.8:
```bash
sudo apt install -y cuda-11-8
nvcc --version  # 应显示 11.8
```

### Q3: MindSpore 找不到 GPU

**症状**: `Cannot find GPU device`

**检查步骤**:
```bash
# 1. 确认 GPU 可见
nvidia-smi

# 2. 检查 CUDA 环境变量
echo $LD_LIBRARY_PATH
echo $PATH

# 3. 重新设置环境变量
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/lib/wsl/lib:$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-11.8/bin:$PATH
```

### Q4: 训练速度慢

**可能原因**:
1. 项目文件在 Windows 文件系统(`/mnt/e/...`)而不是 WSL2 本地
2. batch_size 太小
3. GPU 未被充分利用

**解决方案**:
```bash
# 1. 复制项目到 WSL2 本地
cp -r /mnt/e/.../FER ~/FER

# 2. 增加 batch_size
--batch_size 96  # 或 128

# 3. 监控 GPU 使用率
watch -n 1 nvidia-smi
```

### Q5: 内存不足(OOM)

**症状**: `Out of Memory` 或 `CUDA out of memory`

**解决**:
```bash
# 减小 batch_size
--batch_size 64  # 或 32
```

### Q6: Windows 和 WSL2 之间如何传输文件?

```bash
# WSL2 访问 Windows 文件
cd /mnt/c/Users/...
cd /mnt/e/Users/...

# Windows 访问 WSL2 文件
# 在文件资源管理器输入:
\\wsl$\Ubuntu-22.04\home\username\
```

### Q7: 如何查看 GPU 使用率?

```bash
# 实时监控
watch -n 1 nvidia-smi

# 或单次查看
nvidia-smi
```

### Q8: WSL2 如何重启?

```powershell
# 在 Windows PowerShell 中
wsl --shutdown

# 然后重新进入
wsl
```

## 下一步

环境配置完成后:

1. 📖 阅读 [快速开始指南](quickstart.md) 开始训练
2. 🔧 查看 [模型优化说明](optimization.md) 了解优化技术
3. 📊 参考 [版本更新记录](changelog.md) 了解项目演进

## 参考资源

- [WSL2 官方文档](https://docs.microsoft.com/windows/wsl/)
- [MindSpore 官方文档](https://www.mindspore.cn/)
- [CUDA on WSL2](https://docs.nvidia.com/cuda/wsl-user-guide/)
- [Conda 官方文档](https://docs.conda.io/)

祝配置顺利! 🚀
