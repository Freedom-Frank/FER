# 样例生成命令速查表

根据数据集路径：`/mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv`

## 🎯 推荐命令（复制即用）

### ⭐ 最推荐：生成预测正确的样例

```bash
# 基本使用（每种表情3个正确样例）
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3
```

**特点**：
- ✅ 只保存预测正确的样例
- ✅ 适合项目展示
- ✅ 自动过滤错误预测
- ✅ 输出到 `correct_samples/` 目录

---

## 📋 所有可用命令

### 1. 生成预测正确的样例（推荐用于展示）

```bash
# 基本使用
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3

# GPU 加速（推荐）
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 3

# 快速测试（每种表情1个）
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 1

# 生成更多样例（每种表情5个）
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 5

# 困难表情（增加尝试次数）
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --max_attempts 2000 \
    --num_samples 3
```

**输出目录**：`correct_samples/`

---

### 2. 简化脚本（包含正确和错误样例）

```bash
# 基本使用
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output samples_output \
    --num_samples 2

# GPU 加速
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 3

# 生成更多样例
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 5
```

**输出目录**：`samples_output/`

---

### 3. 完整脚本（包含对比表）

```bash
# 基本使用
python generate_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output samples_output \
    --num_samples 3

# GPU 加速
python generate_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 3
```

**输出目录**：`samples_output/`
**额外输出**：`emotion_comparison_sheet.png`（对比表）

---

### 4. 快速脚本（使用现有可视化工具）

```bash
# 基本使用
python quick_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 2

# GPU 加速
python quick_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 2
```

**输出目录**：
- 样例图片：`test_samples/`
- 处理结果：`samples_results/`

---

### 5. 可视化脚本（处理已有图片）

```bash
# 单张图片
python demo_visualization.py \
    --mode image \
    --ckpt checkpoints/best_model.ckpt \
    --input your_image.jpg

# 批量处理
python demo_visualization.py \
    --mode batch \
    --ckpt checkpoints/best_model.ckpt \
    --input test_images/

# GPU 加速
python demo_visualization.py \
    --mode image \
    --ckpt checkpoints/best_model.ckpt \
    --input your_image.jpg \
    --device GPU
```

**输出目录**：`output/images/` 或 `output/batch/`

---

## 🔍 使用场景对比

| 场景 | 推荐命令 | 输出特点 |
|------|---------|---------|
| **项目展示** | `generate_correct_samples.py` | 只有正确预测，效果最佳 |
| **误差分析** | `generate_samples_simple.py` | 包含正确和错误，便于分析 |
| **完整报告** | `generate_samples.py` | 包含对比表，展示全面 |
| **快速测试** | `quick_samples.py` | 快速提取和处理 |
| **处理图片** | `demo_visualization.py` | 处理已有图片 |

---

## 📊 参数说明

### 通用参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--csv` | 数据集路径 | 必需 | `/mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv` |
| `--ckpt` | 模型路径 | 必需 | `checkpoints/best_model.ckpt` |
| `--output` | 输出目录 | 脚本相关 | `my_samples` |
| `--device` | 计算设备 | `CPU` | `CPU` 或 `GPU` |
| `--num_samples` | 每种表情样例数 | 2-3 | `1`, `3`, `5` |

### generate_correct_samples.py 特有参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--max_attempts` | 每个样例最大尝试次数 | `1000` |
| `--usage` | 数据集分割 | `PublicTest` |

---

## 💡 使用技巧

### 1. 选择合适的模型

```bash
# 使用最佳模型（推荐）
--ckpt checkpoints/best_model.ckpt

# 使用特定 epoch 的模型
--ckpt checkpoints/fer-5_449.ckpt

# 查看所有可用模型
ls -lh checkpoints/
```

### 2. 使用 GPU 加速

```bash
# 所有脚本都支持 GPU
--device GPU

# 检查 GPU 是否可用
python -c "import mindspore as ms; print(ms.context.get_context('device_target'))"
```

### 3. 调整输出数量

```bash
# 快速测试（7个样例，每种表情1个）
--num_samples 1

# 常规使用（21个样例，每种表情3个）
--num_samples 3

# 详细展示（35个样例，每种表情5个）
--num_samples 5
```

### 4. 使用不同数据集分割

```bash
# 公开测试集（推荐，~3500样本）
--usage PublicTest

# 训练集（最多样本，~28000样本）
--usage Training

# 私有测试集（~3500样本）
--usage PrivateTest
```

---

## 🚀 快速开始

### 场景 1：我想要最好效果的样例用于展示

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 3
```

### 场景 2：我想要快速预览模型效果

```bash
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 1
```

### 场景 3：我想要详细的性能分析

```bash
python generate_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 5
```

### 场景 4：我有自己的图片要处理

```bash
python demo_visualization.py \
    --mode batch \
    --ckpt checkpoints/best_model.ckpt \
    --input my_images/
```

---

## 📁 输出文件结构

### generate_correct_samples.py 输出

```
correct_samples/
├── angry/
│   ├── correct_sample_1.png
│   ├── correct_sample_2.png
│   └── correct_sample_3.png
├── disgust/
├── fear/
├── happy/
├── sad/
├── surprise/
└── neutral/
```

### generate_samples_simple.py 输出

```
samples_output/
├── angry/
│   ├── sample_1.png
│   ├── sample_2.png
│   └── sample_3.png
├── disgust/
├── ...
└── all_samples_grid.png  # 网格展示
```

### generate_samples.py 输出

```
samples_output/
├── angry/
├── disgust/
├── ...
├── all_samples_grid.png
└── emotion_comparison_sheet.png  # 对比表
```

---

## 📚 相关文档

- [CORRECT_SAMPLES_README.md](CORRECT_SAMPLES_README.md) - 正确样例生成详细说明
- [SAMPLES_README.md](SAMPLES_README.md) - 普通样例生成详细说明
- [SAMPLES_EXAMPLES.md](SAMPLES_EXAMPLES.md) - 样例展示示例
- [SAMPLES_QUICKSTART.md](SAMPLES_QUICKSTART.md) - 快速入门指南
- [README.md](README.md) - 项目主文档

---

## ⚡ 常见问题

### Q: 哪个命令最好？
**A:** 看使用场景：
- 展示效果：`generate_correct_samples.py`（只要最好的）
- 分析性能：`generate_samples_simple.py`（看所有情况）
- 处理图片：`demo_visualization.py`（已有图片）

### Q: 如何加快生成速度？
**A:** 三个方法：
1. 使用 GPU：`--device GPU`
2. 减少样例数：`--num_samples 1`
3. 使用更好的模型（准确率高）

### Q: 输出目录可以自定义吗？
**A:** 可以，使用 `--output` 参数：
```bash
--output my_custom_output_dir
```

### Q: 如何查看帮助信息？
**A:** 运行时加 `--help`：
```bash
python generate_correct_samples.py --help
python generate_samples_simple.py --help
```
