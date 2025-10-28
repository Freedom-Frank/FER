# FER2013 样例展示说明

本文档展示如何生成面部表情识别的样例结果。

## 样例格式

每个样例包含两部分：
1. **左侧**：原始图片（48x48 灰度图）+ 真实表情标签
2. **右侧**：识别结果（7种表情的概率分布柱状图）+ 预测表情和置信度

## 使用方法

### 方法 1：使用简化脚本生成样例

```bash
# 生成每种表情各2个样例
python generate_samples_simple.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output samples_output \
    --num_samples 2

# 生成更多样例（每种表情5个）
python generate_samples_simple.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output samples_output \
    --num_samples 5
```

### 方法 2：使用完整脚本（包含对比表）

```bash
python generate_samples.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output samples_output \
    --num_samples 3
```

### 方法 3：使用批处理脚本（Windows）

```bash
# 直接双击运行
scripts\generate_samples.bat

# 或在命令行运行
.\scripts\generate_samples.bat
```

## 输出文件结构

生成的样例将保存在以下位置：

```
samples_output/
├── angry/                          # 生气表情样例
│   ├── sample_1.png               # （原图）-（识别结果）
│   ├── sample_2.png
│   └── sample_3.png
├── disgust/                       # 厌恶表情样例
│   ├── sample_1.png
│   └── ...
├── fear/                          # 恐惧表情样例
├── happy/                         # 开心表情样例
├── sad/                           # 悲伤表情样例
├── surprise/                      # 惊讶表情样例
├── neutral/                       # 中性表情样例
├── all_samples_grid.png           # 所有样例的网格展示
└── emotion_comparison_sheet.png   # 表情对比表（仅完整脚本）
```

## 样例说明

### 单个样例文件格式

每个 `sample_N.png` 文件包含：

**左侧区域：**
- 48x48 灰度人脸图像
- 标题显示真实表情（中文+英文）
- 绿色标题 = 预测正确
- 红色标题 = 预测错误

**右侧区域：**
- 横向柱状图显示7种表情的概率分布
- 红色柱子：真实表情的概率
- 蓝绿色柱子：其他表情的概率
- 橙色柱子：错误预测的表情（如果有）
- 标题显示预测结果、置信度和是否正确（✓/✗）

### 网格展示文件

`all_samples_grid.png` 文件：
- 将所有样例排列成网格（4列）
- 每个格子显示原图 + 简化的识别结果
- 便于快速浏览所有样例

### 对比表文件（完整脚本）

`emotion_comparison_sheet.png` 文件：
- 7行（每种表情一行）
- 每行显示3个样例
- 整齐排列，便于比较不同表情的识别效果

## 样例示例说明

### 示例 1：正确识别的开心表情

```
左侧：微笑的人脸图像
标题：真实表情: Happy (happy) [绿色]

右侧：概率分布柱状图
happy: ████████████████████████ 85.3%  (红色，最长)
surprise: ███ 8.1%
neutral: ██ 4.2%
sad: █ 1.5%
fear: █ 0.5%
angry: ▌ 0.3%
disgust: ▌ 0.1%

标题：预测结果: happy (置信度: 85.3%) ✓ [绿色]
```

### 示例 2：错误识别的悲伤表情

```
左侧：悲伤的人脸图像
标题：真实表情: Sad (sad) [红色]

右侧：概率分布柱状图
neutral: █████████████████ 62.1%  (橙色，最长 - 错误预测)
sad: ████████ 28.5%  (红色 - 真实标签)
angry: ██ 5.2%
fear: █ 3.1%
disgust: ▌ 0.8%
surprise: ▌ 0.2%
happy: ▌ 0.1%

标题：预测结果: neutral (置信度: 62.1%) ✗ [红色]
```

## 配置选项

### 数据集选择

通过 `--usage` 参数选择不同的数据集：

```bash
# 使用公开测试集（默认，推荐）
python generate_samples_simple.py ... --usage PublicTest

# 使用训练集
python generate_samples_simple.py ... --usage Training

# 使用私有测试集
python generate_samples_simple.py ... --usage PrivateTest
```

### 样例数量

