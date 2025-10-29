# 多类别批量处理功能指南

## 功能概述

新的批量处理功能支持：
1. **只保存统计图**：默认不保存每张图片的标注结果，只生成统计图表
2. **一次性处理所有类别**：传入父目录，自动识别并处理所有类别
3. **准确率计算**：自动计算每个类别的准确率
4. **准确率排名**：生成各类别准确率对比图

## 使用方法

### 方法 1：多类别批量处理（推荐）

一次性处理所有类别，生成完整的统计报告：

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category
```

**参数说明**：
- `--mode batch`：批处理模式
- `--ckpt`：模型检查点路径
- `--input`：**父目录路径**（包含 angry, sad, happy 等子目录）
- `--multi_category`：启用多类别模式

**输出结果**：
```
output/batch/
├── statistics_angry.png          # angry 类别的预测分布
├── statistics_disgust.png        # disgust 类别的预测分布
├── statistics_fear.png           # fear 类别的预测分布
├── statistics_happy.png          # happy 类别的预测分布
├── statistics_sad.png            # sad 类别的预测分布
├── statistics_surprise.png       # surprise 类别的预测分布
├── statistics_neutral.png        # neutral 类别的预测分布
└── accuracy_comparison.png       # 准确率对比图（带排名）
```

### 方法 2：单类别处理

只处理一个类别：

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/sad
```

**输出结果**：
```
output/batch/
└── statistics_sad.png            # sad 类别的预测分布
```

### 方法 3：保存标注图片（可选）

如果需要保存每张图片的标注结果，添加 `--save_images` 参数：

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --save_images
```

**注意**：启用 `--save_images` 会大大增加处理时间和磁盘空间占用，仅在需要时使用。

## 输出结果详解

### 1. 类别统计图（statistics_{category}.png）

每个类别生成一张统计图，显示：
- **X轴**：预测的表情类别
- **Y轴**：预测数量
- **颜色**：
  - **绿色柱子**：真实标签（True Label）
  - **其他颜色**：错误预测
- **标题**：包含类别名称和准确率
- **数值标签**：显示数量和百分比

**示例**：
```
Prediction Distribution - TRUE LABEL: SAD
Accuracy: 72.45%
```

### 2. 准确率对比图（accuracy_comparison.png）

展示所有类别的准确率排名：
- **X轴**：表情类别（按准确率从高到低排序）
- **Y轴**：准确率百分比
- **颜色**：
  - **绿色**：准确率 ≥ 70%（表现良好）
  - **黄色**：准确率 50-70%（表现一般）
  - **红色**：准确率 < 50%（需要改进）
- **标注**：
  - 柱子上方：准确率百分比
  - 柱子内部：排名 (#1, #2, ...)
  - 柱子底部：样本数量 (n=xxx)
- **蓝色虚线**：平均准确率

### 3. 控制台输出

处理过程中会显示详细信息：

```
======================================================================
BATCH PROCESSING - MULTI-CATEGORY MODE
======================================================================
[INFO] Found 7 categories: angry, disgust, fear, happy, sad, surprise, neutral
[INFO] Save images: False

======================================================================
[1/7] Processing category: ANGRY
======================================================================
[INFO] Found 467 images in /path/to/test/angry
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

[SAVE] Statistics saved to output/batch/statistics_angry.png

... (其他类别similar输出) ...

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

[SAVE] Accuracy comparison saved to output/batch/accuracy_comparison.png

======================================================================
ALL CATEGORIES PROCESSED!
Results saved to: output/batch
======================================================================
```

## 使用场景

### 1. 快速评估模型性能

```bash
# 一键获取所有类别的准确率排名
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category
```

查看 `accuracy_comparison.png` 即可了解：
- 哪些表情识别效果最好
- 哪些表情需要改进
- 模型的整体平均准确率

### 2. 分析混淆模式

查看各个 `statistics_{category}.png`，了解：
- 哪些表情容易被混淆
- 常见的误判模式

**示例分析**：
- `statistics_sad.png` 显示很多样本被预测为 `angry`
- 说明模型容易将"悲伤"误判为"生气"
- 可能需要针对性地增强这两类的区分

### 3. 对比不同模型

```bash
# 模型 A
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/model_a.ckpt \
  --input /path/to/test \
  --multi_category

# 备份结果
mv output/batch output/batch_model_a

# 模型 B
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/model_b.ckpt \
  --input /path/to/test \
  --multi_category

# 对比 accuracy_comparison.png
```

### 4. 生成报告材料

统计图可直接用于：
- 项目演示
- 论文报告
- 模型文档

## 高级选项

### GPU 加速

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /path/to/test \
  --multi_category \
  --device GPU
```

### 自定义文件模式

默认处理 `*.jpg` 文件，可以通过修改代码支持其他格式。

## 性能建议

### 处理速度

- **CPU**：约 10-20 张/秒
- **GPU**：约 50-100 张/秒

### 磁盘空间

- **只保存统计图**：约 1-2 MB
- **保存所有标注图片**：约 数百 MB（取决于测试集大小）

### 建议

1. **默认不保存图片**：大多数情况下只需要统计图
2. **使用 GPU**：如果有 GPU，强烈建议使用以加速处理
3. **处理顺序**：先快速运行生成统计，再根据需要处理特定类别并保存图片

## 故障排除

### 问题 1：找不到类别

```
[ERROR] No valid emotion categories found in /path/to/dir
```

**解决方法**：
- 确保输入目录包含以下子目录之一：angry, disgust, fear, happy, sad, surprise, neutral
- 目录名必须完全匹配（小写）

### 问题 2：没有检测到人脸

```
[WARNING] No faces detected
```

**原因**：
- 图片质量问题
- 人脸太小或角度不正

**影响**：
- 这些图片会被跳过，不影响其他图片处理
- 统计中不包含这些图片

### 问题 3：内存不足

**症状**：程序崩溃或速度极慢

**解决方法**：
1. 减小批处理大小（修改代码中的批次处理逻辑）
2. 使用 CPU 模式（占用内存更少）
3. 分批处理（一次处理一个类别）

## 相关文件

- 核心实现：[src/visualize.py](../src/visualize.py)
  - `process_batch()`: 单类别处理
  - `process_batch_multi_category()`: 多类别处理
  - `generate_overall_report()`: 生成总体报告
  - `save_accuracy_comparison()`: 保存准确率对比图
- 演示脚本：[tools/demo_visualization.py](../tools/demo_visualization.py)
- 主文档：[README.md](../README.md)

## 反馈与建议

如有任何问题或改进建议，欢迎提交 Issue。
