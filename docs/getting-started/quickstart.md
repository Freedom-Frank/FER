# 快速开始指南

本指南将帮助你快速开始使用 FER2013 面部表情识别项目。

## 目录

- [安装环境](#安装环境)
- [准备数据](#准备数据)
- [快速训练](#快速训练)
- [模型评估](#模型评估)
- [推理预测](#推理预测)
- [下一步](#下一步)

## 安装环境

### Windows (CPU)

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 验证安装
python -c "import mindspore; print('MindSpore version:', mindspore.__version__)"
```

### Linux/WSL2 (GPU)

如果需要GPU加速,请参考 [环境配置指南](setup.md#wsl2-gpu-配置)。

## 准备数据

确保 FER2013 数据集已放置在正确位置:

```
data/FER2013/fer2013.csv
```

数据集可以从 [Kaggle](https://www.kaggle.com/datasets/msambare/fer2013) 下载。

## 快速训练

### 方案 A: CPU 训练(快速测试)

适合快速验证代码是否正常工作。

```bash
# 快速测试(2个epoch)
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 2 \
  --augment

# 完整训练(50个epoch)
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 50 \
  --augment
```

**预计时间**: 每个 epoch 约 15-20 分钟

### 方案 B: GPU 训练(推荐)

速度快 5-10 倍,适合完整训练。

```bash
# 快速测试(2个epoch)
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 2 \
  --augment

# 完整优化训练(200个epoch)
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

**预计时间**: 每个 epoch 约 1-2 分钟

### 使用 Windows 批处理脚本

```bash
# 运行预配置的训练脚本
scripts\run_train.bat
```

## 训练参数说明

| 参数 | 说明 | 默认值 | 推荐值 |
|------|------|--------|--------|
| `--data_csv` | 数据集路径 | 必需 | - |
| `--device_target` | 设备类型 | CPU | GPU(如可用) |
| `--batch_size` | 批次大小 | 64 | CPU:32, GPU:96 |
| `--epochs` | 训练轮数 | 100 | 测试:2-10, 完整:200 |
| `--lr` | 学习率 | 1e-3 | 7e-4 |
| `--patience` | 早停耐心值 | 15 | 30 |
| `--augment` | 数据增强 | False | True(推荐) |
| `--mixup` | Mixup增强 | False | True(高级) |
| `--mixup_alpha` | Mixup强度 | 0.2 | 0.4 |

## 训练输出示例

```
============================================================
Training Configuration:
  Device: GPU
  Batch size: 96
  Epochs: 200
  Learning rate: 0.0007
  Data augmentation: True
  Mixup: True (alpha=0.4)
============================================================

Loading datasets...
Training batches: 374
Validation batches: 37

Building model...

Starting training...
============================================================
epoch: 1 step: 374, loss is 1.8245
Epoch 1 - Validation Accuracy: 0.4821

epoch: 2 step: 374, loss is 1.7123
Epoch 2 - Validation Accuracy: 0.5234
...
epoch: 85 step: 374, loss is 0.9234
Epoch 85 - Validation Accuracy: 0.7589  <- Best!

Early stopping triggered!
Best validation accuracy: 0.7589 at epoch 85
============================================================
```

## 模型评估

训练完成后,评估模型性能:

```bash
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints/final_model.ckpt \
  --device_target GPU
```

输出示例:

```
Loading model from checkpoints/final_model.ckpt
Evaluating on test set...
Test Accuracy: 75.89%

Per-class accuracy:
  Angry: 72.3%
  Disgust: 68.5%
  Fear: 71.2%
  Happy: 86.4%
  Sad: 73.8%
  Surprise: 81.2%
  Neutral: 77.9%
```

## 推理预测

使用训练好的模型对单张图片进行预测:

```bash
python src/inference.py \
  --ckpt_path checkpoints/final_model.ckpt \
  --image_path path/to/your/image.jpg
```

输出示例:

```
Loading model from checkpoints/final_model.ckpt
Processing image: path/to/your/image.jpg

Prediction Results:
  Predicted emotion: Happy (3)
  Confidence: 92.45%

All probabilities:
  Angry: 1.2%
  Disgust: 0.3%
  Fear: 2.1%
  Happy: 92.5%
  Sad: 1.5%
  Surprise: 1.8%
  Neutral: 0.6%
```

## 性能对比

| 配置 | 训练时间/epoch | 100 epochs 总时间 | 预期准确率 |
|------|---------------|------------------|-----------|
| **CPU** | 15-20分钟 | 25-33小时 | ~66-70% |
| **GPU** | 1-2分钟 | 2-3小时 | ~74-77% |

## 常见问题

### Q1: 如何查看GPU使用情况?

```bash
# Linux/WSL2
watch -n 1 nvidia-smi

# 或在训练的另一个终端运行
nvidia-smi
```

### Q2: 训练中断如何恢复?

模型会自动保存最佳 checkpoint 到 `checkpoints/` 目录。如果训练中断,可以从最新的 checkpoint 继续训练(需要修改训练脚本添加加载 checkpoint 的代码)。

### Q3: 如何调整模型以适应内存限制?

减小 `batch_size`:
```bash
# 从 96 降到 64
--batch_size 64

# 或降到 32
--batch_size 32
```

### Q4: 如何提高训练速度?

1. 使用 GPU 训练
2. 增加 `batch_size` (如果内存允许)
3. 减少数据增强(去掉 `--augment` 或 `--mixup`)
4. 使用更少的训练轮数

### Q5: 准确率不理想怎么办?

1. 确保启用数据增强: `--augment`
2. 使用 Mixup: `--mixup --mixup_alpha 0.4`
3. 增加训练轮数: `--epochs 200`
4. 调整学习率: `--lr 7e-4`
5. 参考 [模型优化说明](optimization.md) 进行深入优化

## 下一步

- 📖 阅读 [环境配置指南](setup.md) 了解详细的环境配置
- 🔧 查看 [模型优化说明](optimization.md) 了解模型优化技术
- 📊 参考 [版本更新记录](changelog.md) 了解各版本改进

## 推荐工作流程

1. **首次运行**: CPU 快速测试(2 epochs)验证环境
2. **环境配置**: 配置 WSL2 GPU 环境(一次性工作)
3. **初步训练**: GPU 中等训练(50 epochs)
4. **完整训练**: GPU 完整训练(200 epochs,启用所有优化)
5. **模型调优**: 根据结果调整超参数

祝训练顺利! 🎉
