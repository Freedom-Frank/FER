# CSV 批量评估快速开始

## 为什么使用 CSV 而不是图片文件？

### 图片文件的问题
- ❌ 需要 OpenCV 人脸检测
- ❌ 检测器可能漏检（特别是低分辨率图片）
- ❌ 对图片质量要求高
- ❌ 处理速度较慢

### CSV 数据的优势
- ✅ 直接使用像素数据，无需人脸检测
- ✅ **100% 不漏检**：所有样本都会被处理
- ✅ 处理速度更快
- ✅ 结果更准确、更可靠

## 一键运行

### CPU 模式

```bash
python src/batch_eval_csv.py \
  --csv E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest
```

### GPU 模式（推荐）

```bash
python src/batch_eval_csv.py \
  --csv E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

## 参数说明

- `--csv`: CSV 文件路径（必需）
- `--ckpt`: 模型检查点路径（必需）
- `--usage`: 使用哪个数据集
  - `Training`: 训练集
  - `PublicTest`: 公开测试集
  - `PrivateTest`: 私有测试集（**默认，推荐**）
- `--device`: 计算设备 (`CPU` 或 `GPU`)
- `--output`: 输出目录（默认：`output/batch_csv`）

## 输出结果

运行后，在 `output/batch_csv/` 目录下生成：

### 1. 各类别统计图（7张）
- `statistics_angry.png`
- `statistics_disgust.png`
- `statistics_fear.png`
- `statistics_happy.png`
- `statistics_sad.png`
- `statistics_surprise.png`
- `statistics_neutral.png`

### 2. 准确率对比图（1张）
- `accuracy_comparison.png`

## 控制台输出示例

```
======================================================================
CSV BATCH EVALUATION - ALL CATEGORIES
======================================================================
[INFO] CSV file: E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv
[INFO] Usage: PrivateTest
[INFO] Loading CSV file...
[INFO] Found 3589 images in PrivateTest set

======================================================================
Evaluating category: ANGRY
======================================================================
Processing angry: 100%|████████████████████| 467/467 [00:15<00:00, 30.45it/s]

[INFO] Category: ANGRY
[INFO] Total images: 467
[INFO] Correct predictions: 327
[INFO] Accuracy: 70.02%

[STATISTICS] Prediction distribution:
  angry: 327 (70.0%) ← TRUE LABEL
  disgust: 28 (6.0%)
  fear: 32 (6.9%)
  happy: 12 (2.6%)
  sad: 48 (10.3%)
  surprise: 15 (3.2%)
  neutral: 5 (1.1%)

... (其他类别类似输出) ...

======================================================================
OVERALL ACCURACY REPORT
======================================================================

Category     Total    Correct  Accuracy   Rank
----------------------------------------------------------------------
happy        895      718      80.22%     #1
neutral      626      485      77.48%     #2
sad          653      473      72.44%     #3
angry        467      327      70.02%     #4
surprise     415      280      67.47%     #5
fear         528      326      61.74%     #6
disgust      5        2        40.00%     #7
----------------------------------------------------------------------
AVERAGE                        67.05%

[SAVE] Accuracy comparison saved to output/batch_csv/accuracy_comparison.png

======================================================================
ALL CATEGORIES EVALUATED!
Results saved to: output/batch_csv
======================================================================
```

## 与图片文件方式的对比

| 特性 | CSV 方式 | 图片文件方式 |
|------|---------|-------------|
| 人脸检测 | ❌ 不需要 | ✅ 需要 |
| 漏检问题 | ❌ 无漏检 | ⚠️ 可能漏检 |
| 处理速度 | ⚡ 快 | 🐢 较慢 |
| 准确率 | ✅ 真实准确率 | ⚠️ 可能偏高（漏检的样本不算） |
| 样本数量 | 📊 所有样本 | 📉 漏检后的样本 |

## 数据集选择建议

### PrivateTest（推荐）
```bash
python src/batch_eval_csv.py \
  --csv E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest
```
- **用途**：最终模型评估
- **样本数**：约 3,589 张
- **特点**：模型训练时未见过的数据，最真实的性能指标

### PublicTest
```bash
python src/batch_eval_csv.py \
  --csv E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PublicTest
```
- **用途**：验证集评估
- **样本数**：约 3,589 张
- **特点**：可能在训练过程中用于验证

### Training（不推荐用于评估）
```bash
python src/batch_eval_csv.py \
  --csv E:/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage Training
```
- **用途**：仅用于调试
- **样本数**：约 28,709 张
- **特点**：训练集，准确率会虚高

## 预期时间

### PrivateTest（3,589 张）

#### CPU 模式
- 约 20-30 张/秒
- 总时间：约 2-3 分钟

#### GPU 模式
- 约 100-150 张/秒
- 总时间：约 25-40 秒

### PublicTest（3,589 张）
- 与 PrivateTest 相同

### Training（28,709 张）
- CPU：约 15-20 分钟
- GPU：约 3-5 分钟

## 安装依赖

如果出现 `tqdm` 未安装的错误：

```bash
pip install tqdm
```

## WSL 路径转换

在 WSL 环境中，Windows 路径需要转换：

```bash
# Windows 路径
E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv

# WSL 路径
/mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv
```

**WSL 命令**：
```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

## 对比两种方式

可以同时运行两种方式，对比结果：

### 1. CSV 方式（无漏检）
```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --output output/batch_csv
```

### 2. 图片文件方式（可能有漏检）
```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --output output/batch_images
```

### 3. 对比结果
- 查看两个目录下的 `accuracy_comparison.png`
- CSV 方式的准确率通常会**略低**但**更真实**
- 图片方式可能因为漏检导致准确率虚高

## 常见问题

### Q: CSV 准确率比图片方式低？
**A**: 这是正常的，因为：
- CSV 方式处理了**所有样本**（包括难识别的）
- 图片方式漏检的往往是**难识别的样本**
- CSV 方式的结果**更真实、更可靠**

### Q: 某个类别样本数很少？
**A**: FER2013 数据集本身类别不平衡，例如 disgust 类别样本很少，这是正常的。

### Q: 需要安装额外依赖吗？
**A**: 只需要 `tqdm`：
```bash
pip install tqdm
```

## 推荐工作流程

1. **使用 CSV 方式获取真实准确率**：
   ```bash
   python src/batch_eval_csv.py \
     --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
     --ckpt checkpoints_50epoch/best_model.ckpt \
     --usage PrivateTest \
     --device GPU
   ```

2. **查看结果**：
   - `output/batch_csv/accuracy_comparison.png`
   - 各个 `statistics_{category}.png`

3. **根据结果改进模型**：
   - 识别表现差的类别
   - 分析混淆模式
   - 调整训练策略

## 相关文档

- 主文档：[README.md](README.md)
- 多类别批量处理指南：[docs/batch_multi_category_guide.md](docs/batch_multi_category_guide.md)
