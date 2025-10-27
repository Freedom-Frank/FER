# FER2013 面部表情识别项目

基于 MindSpore 的面部表情识别系统,使用 FER2013 数据集训练深度学习模型识别 7 种面部表情。

---

## ⚡ 快速开始（3 步）

```bash
# 1. 进入项目目录
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER

# 2. 运行快速启动脚本（推荐）
./quick_start.sh

# 或者直接测试
./test_now.sh

# 3. 查看结果
ls output/images/
```

**快速导航：**
- [所有文档索引](DOCS_INDEX.md) - 完整文档导航
- [项目文件结构](PROJECT_STRUCTURE.md) - 文件组织说明
- [快速命令清单](COPY_PASTE_COMMANDS.txt) - 最常用的命令
- [可视化快速指南](VISUALIZATION_README.md) - 可视化功能使用
- [故障排除指南](QUICK_FIX.md) - 常见问题修复

---

## 项目特点

- **深度残差网络**: 采用 ResNet 架构,包含注意力机制(SENet + 空间注意力)
- **先进的数据增强**: Mixup、随机旋转、亮度调整、Cutout 等多种增强技术
- **优化的训练策略**: Warmup 学习率、AdamW 优化器、Label Smoothing
- **高准确率**: 经过多轮优化,验证集准确率可达 74-77%
- **跨平台支持**: Windows CPU 或 Linux/WSL2 GPU 训练

## 快速开始

### 环境要求

- Python 3.7+
- MindSpore 2.0+
- 其他依赖见 [requirements.txt](requirements.txt)

### 数据集准备

本项目使用 FER2013 数据集。由于数据集文件较大（287 MB），未包含在仓库中，需要手动下载：