```bash
# 每种表情1个样例（快速预览）
python generate_samples_simple.py ... --num_samples 1

# 每种表情5个样例（详细展示）
python generate_samples_simple.py ... --num_samples 5
```

### 设备选择

```bash
# CPU运行（默认）
python generate_samples_simple.py ... --device CPU

# GPU运行（需要GPU环境）
python generate_samples_simple.py ... --device GPU
```

### 模型选择

```bash
# 使用默认模型
python generate_samples_simple.py ... --ckpt checkpoints/best_model.ckpt

# 使用特定epoch的模型
python generate_samples_simple.py ... --ckpt checkpoints/fer-5_449.ckpt
```

## 常见问题

### Q: 生成样例时出现中文乱码？
**A:** 脚本使用了多种中文字体fallback机制。如果仍有问题，可以：
- 使用 `generate_samples_simple.py`（使用英文标签）
- 安装 SimHei 或 Arial Unicode MS 字体

### Q: 生成速度慢？
**A:** 优化方法：
- 减少样例数量：`--num_samples 1`
- 使用 GPU：`--device GPU`（如果有GPU环境）
- 使用训练集（数据更多）：`--usage Training`

### Q: 输出文件在哪里？
**A:** 默认保存在 `samples_output/` 目录。可通过 `--output` 参数修改：
```bash
python generate_samples_simple.py ... --output my_samples
```

### Q: 如何选择最佳样例？
**A:** 建议使用公开测试集（PublicTest），因为：
- 数据分布平衡
- 未用于训练，能反映真实性能
- 与官方基准一致

## 样例应用场景

### 1. 项目展示
将 `all_samples_grid.png` 添加到 README.md：
```markdown
## 识别效果展示
![样例展示](samples_output/all_samples_grid.png)
```

### 2. 论文/报告
使用单个样例文件展示识别过程：
- 选择识别正确的样例展示模型优势
- 选择识别错误的样例进行误差分析

### 3. 模型对比
对不同模型生成样例并比较：
```bash
# 模型 A
python generate_samples_simple.py ... --ckpt checkpoints/model_a.ckpt --output samples_a

# 模型 B
python generate_samples_simple.py ... --ckpt checkpoints/model_b.ckpt --output samples_b
```

### 4. 错误分析
筛选识别错误的样例，分析原因：
- 表情相似（如 sad 和 neutral）
- 图像质量问题
- 表情标注错误
- 边界情况

## 进阶使用

### 只生成特定表情的样例

修改脚本，在 `load_sample_images` 函数中指定 emotion_id：

```python
# 只加载 happy 表情（emotion_id=3）
samples = load_sample_images(csv_path, num_samples=10, usage='PublicTest')
happy_samples = samples[3]  # 只处理 happy 表情
```

### 自定义可视化样式

在 `create_sample_visualization` 函数中修改：
- 颜色方案：`colors` 变量
- 字体大小：`fontsize` 参数
- 图片尺寸：`figsize` 参数
- DPI：`dpi` 参数

### 批量处理并统计

```python
# 生成100个样例并统计每种表情的准确率
python generate_samples_simple.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 15 \
    --output large_samples
```

查看输出的统计信息，了解模型在不同表情上的表现。

## 相关文档

- [可视化指南](docs/visualization_guide.md) - 完整的可视化功能说明
- [快速开始](docs/quickstart.md) - 项目使用入门
- [模型优化](docs/optimization.md) - 提升识别准确率的方法

## 技术说明

### 图像预处理
- 输入：48x48 灰度图（像素值 0-255）
- 归一化：除以 255.0 转换到 [0, 1]
- 张量格式：(batch, channel, height, width) = (1, 1, 48, 48)

### 概率计算
- 模型输出：7维logits向量
- Softmax：转换为概率分布（和为1）
- 预测：选择概率最高的类别

### 颜色编码
- **红色**：真实标签对应的类别
- **蓝绿色**：其他类别
- **橙色**：错误预测的类别
- **绿色标题**：预测正确
- **红色标题**：预测错误

## 更新历史

- 2025-01: 添加简化版脚本 `generate_samples_simple.py`
- 2025-01: 添加批处理脚本支持
- 2025-01: 改进中文字体支持
- 2025-01: 添加网格展示和对比表功能
