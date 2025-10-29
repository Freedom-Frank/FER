# FER2013 完整工作流程 - 从头到尾的所有命令

## 目录
1. [环境准备](#1-环境准备)
2. [问题诊断](#2-问题诊断可选)
3. [清理旧模型](#3-清理旧模型)
4. [训练新模型](#4-训练新模型50轮)
5. [验证模型](#5-验证模型)
6. [可视化使用](#6-可视化使用)
7. [故障排除](#7-故障排除)

---

## 1. 环境准备

### 进入项目目录

```bash
# Windows CMD
cd /d E:\Users\Meng\Projects\VScodeProjects\FER

# Windows PowerShell
cd E:\Users\Meng\Projects\VScodeProjects\FER

# WSL2/Linux
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER

# 确认当前目录
pwd
# 应该输出: /mnt/e/Users/Meng/Projects/VScodeProjects/FER (WSL2)
# 或: E:\Users\Meng\Projects\VScodeProjects\FER (Windows)
```

### 检查环境
```bash
# 检查Python和依赖
python --version                    # 应该是Python 3.7+
python -c "import mindspore; print('MindSpore:', mindspore.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"

# 如果缺少依赖，安装
pip install -r requirements.txt
```

### 检查数据集
```bash
# Windows
dir E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv

# WSL2/Linux
ls -lh /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv

# 应该看到文件大小约 287 MB
```

### 检查项目结构
```bash
# 确认关键文件存在
ls -l src/train.py
ls -l src/inference.py
ls -l tools/generate_correct_samples.py
ls -l tools/demo_visualization.py
```

---

## 2. 问题诊断（可选）

### 检查现有模型问题
```bash
# 查看现有模型大小
ls -lh checkpoints/*.ckpt

# 应该看到类似：
# best_model.ckpt    434K   ← 问题模型（太小）
# fer-5_449.ckpt     1.3M   ← 可用但不是最佳

# 验证问题模型
python verify_model.py --ckpt checkpoints/best_model.ckpt --device CPU

# 会显示：概率分布接近均匀（14.3%），模型未训练
```

---

## 3. 清理旧模型

### 备份现有checkpoints（推荐）
```bash
# 创建备份目录
mkdir -p checkpoints_backup

# Windows
xcopy checkpoints checkpoints_backup /E /I

# Linux/WSL2
cp -r checkpoints checkpoints_backup
```

### 删除问题模型
```bash
# 删除有问题的 best_model.ckpt
rm checkpoints/best_model.ckpt

# 或者移动到备份
mv checkpoints/best_model.ckpt checkpoints_backup/
```

---

## 4. 训练新模型（50轮）

### 选项A: WSL2/Linux GPU训练（推荐，50-100分钟）

#### 方法1: 使用一键脚本（最简单）
```bash
# 赋予执行权限
chmod +x train_50_epochs.sh

# 执行训练
bash train_50_epochs.sh
```

#### 方法2: 手动命令（完整控制）
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

**预期输出**：
```
============================================================
Training Configuration:
  Device: GPU
  Batch size: 96
  Epochs: 50
  Learning rate: 7e-4
  Data augmentation: True
============================================================

Loading datasets...
Training batches: 449
Validation batches: 56

Building model...
Using Soft Target Cross Entropy for Mixup (alpha=0.4)

Starting training...
============================================================

Epoch 1/50 - Loss: 1.8234
Validation Accuracy: 0.3245

Epoch 2/50 - Loss: 1.5432
Validation Accuracy: 0.4123

...

Epoch 25/50 - Loss: 0.6543
Validation Accuracy: 0.6821
New best accuracy: 0.6821 at epoch 25
Saved best model to: checkpoints_50epoch/best_model.ckpt  ← 关键！

...

Training finished!
Best validation accuracy: 0.6821 at epoch 25
```

---

### 选项B: Windows CPU训练（8-16小时）

#### 方法1: 使用一键脚本（最简单）
```bash
# 双击运行
train_50_epochs.bat
```

#### 方法2: 手动命令
```bash
python src/train.py ^
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv ^
  --device_target CPU ^
  --batch_size 32 ^
  --epochs 50 ^
  --lr 5e-4 ^
  --patience 15 ^
  --augment ^
  --label_smoothing 0.1 ^
  --weight_decay 3e-5 ^
  --save_dir checkpoints_50epoch
```

#### PowerShell版本（如果上面的不行）
```powershell
python src/train.py `
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv `
  --device_target CPU `
  --batch_size 32 `
  --epochs 50 `
  --lr 5e-4 `
  --patience 15 `
  --augment `
  --label_smoothing 0.1 `
  --weight_decay 3e-5 `
  --save_dir checkpoints_50epoch
```

---

### 选项C: 快速测试训练（5轮，用于测试）

```bash
# GPU
python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 5 \
  --lr 5e-4 \
  --save_dir test_training

# CPU
python src/train.py \
  --data_csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv \
  --device_target CPU \
  --batch_size 32 \
  --epochs 5 \
  --lr 5e-4 \
  --save_dir test_training
```

---

## 5. 验证模型

### 5.1 检查模型文件
```bash
# 列出生成的模型
ls -lh checkpoints_50epoch/

# 应该看到：
# best_model.ckpt     1.3M  ← 最佳模型（准确率最高）
# fer-50_449.ckpt     1.3M  ← 第50轮的模型
# fer-49_449.ckpt     1.3M  ← 第49轮的模型
# ...
# final_model.ckpt    1.3M  ← 最终模型

# 关键检查：best_model.ckpt 应该约1.3MB
```

### 5.2 验证模型可用性
```bash
# 运行验证工具
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt --device CPU

# 预期输出（正常）：
# ============================================================
# Step 1: Checking Model File
# ============================================================
# Model file: checkpoints_50epoch/best_model.ckpt
# File size: 1.31 MB
# ✓ File size looks good (1.31 MB)
#
# ============================================================
# Step 2: Loading Model
# ============================================================
# [INFO] Detected classifier shape: (256, 512)
# [INFO] Loading current model
# ✓ Model loaded successfully
#
# ============================================================
# Step 3: Testing Random Inference
# ============================================================
# Prediction probabilities:
#   angry      18.2% #########
#   disgust     9.1% ####
#   fear       12.3% ######
#   happy      32.4% ################
#   sad        11.2% #####
#   surprise   10.5% #####
#   neutral     6.3% ###
#
# ✓ Model produces non-uniform predictions
#   Predicted: happy (32.4%)
#
# ============================================================
# VERDICT: Model appears to be WORKING! ✓
# ============================================================
```

### 5.3 测试单张图片推理
```bash
# 如果有测试图片
python src/inference.py \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --image_path correct_samples/happy/correct_sample_1.png \
  --device_target CPU

# 预期输出（正常）：
# [INFO] Detected classifier shape: (256, 512)
# [INFO] Loading current model
# Prediction: happy Probability: 0.7823

# 注意：概率应该在 0.3-0.9 之间，不应该是 0.14 左右
```

---

## 6. 可视化使用

### 6.1 生成正确的样例展示

#### 基础版（每种情绪3个样例）
```bash
# WSL2/Linux
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3 \
  --output visualization_samples

# Windows
python tools/generate_correct_samples.py --csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv --ckpt checkpoints_50epoch\best_model.ckpt --num_samples 3 --output visualization_samples
```

#### GPU加速版
```bash
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --device GPU \
  --num_samples 3 \
  --output visualization_samples
```

**预期输出**：
```
============================================================
Generating CORRECT prediction samples only
============================================================

============================================================
Processing: Happy (happy)
Target: 3 correct samples
============================================================
Available samples in dataset: 895

Generating sample 1/3...
  ✓ Found correct sample after 12 attempts! (confidence: 78.2%)
  Saved: visualization_samples/happy/correct_sample_1.png

Generating sample 2/3...
  ✓ Found correct sample after 8 attempts! (confidence: 82.4%)
  Saved: visualization_samples/happy/correct_sample_2.png

...

============================================================
Generation Complete!
============================================================

Statistics:
  Total correct samples generated: 21
  Total attempts needed: 234
  Average attempts per sample: 11.1

Output directory: visualization_samples/
```

---

### 6.2 单张图片可视化

```bash
# WSL2/Linux
python tools/demo_visualization.py \
  --mode image \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test.jpg

# Windows
python tools\demo_visualization.py --mode image --ckpt checkpoints_50epoch\best_model.ckpt --input test.jpg
```

**生成文件**：
- `output/images/test_annotated.jpg` - 标注图
- `output/images/test_result.png` - 概率分布图

---

### 6.3 批量图片处理

```bash
# 准备图片目录
mkdir test_images
# 放入一些测试图片...

# 批量处理
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test_images/

# 生成文件：
# - output/batch/*_result.jpg - 每张图的结果
# - output/batch/statistics.png - 统计图表
```

---

### 6.4 实时摄像头识别（需要摄像头）

```bash
python tools/demo_visualization.py \
  --mode webcam \
  --ckpt checkpoints_50epoch/best_model.ckpt

# 按 'q' 退出
# 按 's' 保存当前帧
```

---

### 6.5 视频处理

```bash
python tools/demo_visualization.py \
  --mode video \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test_video.mp4

# 生成标注后的视频
```

---

## 7. 故障排除

### 问题1: ModuleNotFoundError: No module named 'inference'

**解决方案**：
```bash
# 已修复，确保使用最新代码
git pull  # 如果使用git

# 或者手动检查 tools/ 下的文件是否包含：
# script_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(script_dir)
# sys.path.insert(0, os.path.join(project_root, 'src'))
```

---

### 问题2: 训练时内存不足

**解决方案**：
```bash
# 减小 batch_size
# GPU: 96 → 64 → 32
# CPU: 32 → 16

python src/train.py \
  --data_csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --device_target GPU \
  --batch_size 64 \
  --epochs 50 \
  --lr 7e-4 \
  --patience 15 \
  --augment \
  --save_dir checkpoints_50epoch
```

---

### 问题3: 生成样例找不到正确预测

**解决方案**：
```bash
# 增加尝试次数
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3 \
  --max_attempts 5000

# 或使用训练集（样本更多）
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3 \
  --usage Training
```

---

### 问题4: 模型预测概率仍然均匀（14.3%）

**诊断**：
```bash
# 检查模型文件大小
ls -lh checkpoints_50epoch/best_model.ckpt

# 如果小于1MB，模型有问题
# 检查训练日志：
# - Loss 是否下降？
# - Accuracy 是否提升？
# - 是否看到 "Saved best model to..." 消息？
```

**解决方案**：
```bash
# 重新训练，确保使用修复后的代码
# 监控训练过程，确保看到：
# "Saved best model to: checkpoints_50epoch/best_model.ckpt"
```

---

### 问题5: 训练中断了

**解决方案**：
```bash
# 检查已保存的checkpoint
ls -lh checkpoints_50epoch/

# 使用最新的epoch checkpoint
python verify_model.py --ckpt checkpoints_50epoch/fer-45_449.ckpt

# 如果验证通过，可以直接使用
# 或者重新开始训练（暂不支持断点续训）
```

---

## 8. 完整工作流程示例（从头到尾）

### GPU训练完整流程（推荐）

```bash
# 0. 进入项目目录
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER

# 1. 环境检查
python -c "import mindspore; print('MindSpore:', mindspore.__version__)"
ls /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv

# 2. 清理旧模型
mkdir -p checkpoints_backup
mv checkpoints/best_model.ckpt checkpoints_backup/ 2>/dev/null || true

# 3. 开始训练（50-100分钟）
bash train_50_epochs.sh

# 4. 验证模型
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt --device CPU

# 5. 生成可视化样例
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --device GPU \
  --num_samples 3 \
  --output visualization_samples

# 6. 查看结果
ls -R visualization_samples/
```

---

### CPU训练完整流程

```bash
# 0. 进入项目目录
cd /d E:\Users\Meng\Projects\VScodeProjects\FER

# 1. 环境检查
python -c "import mindspore; print('MindSpore:', mindspore.__version__)"
dir E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv

# 2. 清理旧模型
mkdir checkpoints_backup
move checkpoints\best_model.ckpt checkpoints_backup\

# 3. 开始训练（8-16小时）
train_50_epochs.bat

# 4. 验证模型
python verify_model.py --ckpt checkpoints_50epoch\best_model.ckpt --device CPU

# 5. 生成可视化样例
python tools\generate_correct_samples.py --csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv --ckpt checkpoints_50epoch\best_model.ckpt --num_samples 3 --output visualization_samples

# 6. 查看结果
dir visualization_samples\ /s
```

---

## 9. 快速命令参考

### 训练命令
```bash
# GPU快速（推荐）
bash train_50_epochs.sh

# CPU快速
train_50_epochs.bat

# 自定义训练
python src/train.py --data_csv <path> --device_target <CPU|GPU> --batch_size <32|96> --epochs 50 --lr <5e-4|7e-4> --patience 15 --augment --save_dir checkpoints_50epoch
```

### 验证命令
```bash
# 验证模型
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt --device CPU

# 测试推理
python src/inference.py --ckpt_path checkpoints_50epoch/best_model.ckpt --image_path test.jpg --device_target CPU
```

### 可视化命令
```bash
# 生成样例
python tools/generate_correct_samples.py --csv <csv_path> --ckpt checkpoints_50epoch/best_model.ckpt --num_samples 3 --output visualization_samples

# 单图处理
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg

# 批量处理
python tools/demo_visualization.py --mode batch --ckpt checkpoints_50epoch/best_model.ckpt --input test_images/
```

---

## 10. 预期结果

### 训练完成后
- ✓ 模型文件：`checkpoints_50epoch/best_model.ckpt` ≈ 1.3MB
- ✓ 准确率：65-72%
- ✓ 训练时间：GPU 50-100分钟，CPU 8-16小时

### 验证结果
- ✓ 文件大小检查通过
- ✓ 模型加载成功
- ✓ 预测概率非均匀（某个类别明显更高）

### 可视化结果
- ✓ 生成正确的样例展示
- ✓ 概率分布图显示合理（不是14.3%均匀分布）
- ✓ 预测置信度在30-90%之间

---

## 需要帮助？

1. **查看详细文档**：
   - [TRAINING_GUIDE_50_EPOCHS.md](TRAINING_GUIDE_50_EPOCHS.md)
   - [MODEL_SAVE_FIX.md](MODEL_SAVE_FIX.md)

2. **运行诊断工具**：
   ```bash
   python verify_model.py --ckpt <your_model>.ckpt
   ```

3. **检查训练日志**：确保看到 "Saved best model to..." 消息

4. **快速测试**：先跑5轮训练测试修复是否有效

---

**总结**：按照这个流程，你应该能从头到尾完成：环境准备 → 训练模型 → 验证模型 → 可视化使用