1. **从 Kaggle 下载**：
   - 访问 [FER2013 数据集页面](https://www.kaggle.com/datasets/msambare/fer2013)
   - 下载 `fer2013.csv` 文件

2. **放置数据集**：
   ```bash
   # 创建数据目录（如果不存在）
   mkdir -p data/FER2013

   # 将下载的 fer2013.csv 放到此目录下
   # 最终路径应为: data/FER2013/fer2013.csv
   ```

3. **验证数据集**：
   ```bash
   # 确保文件存在
   ls data/FER2013/fer2013.csv
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 快速训练

```bash
# CPU 训练(Windows)
python src/train.py --data_csv data/FER2013/fer2013.csv --device_target CPU --batch_size 32 --epochs 50

# GPU 训练(Linux/WSL2)
python src/train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 96 --epochs 200 --augment --mixup
```

更多详情请参阅 [快速开始指南](docs/quickstart.md)。

## 文档导航

**快速参考：**
- [快速命令清单](COPY_PASTE_COMMANDS.txt) - 最常用命令（复制粘贴即用）
- [可视化快速指南](VISUALIZATION_README.md) - 5分钟上手可视化
- [故障排除](QUICK_FIX.md) - 模型加载错误修复
- [WSL配置问题](USBIP_FIX.md) - USBip错误说明

**详细文档：**
- [快速开始](docs/quickstart.md) - 完整入门教程
- [环境配置](docs/setup.md) - 详细环境配置步骤
- [可视化指南](docs/visualization_guide.md) - 可视化功能完整说明
- [模型优化](docs/optimization.md) - 模型优化技术详解
- [故障排除](docs/troubleshooting.md) - 常见问题解决方案
- [版本历史](docs/changelog.md) - 更新记录

## 项目结构

```
FER/
├── README.md                    # 项目主文档
├── requirements.txt             # Python 依赖
├── docs/                        # 文档目录
│   ├── quickstart.md           # 快速开始
│   ├── setup.md                # 环境配置
│   ├── optimization.md         # 优化说明
│   └── changelog.md            # 版本历史
├── src/                        # 源代码
│   ├── train.py                # 训练脚本
│   ├── eval.py                 # 评估脚本
│   ├── inference.py            # 推理脚本
│   ├── model.py                # 模型定义
│   └── dataset.py              # 数据加载
├── scripts/                    # 辅助脚本
│   ├── run_train.bat           # Windows 训练脚本
│   ├── quick_test.bat          # 快速测试脚本
│   └── wsl2_setup.sh           # WSL2 自动配置
├── data/                       # 数据目录
│   └── FER2013/
│       └── fer2013.csv         # 数据集文件
└── checkpoints/                # 模型检查点
```

## 表情类别

模型可识别 7 种基本面部表情:

0. Angry (生气)
1. Disgust (厌恶)
2. Fear (恐惧)
3. Happy (开心)
4. Sad (悲伤)
5. Surprise (惊讶)
6. Neutral (中性)

## 性能指标

| 版本 | 准确率 | 主要技术 |
|------|--------|----------|
| v1.0 | 66.91% | 基础 ResNet |
| v2.0 | 70.09% | + 注意力机制 + 数据增强 |
| v3.0 | 72-74% | + 超参数优化 |
| v4.0 | 74-77% | + Mixup 增强 |

## 硬件要求

### Windows (CPU)
- 最小: 4GB RAM, 10GB 磁盘空间
- 推荐: 8GB RAM, 20GB 磁盘空间
- 训练时间: ~20分钟/epoch

### Linux/WSL2 (GPU)
- NVIDIA GPU (推荐 RTX 3060 或更高)
- 6GB+ GPU 内存
- CUDA 11.6+
- 训练时间: ~1-2分钟/epoch

## 使用示例

### 训练模型

```bash
# 基础训练
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 100 \
  --augment

# 完整优化训练
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

### 评估模型

```bash
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints/final_model.ckpt \
  --device_target GPU
```

### 推理预测

```bash
python src/inference.py \
  --ckpt_path checkpoints/final_model.ckpt \
  --image_path your_image.jpg
```

### 可视化功能 (WSL/Linux)

```bash
# 方法 1: 使用快速启动脚本（推荐）
./quick_start.sh

# 方法 2: 直接运行命令
# 实时摄像头表情识别 (按 'q' 退出，按 's' 保存)
python demo_visualization.py --mode webcam --ckpt checkpoints/best.ckpt

# 处理单张图片（生成标注图和概率图）
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input test.jpg

# 处理视频文件
python demo_visualization.py --mode video --ckpt checkpoints/best.ckpt --input test.mp4

# 批量处理图片（生成统计报告）
python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input test_images/

# GPU 加速
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input test.jpg --device GPU
```

详细说明请参考 [完整文档](docs/visualization_guide.md)。

## 常见问题

### Q: Windows 下如何使用 GPU?
A: MindSpore 在 Windows 上仅支持 CPU。如需 GPU 加速,请使用 WSL2。详见 [环境配置指南](docs/setup.md#wsl2-gpu-配置)。

### Q: 训练速度慢怎么办?
A:
- 使用 GPU 训练(速度提升 5-10 倍)
- 增加 batch_size
- 减少数据增强强度

### Q: 如何提高准确率?
A:
- 启用数据增强 (`--augment`)
- 使用 Mixup (`--mixup`)
- 增加训练轮数
- 调整学习率和正则化参数

### Q: 内存不足怎么办?
A: 减小 batch_size (如从 96 降到 64 或 32)

## 贡献

欢迎提交 Issue 和 Pull Request!

## 许可证

MIT License

## 致谢

- [FER2013 数据集](https://www.kaggle.com/datasets/msambare/fer2013)
- [MindSpore 深度学习框架](https://www.mindspore.cn/)
- 参考论文:
  - SENet: Hu et al. "Squeeze-and-Excitation Networks" (CVPR 2018)
  - Mixup: Zhang et al. "mixup: Beyond Empirical Risk Minimization" (ICLR 2018)
  - Label Smoothing: Szegedy et al. "Rethinking the Inception Architecture" (CVPR 2016)

## 联系方式

如有问题或建议,欢迎通过 Issue 反馈。
