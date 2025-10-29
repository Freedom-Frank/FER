# FER2013 快速训练指南 - 50轮优化方案

## 目标
在50个epoch内训练出一个准确率达到65-70%的可用模型，确保模型文件完整且可用于可视化。

## 问题分析

### 当前问题
- `best_model.ckpt` 只有 434KB（不完整）
- `fer-5_449.ckpt` 有 1.3MB（完整且可用）
- 需要确保训练出的模型能正常保存和使用

## 训练方案

### 方案1: CPU训练（适合Windows，约10-20分钟/epoch）

#### 基础版（快速训练，预计准确率60-65%）
```bash
python src/train.py \
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 50 \
  --lr 5e-4 \
  --patience 15 \
  --save_dir checkpoints_50epoch
```

#### 优化版（数据增强，预计准确率65-68%）
```bash
python src/train.py \
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 50 \
  --lr 5e-4 \
  --patience 15 \
  --augment \
  --label_smoothing 0.1 \
  --save_dir checkpoints_50epoch
```

### 方案2: GPU训练（适合WSL2/Linux，约1-2分钟/epoch）

#### 推荐版（最佳性能，预计准确率68-72%）
```bash
python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 50 \
  --lr 7e-4 \
  --patience 15 \
  --augment \
  --mixup \
  --mixup_alpha 0.4 \
  --label_smoothing 0.12 \
  --weight_decay 3e-5 \
  --save_dir checkpoints_50epoch
```

#### 快速版（适中性能，预计准确率65-70%）
```bash
python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 50 \
  --lr 5e-4 \
  --patience 15 \
  --augment \
  --label_smoothing 0.1 \
  --save_dir checkpoints_50epoch
```

## 超参数说明

### 关键参数调整（50轮优化）

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `--epochs` | **50** | 训练轮数 |
| `--patience` | **15** | 早停耐心值（15轮不提升则停止） |
| `--lr` | **5e-4 到 7e-4** | 学习率（50轮适合用稍高一点的学习率） |
| `--batch_size` | CPU: **32**, GPU: **64-96** | 批次大小 |
| `--augment` | **推荐启用** | 数据增强（提升2-5%准确率） |
| `--mixup` | GPU推荐 | Mixup增强（GPU可用，提升3-5%） |
| `--label_smoothing` | **0.1-0.12** | 标签平滑（防止过拟合） |
| `--weight_decay` | **3e-5** | 权重衰减（正则化） |

### 时间预估

- **CPU训练**: 10-20分钟/epoch × 50轮 ≈ **8-16小时**
- **GPU训练**: 1-2分钟/epoch × 50轮 ≈ **50-100分钟**
- 实际可能更快（早停机制会在准确率不再提升时停止）

## 训练流程

### 第1步: 准备环境
```bash
# 检查环境
python -c "import mindspore; print('MindSpore:', mindspore.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"

# 确认数据集存在
# Windows
dir E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv

# WSL2
ls /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv
```

### 第2步: 开始训练
```bash
# 选择上面的一个方案运行
# 推荐GPU优化版（如果有GPU）或CPU优化版

# GPU训练（推荐）
python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 50 \
  --lr 7e-4 \
  --patience 15 \
  --augment \
  --mixup \
  --mixup_alpha 0.4 \
  --label_smoothing 0.12 \
  --weight_decay 3e-5 \
  --save_dir checkpoints_50epoch
```

### 第3步: 监控训练过程
训练时会输出：
```
Epoch 1/50 - Loss: 1.8234
Validation Accuracy: 0.3245
...
Epoch 25/50 - Loss: 0.6543
Validation Accuracy: 0.6821
New best accuracy: 0.6821 at epoch 25
...
```

### 第4步: 训练完成后检查模型
```bash
# 检查生成的模型文件
ls -lh checkpoints_50epoch/

# 应该看到类似这样的输出：
# -rw-r--r-- 1 user user 1.3M ... fer-50_449.ckpt
# -rw-r--r-- 1 user user 1.3M ... best_model.ckpt
```

**关键检查点**：
- 模型文件大小应该在 **1.2-1.5MB** 左右
- 如果文件小于500KB，说明模型未完整保存

### 第5步: 验证模型可用性
```bash
# 测试模型推理
python src/inference.py \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --image_path correct_samples/happy/correct_sample_1.png \
  --device_target CPU

# 应该输出类似：
# [INFO] Detected classifier shape: (256, 512)
# [INFO] Loading current model
# Prediction: happy Probability: 0.7523

# 检查概率是否合理（不是均匀分布的14.3%）
```

