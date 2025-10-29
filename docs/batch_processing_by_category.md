# 批量处理按类别保存功能说明

## 功能概述

从现在开始，`demo_visualization.py` 的 batch 模式支持按输入目录的类别名称自动创建独立的输出文件夹。这对于分类对比和结果分析非常有用。

## 功能特点

1. **自动识别类别**：从输入目录名称自动提取类别（如 sad、happy、angry 等）
2. **独立存放结果**：每个类别的结果保存在独立的子目录下
3. **专属统计图**：为每个类别生成独立的统计图表
4. **清晰的目录结构**：便于对比不同类别的识别效果

## 使用示例

### 场景：处理 FER2013 测试集的不同类别

假设你的 FER2013 测试集目录结构如下：

```
/mnt/e/Users/Meng/Datasets/FER2013/test/
├── angry/
│   ├── PrivateTest_10077120.jpg
│   ├── PrivateTest_10613684.jpg
│   └── ...
├── sad/
│   ├── PrivateTest_11288161.jpg
│   ├── PrivateTest_12052491.jpg
│   └── ...
├── happy/
│   ├── PrivateTest_13051954.jpg
│   └── ...
└── ...
```

### 处理单个类别

```bash
# 处理 sad 类别
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/sad

# 处理 happy 类别
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/happy

# 处理 angry 类别
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/angry
```

### 输出目录结构

运行后，输出目录将自动按类别组织：

```
output/batch/
├── sad/                                    # sad 类别的结果
│   ├── PrivateTest_11288161_result.jpg
│   ├── PrivateTest_12052491_result.jpg
│   ├── ...
│   └── statistics_sad.png                  # sad 类别的统计图
├── happy/                                  # happy 类别的结果
│   ├── PrivateTest_13051954_result.jpg
│   ├── ...
│   └── statistics_happy.png               # happy 类别的统计图
├── angry/                                  # angry 类别的结果
│   ├── PrivateTest_10077120_result.jpg
│   ├── ...
│   └── statistics_angry.png               # angry 类别的统计图
└── ...
```

## 输出内容说明

### 1. 标注图片（*_result.jpg）

每张输入图片会生成一个对应的结果图，包含：
- 人脸检测框（带颜色编码）
- 预测的表情标签和置信度
- 右侧的 7 种表情概率条形图

### 2. 统计图（statistics_{类别名}.png）

每个类别会生成一个专属的统计图表，显示：
- 该类别中每种表情被预测的次数
- 彩色柱状图，直观展示表情分布
- 图表标题包含类别名称（如 "Emotion Distribution - SAD"）

## 实用场景

### 1. 评估分类准确率

通过对比真实标签（目录名）和预测结果的统计图，可以快速评估模型在特定表情类别上的表现：

- **理想情况**：sad 目录的统计图中，"sad" 柱子应该最高
- **混淆分析**：如果其他表情柱子较高，说明模型容易将该类别误判为其他表情

### 2. 错误分析

查看各个类别目录下的标注图片，可以：
- 找出预测错误的样本
- 分析哪些样本容易混淆
- 识别数据质量问题

### 3. 模型对比

使用不同的模型 checkpoint 处理同一类别，对比结果：

```bash
# 使用模型 A
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/model_a.ckpt \
  --input /path/to/test/sad

# 使用模型 B（需要先清理或备份之前的结果）
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/model_b.ckpt \
  --input /path/to/test/sad
```

## 批量处理多个类别

### 使用 Bash 脚本

创建一个脚本来自动处理所有类别：

```bash
#!/bin/bash

CKPT="checkpoints_50epoch/best_model.ckpt"
TEST_DIR="/mnt/e/Users/Meng/Datasets/FER2013/test"

for category in angry disgust fear happy sad surprise neutral; do
    echo "Processing category: $category"
    python tools/demo_visualization.py \
        --mode batch \
        --ckpt $CKPT \
        --input "$TEST_DIR/$category"
    echo "Completed: $category"
    echo "----------------------------------------"
done

echo "All categories processed!"
echo "Results saved in: output/batch/"
```

### 使用 Windows 批处理

```batch
@echo off
set CKPT=checkpoints_50epoch\best_model.ckpt
set TEST_DIR=\mnt\e\Users\Meng\Datasets\FER2013\test

for %%c in (angry disgust fear happy sad surprise neutral) do (
    echo Processing category: %%c
    python tools\demo_visualization.py ^
        --mode batch ^
        --ckpt %CKPT% ^
        --input "%TEST_DIR%\%%c"
    echo Completed: %%c
    echo ----------------------------------------
)

echo All categories processed!
echo Results saved in: output\batch\
pause
```

## 技术细节

### 类别名称提取

脚本使用 `os.path.basename(os.path.normpath(image_dir))` 来提取输入目录的最后一级目录名作为类别名称。

例如：
- `/mnt/e/Users/Meng/Datasets/FER2013/test/sad` → `sad`
- `/path/to/test/happy/` → `happy`

### 输出目录创建

输出目录会自动创建为 `{原始输出目录}/{类别名}/`，例如：
- 原始输出目录：`output/batch`
- sad 类别结果：`output/batch/sad/`
- happy 类别结果：`output/batch/happy/`

### 统计图命名

统计图文件名格式为 `statistics_{类别名}.png`，并保存在对应的类别目录下。

## 注意事项

1. **目录名即类别名**：确保输入目录名称准确反映类别（如 sad、happy 等）
2. **结果覆盖**：重复处理同一类别会覆盖之前的结果，建议备份重要结果
3. **路径兼容**：在 WSL 环境中使用 Windows 路径时，使用 `/mnt/` 前缀
4. **输出目录**：默认输出到 `output/batch/`，可通过修改代码更改基础输出路径

## 与旧版本的区别

### 旧版本（修改前）
- 所有类别的结果混在一起，保存在 `output/batch/` 下
- 只有一个总的 `statistics.png`
- 难以区分不同类别的结果

### 新版本（修改后）
- 每个类别的结果独立存放在 `output/batch/{类别名}/` 下
- 每个类别有专属的 `statistics_{类别名}.png`
- 清晰的目录结构，便于对比和分析

## 相关文件

- 主要修改文件：[src/visualize.py](../src/visualize.py) 中的 `process_batch()` 方法
- 演示脚本：[tools/demo_visualization.py](../tools/demo_visualization.py)
- 主文档：[README.md](../README.md)

## 反馈与建议

如有任何问题或改进建议，欢迎提交 Issue。
