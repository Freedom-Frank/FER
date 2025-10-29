# 批量处理快速开始

## 一键运行 - 多类别批量处理

```bash
# WSL/Linux 环境
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category
```

## 输出结果

运行后，在 `output/batch/` 目录下会生成：

### 1. 各类别统计图（7张）
- `statistics_angry.png`
- `statistics_disgust.png`
- `statistics_fear.png`
- `statistics_happy.png`
- `statistics_sad.png`
- `statistics_surprise.png`
- `statistics_neutral.png`

每张图显示：
- 该类别的预测分布
- 准确率百分比
- 真实标签用绿色标记

### 2. 准确率对比图（1张）
- `accuracy_comparison.png`

显示：
- 7个类别的准确率排名
- 颜色编码（绿色=好，黄色=一般，红色=差）
- 平均准确率参考线

## 控制台输出

```
======================================================================
BATCH PROCESSING - MULTI-CATEGORY MODE
======================================================================
[INFO] Found 7 categories: angry, disgust, fear, happy, sad, surprise, neutral
[INFO] Save images: False

======================================================================
[1/7] Processing category: ANGRY
======================================================================
[INFO] Found 467 images in /mnt/e/Users/Meng/Datasets/FER2013/test/angry
[1/467] Processing...
[50/467] Processing...
...

[INFO] Category: ANGRY
[INFO] Total images processed: 450
[INFO] Correct predictions: 315
[INFO] Accuracy: 70.00%

[STATISTICS] Prediction distribution:
  angry: 315 (70.0%) ← TRUE LABEL
  disgust: 25 (5.6%)
  fear: 30 (6.7%)
  happy: 10 (2.2%)
  sad: 50 (11.1%)
  surprise: 15 (3.3%)
  neutral: 5 (1.1%)

======================================================================
OVERALL ACCURACY REPORT
======================================================================

Category     Total    Correct  Accuracy   Rank
----------------------------------------------------------------------
happy        436      350      80.28%     #1
neutral      478      370      77.41%     #2
sad          456      330      72.37%     #3
angry        450      315      70.00%     #4
surprise     415      280      67.47%     #5
fear         470      290      61.70%     #6
disgust      440      230      52.27%     #7
----------------------------------------------------------------------
AVERAGE                        68.79%

======================================================================
ALL CATEGORIES PROCESSED!
Results saved to: output/batch
======================================================================
```

## 可选参数

### GPU 加速（强烈推荐）

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --device GPU
```

### 保存标注图片（可选）

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --save_images
```

**注意**：添加 `--save_images` 会保存所有标注后的图片，会占用大量磁盘空间和处理时间。

## 单类别处理

如果只想处理某一个类别：

```bash
# 只处理 sad 类别
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/sad
```

输出：
- `output/batch/statistics_sad.png`

## 预期时间

### CPU 模式
- 约 10-20 张/秒
- 全部 7 个类别（约 3500 张图）：约 3-6 分钟

### GPU 模式
- 约 50-100 张/秒
- 全部 7 个类别（约 3500 张图）：约 35-70 秒

## 下一步

1. **查看统计图**：浏览 `output/batch/` 目录中的图片
2. **分析结果**：
   - 查看 `accuracy_comparison.png` 了解整体表现
   - 查看各个 `statistics_{category}.png` 分析混淆模式
3. **改进模型**：根据发现的问题调整训练策略

## 更多信息

- 详细指南：[docs/batch_multi_category_guide.md](docs/batch_multi_category_guide.md)
- 完整文档：[README.md](README.md)