### 第6步: 生成可视化样例
```bash
# 使用新训练的模型生成样例
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3 \
  --output visualization_samples

# 单张图片可视化
python tools/demo_visualization.py \
  --mode image \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input correct_samples/happy/correct_sample_1.png
```

## 训练脚本（一键运行）

### Windows批处理脚本
创建文件 `train_50_epochs.bat`:
```batch
@echo off
echo Starting 50-epoch training...
echo.

python src/train.py ^
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv ^
  --device_target CPU ^
  --batch_size 32 ^
  --epochs 50 ^
  --lr 5e-4 ^
  --patience 15 ^
  --augment ^
  --label_smoothing 0.1 ^
  --save_dir checkpoints_50epoch

echo.
echo Training complete! Check checkpoints_50epoch/ for model files.
pause
```

运行：`train_50_epochs.bat`

### WSL2/Linux脚本
创建文件 `train_50_epochs.sh`:
```bash
#!/bin/bash
echo "Starting 50-epoch GPU training..."
echo

python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 50 \
  --lr 7e-4 \
  --patience 15 \
  --augment \
  --mixup \
  --mixup_alpha 0.4 \
  --label_smoothing 0.12 \
  --weight_decay 3e-5 \
  --save_dir checkpoints_50epoch

echo
echo "Training complete! Check checkpoints_50epoch/ for model files."
echo "Model file should be around 1.3MB"
ls -lh checkpoints_50epoch/
```

运行：`bash train_50_epochs.sh`

## 预期结果

### 训练结束后
- 模型文件：`checkpoints_50epoch/best_model.ckpt` ≈ **1.3MB**
- 准确率：**65-72%**（取决于使用的方案）
- 训练时间：
  - CPU: 8-16小时（可能因早停而更短）
  - GPU: 50-100分钟（可能因早停而更短）

### 验证模型质量
运行以下命令检查模型输出：
```bash
python src/inference.py \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --image_path test_image.jpg \
  --device_target CPU
```

**正常输出示例**：
```
Prediction: happy Probability: 0.8234
```

**异常输出示例**（说明模型有问题）：
```
Prediction: happy Probability: 0.1428  # 接近1/7，说明是随机预测
```

## 常见问题排查

### Q1: 训练中断了怎么办？
A: 训练脚本会自动保存checkpoint，可以继续训练：
```bash
# 暂不支持断点续训，需要重新开始
# 但中途保存的checkpoint可以直接使用
```

### Q2: 内存不足
A: 减小batch_size
```bash
# CPU: 32 → 16
# GPU: 96 → 64 → 32
```

### Q3: 准确率太低
A: 启用更多优化
```bash
--augment --mixup --label_smoothing 0.12
```

### Q4: 训练太慢
A:
- 使用GPU（速度提升5-10倍）
- 减小batch_size并减少augment
- 减少epochs到30

### Q5: 模型文件太小（<500KB）
A: 这是最关键的问题！
- 检查训练是否正常完成
- 查看训练日志中的Loss和Accuracy
- 如果Loss一直很高（>1.5）且不下降，可能是配置问题
- 尝试使用更简单的配置（不用mixup）

## 快速命令速查

### CPU训练（最简单）
```bash
python src/train.py --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv --device_target CPU --batch_size 32 --epochs 50 --lr 5e-4 --patience 15 --augment --save_dir checkpoints_50epoch
```

### GPU训练（推荐）
```bash
python src/train.py --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv --device_target GPU --batch_size 96 --epochs 50 --lr 7e-4 --patience 15 --augment --mixup --label_smoothing 0.12 --save_dir checkpoints_50epoch
```

### 验证模型
```bash
# 检查文件大小
ls -lh checkpoints_50epoch/best_model.ckpt

# 测试推理
python src/inference.py --ckpt_path checkpoints_50epoch/best_model.ckpt --image_path test.jpg --device_target CPU

# 生成可视化
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg
```

## 下一步

训练完成后，使用新模型进行可视化：

```bash
# 生成正确样例
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3

# 处理图片
python tools/demo_visualization.py \
  --mode image \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input your_image.jpg
```

现在你应该能看到正确的概率分布，而不是均匀的14.3%了！
