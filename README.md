# FER2013 面部表情识别项目

基于 MindSpore 的面部表情识别系统,使用 FER2013 数据集训练深度学习模型识别 7 种面部表情 (angry, disgust, fear, happy, sad, surprise, neutral)。

## 目录

- [项目特点](#项目特点)
- [快速开始](#快速开始)
- [技术架构](#技术架构)
- [文档导航](#文档导航)
- [项目结构](#项目结构)
- [表情类别](#表情类别)
- [性能指标](#性能指标)
- [硬件要求](#硬件要求)
- [核心脚本说明](#核心脚本说明)
- [常见问题](#常见问题-faq)
- [项目亮点与特性](#项目亮点与特性)
- [开发与贡献](#开发与贡献)
- [许可证](#许可证)
- [致谢](#致谢)

## 项目特点

- **深度残差网络**: 采用 ResNet 架构,包含注意力机制(SENet + 空间注意力)
- **先进的数据增强**: Mixup、随机旋转、亮度调整、对比度调整、高斯噪声、随机平移、Cutout 等多种增强技术
- **优化的训练策略**: Warmup 学习率、AdamW 优化器、Label Smoothing、早停机制
- **高准确率**: 经过多轮优化,验证集准确率可达 74-77%
- **跨平台支持**: Windows CPU 或 Linux/WSL2 GPU 训练
- **丰富的可视化功能**: 支持实时摄像头、图片、视频和批量处理

## 快速开始

### 环境要求

- **Python**: 3.7 或更高版本
- **MindSpore**: 2.0.0 或更高版本
- **操作系统**:
  - Windows 10/11 (仅支持 CPU)
  - Linux / WSL2 (支持 CPU 和 GPU)
- **其他依赖**:
  - numpy >= 1.21.0
  - pandas >= 1.3.0
  - opencv-python >= 4.5.0 (可视化功能需要)
  - scikit-learn >= 1.0.0
  - matplotlib >= 3.3.0 (可视化功能需要)
  - seaborn >= 0.11.0 (可视化功能需要)

完整依赖列表见 [requirements.txt](requirements.txt)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd FER
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **验证安装**
```bash
python -c "import mindspore; print(mindspore.__version__)"
python -c "import cv2; print(cv2.__version__)"
```

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

### 快速开始训练

**基础训练 (CPU, Windows):**
```bash
python src/train.py --data_csv data/FER2013/fer2013.csv --device_target CPU --batch_size 32 --epochs 50
```

**优化训练 (GPU, Linux/WSL2):**
```bash
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 200 \
  --augment \
  --mixup
```

训练过程中会自动:
- 保存每个 epoch 的检查点到 `checkpoints/` 目录
- 在验证集上评估性能
- 在验证准确率不再提升时提前停止 (早停机制)
- 输出最佳验证准确率和对应的 epoch

更多详情请参阅 [快速开始指南](docs/quickstart.md)。

## 技术架构

### 模型架构
- **网络结构**: 深度残差网络 (ResNet)
  - 初始卷积层: 64 个滤波器
  - 4 个残差层: 64 → 128 → 256 → 512 通道
  - 每层包含 2 个残差块
- **注意力机制**:
  - 通道注意力 (SENet): 使用全局平均池化和 FC 层生成通道权重
  - 空间注意力: 使用平均池化和最大池化生成空间权重
- **分类器**: 全连接层 (512 → 256 → 128 → 7) + BatchNorm + Dropout

### 数据增强策略
- **传统增强**: 水平翻转、随机旋转 (±20°)、亮度调整 (±30%)
- **高级增强**: 对比度调整、高斯噪声、随机平移 (±10%)、Cutout (15%)
- **Mixup**: 样本混合增强,alpha=0.4

### 训练优化
- **优化器**: AdamWeightDecay (权重衰减 3e-5)
- **学习率调度**: Warmup (5 epochs) + Cosine Decay
- **损失函数**:
  - 标准训练: Label Smoothing Cross Entropy (smoothing=0.12)
  - Mixup 训练: Soft Target Cross Entropy
- **早停机制**: Patience=30, min_delta=0.001
- **正则化**: Dropout (0.5, 0.3)、BatchNorm、权重衰减

## 文档导航

### 快速参考
- [命令速查表](COPY_PASTE_COMMANDS.txt) - 最常用命令（复制粘贴即用）
- [可视化快速参考](docs/quick-reference/visualization.md) - 可视化命令清单

### 核心文档
- [快速开始](docs/quickstart.md) - 完整入门教程
- [环境配置](docs/setup.md) - 详细环境配置步骤
- [入门指南](docs/getting_started.md) - 初学者指南
- [可视化指南](docs/visualization_guide.md) - 可视化功能完整说明
- [可视化环境配置](docs/visualization_setup.md) - 可视化依赖安装

### 进阶文档
- [模型优化](docs/optimization.md) - 模型优化技术详解
- [模型兼容性](docs/model_compatibility.md) - 新旧模型版本说明
- [故障排除](docs/troubleshooting.md) - 常见问题解决方案
- [版本历史](docs/changelog.md) - 更新记录

### 示例与参考
- [可视化示例](examples/visualization_examples.md) - 可视化使用示例
- [文档索引](docs/README.md) - 完整文档列表

## 项目结构

```
FER/
├── README.md                       # 项目主文档
├── requirements.txt                # Python 依赖
├── demo_visualization.py           # 可视化演示脚本
├── COPY_PASTE_COMMANDS.txt         # 常用命令快速参考
├── src/                           # 源代码目录
│   ├── train.py                   # 训练脚本
│   ├── eval.py                    # 评估脚本
│   ├── inference.py               # 推理脚本
│   ├── model.py                   # 模型定义(ResNet + 注意力机制)
│   ├── model_legacy.py            # 旧版模型定义(兼容)
│   ├── dataset.py                 # 数据加载与增强
│   └── visualize.py               # 可视化工具类
├── scripts/                       # 辅助脚本
│   ├── run_train.bat              # Windows 训练脚本
│   ├── quick_test.bat             # 快速测试脚本
│   ├── wsl2_setup.sh              # WSL2 自动配置
│   ├── download_wsl_simple.ps1    # WSL 数据集下载脚本
│   ├── download_ubuntu.ps1        # Ubuntu 数据集下载脚本
│   ├── install_wsl2.ps1           # WSL2 安装脚本
│   └── test_visualization.sh      # 可视化测试脚本
├── docs/                          # 文档目录
│   ├── quickstart.md              # 快速开始
│   ├── setup.md                   # 环境配置
│   ├── optimization.md            # 优化说明
│   ├── changelog.md               # 版本历史
│   ├── visualization_guide.md     # 可视化指南
│   ├── visualization_setup.md     # 可视化环境配置
│   ├── model_compatibility.md     # 模型兼容性说明
│   ├── troubleshooting.md         # 故障排除
│   ├── getting_started.md         # 入门指南
│   ├── README.md                  # 文档索引
│   └── quick-reference/           # 快速参考目录
│       ├── visualization.md       # 可视化快速参考
│       └── commands.txt           # 命令清单
├── examples/                      # 示例文件
│   └── visualization_examples.md  # 可视化使用示例
├── data/                          # 数据目录
│   └── FER2013/
│       └── fer2013.csv            # 数据集文件(需手动下载)
├── checkpoints/                   # 模型检查点目录
│   ├── best_model.ckpt            # 最佳模型
│   └── fer-*.ckpt                 # 训练检查点
├── output/                        # 输出目录
│   ├── images/                    # 图片处理结果
│   ├── videos/                    # 视频处理结果
│   ├── webcam/                    # 摄像头截图
│   └── batch/                     # 批量处理结果
└── rank_0/                        # MindSpore 运行时输出
    └── om/                        # 模型编译输出
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

## 核心脚本说明

### 1. 训练脚本 (src/train.py)

训练面部表情识别模型,支持多种优化策略。

**主要参数:**
- `--data_csv`: FER2013 数据集路径 (必需)
- `--device_target`: 计算设备 [CPU, GPU, Ascend]
- `--batch_size`: 批次大小 (默认: 96)
- `--epochs`: 训练轮数 (默认: 200)
- `--lr`: 初始学习率 (默认: 7e-4)
- `--augment`: 启用数据增强
- `--mixup`: 启用 Mixup 增强
- `--mixup_alpha`: Mixup alpha 参数 (默认: 0.4)
- `--label_smoothing`: 标签平滑因子 (默认: 0.12)
- `--weight_decay`: 权重衰减 (默认: 3e-5)
- `--patience`: 早停耐心值 (默认: 30)
- `--save_dir`: 检查点保存目录 (默认: checkpoints)

**使用示例:**
```bash
# 基础训练
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 100 \
  --augment

# 完整优化训练 (推荐)
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

### 2. 评估脚本 (src/eval.py)

在测试集上评估训练好的模型,输出详细的分类报告和混淆矩阵。

**主要参数:**
- `--data_csv`: FER2013 数据集路径 (必需)
- `--ckpt_path`: 模型检查点路径 (必需)
- `--device_target`: 计算设备 [CPU, GPU, Ascend]
- `--batch_size`: 批次大小 (默认: 64)

**使用示例:**
```bash
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints/best_model.ckpt \
  --device_target GPU
```

**输出内容:**
- 每个表情类别的精确率、召回率、F1-score
- 整体准确率
- 混淆矩阵

### 3. 推理脚本 (src/inference.py)

对单张图片进行表情识别,支持自动模型版本检测。

**主要参数:**
- `--image_path`: 输入图片路径 (必需)
- `--ckpt_path`: 模型检查点路径 (必需)
- `--device_target`: 计算设备 [CPU, GPU, Ascend]

**使用示例:**
```bash
python src/inference.py \
  --ckpt_path checkpoints/best_model.ckpt \
  --image_path your_image.jpg \
  --device_target CPU
```

**输出示例:**
```
[INFO] Detected classifier shape: (256, 512)
[INFO] Loading current model
Prediction: happy Probability: 0.8523
```

### 4. 可视化演示脚本 (demo_visualization.py)

提供完整的可视化功能,支持实时摄像头、图片、视频和批量处理。(需要 OpenCV 和可视化相关依赖)

**主要参数:**
- `--mode`: 运行模式 [webcam, image, video, batch, menu] (必需)
- `--ckpt`: 模型检查点路径 (必需)
- `--input`: 输入文件/目录路径 (根据模式而定)
- `--device`: 计算设备 [CPU, GPU] (默认: CPU)

**使用示例:**

#### 实时摄像头识别
```bash
python demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt
```
- 按 `q` 退出
- 按 `s` 保存当前帧到 `output/webcam/`

#### 单张图片处理
```bash
python demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input test.jpg
```
生成两个文件:
- `*_annotated.jpg`: 带表情标注和置信度的图片
- `*_result.png`: 7种表情的概率分布柱状图

#### 视频文件处理
```bash
python demo_visualization.py --mode video --ckpt checkpoints/best_model.ckpt --input test.mp4
```
生成带实时表情识别标注的视频文件,保存到 `output/videos/`

#### 批量图片处理
```bash
python demo_visualization.py --mode batch --ckpt checkpoints/best_model.ckpt --input test_images/
```
处理目录中的所有图片,并生成:
- 每张图片的标注结果
- `statistics.png`: 所有图片的表情分布统计图

#### GPU 加速
```bash
python demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input test.jpg --device GPU
```

详细说明请参考 [可视化指南](docs/visualization_guide.md)。

## 常见问题 (FAQ)

### Q: Windows 下如何使用 GPU?
**A:** MindSpore 在 Windows 上仅支持 CPU。如需 GPU 加速,请使用 WSL2。详见 [环境配置指南](docs/setup.md)。

推荐配置流程:
1. 安装 WSL2
2. 在 WSL2 中安装 CUDA
3. 安装 MindSpore GPU 版本
4. 使用项目提供的 `scripts/wsl2_setup.sh` 自动配置

### Q: 训练速度慢怎么办?
**A:** 多种优化方法:
- **使用 GPU 训练**: 速度提升 5-10 倍
- **增加 batch_size**: 在显存允许的情况下,如 64 → 96
- **减少数据增强**: 如果不需要最高准确率,可禁用 `--augment` 或 `--mixup`
- **减少训练轮数**: 使用早停机制,通常 50-100 轮即可达到不错效果

### Q: 如何提高准确率?
**A:** 优化策略:
- **启用数据增强**: `--augment`
- **使用 Mixup**: `--mixup --mixup_alpha 0.4`
- **增加训练轮数**: `--epochs 200`
- **调整超参数**:
  - 学习率: `--lr 7e-4`
  - 标签平滑: `--label_smoothing 0.12`
  - 权重衰减: `--weight_decay 3e-5`
- **使用完整的优化训练命令** (见上方"核心脚本说明")

### Q: 内存不足怎么办?
**A:** 减小资源占用:
- 减小 `batch_size`: 96 → 64 → 32
- 减少数据增强: 禁用 `--mixup`
- 使用 CPU 训练: `--device_target CPU`

### Q: 模型加载失败怎么办?
**A:** 项目支持新旧两个版本的模型:
- **自动检测**: `src/inference.py` 会自动检测模型版本
- **手动指定**: 如果遇到兼容性问题,查看 [模型兼容性文档](docs/model_compatibility.md)
- **重新训练**: 使用最新代码重新训练模型

### Q: 可视化功能无法使用?
**A:** 检查依赖:
```bash
pip install opencv-python matplotlib seaborn
```
如果是 WSL2 环境,还需要配置 X11 转发或使用 WSLg。详见 [可视化环境配置](docs/visualization_setup.md)。

### Q: 如何在自己的数据集上训练?
**A:** 数据集格式要求:
1. 准备 CSV 文件,包含以下列:
   - `emotion`: 表情标签 (0-6)
   - `pixels`: 48x48 灰度图像的像素值 (空格分隔)
   - `Usage`: 数据用途 (Training/PublicTest/PrivateTest)
2. 使用相同的训练命令,修改 `--data_csv` 路径即可

## 项目亮点与特性

### 模型特性
- ✅ **深度残差网络**: 基于 ResNet 架构,包含 4 个残差层,每层 2 个残差块
- ✅ **双重注意力机制**: 结合通道注意力(SENet)和空间注意力,提升特征提取能力
- ✅ **自动模型版本检测**: 兼容新旧版本模型,自动加载正确的架构
- ✅ **全局平均池化**: 减少参数量,提升泛化能力

### 数据增强
- ✅ **传统增强**: 水平翻转、随机旋转、亮度调整
- ✅ **高级增强**: 对比度调整、高斯噪声、随机平移、Cutout
- ✅ **Mixup 增强**: 样本级混合,有效提升模型鲁棒性
- ✅ **软标签支持**: 配合 Mixup 使用,提升训练效果

### 训练优化
- ✅ **智能学习率调度**: Warmup + Cosine Decay
- ✅ **AdamW 优化器**: 解耦权重衰减,更好的泛化性能
- ✅ **Label Smoothing**: 防止过拟合,提升泛化能力
- ✅ **早停机制**: 自动停止训练,节省时间和资源
- ✅ **自动检查点保存**: 保存最佳模型和定期检查点
- ✅ **实时验证评估**: 每个 epoch 自动在验证集上评估

### 可视化功能
- ✅ **实时摄像头识别**: 支持 webcam 实时表情检测
- ✅ **图片处理**: 生成标注图和概率分布图
- ✅ **视频处理**: 处理视频文件,生成带标注的输出
- ✅ **批量处理**: 处理多张图片,生成统计报告
- ✅ **多种输出格式**: 支持图片标注、概率图、统计图等

### 工程特性
- ✅ **跨平台支持**: Windows(CPU)、Linux(CPU/GPU)、WSL2(GPU)
- ✅ **完善的文档**: 包含快速开始、详细配置、故障排除等
- ✅ **辅助脚本**: 提供一键配置、快速测试等脚本
- ✅ **详细的代码注释**: 代码易读易懂,便于学习和修改

## 开发与贡献

### 项目开发
如果你想基于此项目进行开发或修改:

1. **Fork 项目**
2. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **进行修改并测试**
4. **提交更改**
   ```bash
   git commit -m "Add your feature"
   ```
5. **推送到分支**
   ```bash
   git push origin feature/your-feature
   ```
6. **创建 Pull Request**

### 代码结构说明
- `src/model.py`: 包含模型定义,可修改网络结构
- `src/dataset.py`: 数据加载和增强,可添加新的增强方法
- `src/train.py`: 训练流程,可调整训练策略
- `src/visualize.py`: 可视化工具类,可扩展新功能

### 贡献指南
欢迎以下类型的贡献:
- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 修复问题
- ✨ 添加新功能

提交 Issue 或 Pull Request 时,请提供详细的描述和复现步骤(如果适用)。

## 许可证

MIT License

本项目采用 MIT 许可证,您可以自由使用、修改和分发本项目,但需保留原作者信息和许可证声明。

## 致谢

- [FER2013 数据集](https://www.kaggle.com/datasets/msambare/fer2013)
- [MindSpore 深度学习框架](https://www.mindspore.cn/)
- 参考论文:
  - SENet: Hu et al. "Squeeze-and-Excitation Networks" (CVPR 2018)
  - Mixup: Zhang et al. "mixup: Beyond Empirical Risk Minimization" (ICLR 2018)
  - Label Smoothing: Szegedy et al. "Rethinking the Inception Architecture" (CVPR 2016)

## 联系方式

如有问题或建议,欢迎通过 Issue 反馈。
