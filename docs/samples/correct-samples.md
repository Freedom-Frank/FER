# 生成正确预测样例

本脚本专门用于生成**预测正确**的样例。它会持续从数据集中随机抽取样例，直到找到模型预测正确的样例并保存。

## 核心逻辑

```
对于每种表情：
    循环直到找到指定数量的正确样例：
        1. 从数据集中随机抽取一个该表情的样本
        2. 使用模型预测
        3. 如果预测正确（预测标签 == 真实标签）：
           - 保存样例可视化
           - 继续下一个样例
        4. 如果预测错误：
           - 丢弃该样例
           - 继续尝试下一个随机样本
```

## 使用方法

### 基本命令

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3
```

### 完整参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--csv` | 数据集路径 | 必需 | `/mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv` |
| `--ckpt` | 模型路径 | 必需 | `checkpoints/best_model.ckpt` |
| `--output` | 输出目录 | `correct_samples` | `my_correct_samples` |
| `--device` | 计算设备 | `CPU` | `CPU` 或 `GPU` |
| `--num_samples` | 每种表情的样例数 | `3` | `1`, `3`, `5` |
| `--usage` | 数据集分割 | `PublicTest` | `Training`, `PublicTest`, `PrivateTest` |
| `--max_attempts` | 每个样例最大尝试次数 | `1000` | `500`, `1000`, `2000` |

## 命令示例

### 示例 1：生成3个正确样例（推荐）

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3
```

输出：每种表情各3个预测正确的样例（共21个样例）

### 示例 2：使用 GPU 加速

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 5
```

### 示例 3：只生成1个样例（快速测试）

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 1
```

### 示例 4：增加最大尝试次数（用于准确率较低的模型）

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --max_attempts 2000 \
    --num_samples 3
```

### 示例 5：使用训练集数据

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --usage Training \
    --num_samples 3
```

### 示例 6：自定义输出目录

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --output best_samples \
    --num_samples 5
```

## 输出结果

### 文件结构

```
correct_samples/
├── angry/
│   ├── correct_sample_1.png
│   ├── correct_sample_2.png
│   └── correct_sample_3.png
├── disgust/
│   ├── correct_sample_1.png
│   ├── correct_sample_2.png
│   └── correct_sample_3.png
├── fear/
│   └── ...
├── happy/
│   └── ...
├── sad/
│   └── ...
├── surprise/
│   └── ...
└── neutral/
    └── ...
```

### 样例格式

每个样例包含：
- **左侧**：48x48 灰度人脸图像 + 真实表情标签（绿色）
- **右侧**：概率分布柱状图 + 预测结果（绿色，标记 [CORRECT]）

### 运行输出示例

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
  Found correct sample after 2 attempts! (confidence: 87.5%)
  Saved: correct_samples/happy/correct_sample_1.png

Generating sample 2/3...
  Found correct sample after 5 attempts! (confidence: 92.1%)
  Saved: correct_samples/happy/correct_sample_2.png

Generating sample 3/3...
  Found correct sample after 1 attempts! (confidence: 85.3%)
  Saved: correct_samples/happy/correct_sample_3.png

Completed: 3/3 correct samples found

============================================================
Processing: Sad (sad)
Target: 3 correct samples
============================================================
Available samples in dataset: 1024

Generating sample 1/3...
  Attempt 100... still searching...
  Found correct sample after 143 attempts! (confidence: 72.1%)
  Saved: correct_samples/sad/correct_sample_1.png

...

============================================================
Generation Complete!
============================================================

Statistics:
  Total correct samples generated: 21
  Total attempts needed: 456
  Average attempts per sample: 21.7

Output directory: correct_samples/
```

## 性能说明

### 尝试次数与准确率的关系

假设模型在某个表情类别上的准确率为 P：
- **期望尝试次数** = 1 / P

例如：
- 准确率 80%：平均需要 1.25 次尝试
- 准确率 50%：平均需要 2 次尝试
- 准确率 20%：平均需要 5 次尝试

### 各表情的预期性能

基于典型的 FER2013 模型表现（准确率 ~75%）：

| 表情 | 准确率 | 平均尝试次数 | 生成3个样例预计尝试 |
|------|--------|--------------|-------------------|
| Happy | ~85% | 1.2 | ~4 次 |
| Surprise | ~80% | 1.3 | ~4 次 |
| Neutral | ~75% | 1.3 | ~4 次 |
| Angry | ~70% | 1.4 | ~5 次 |
| Fear | ~65% | 1.5 | ~5 次 |
| Sad | ~60% | 1.7 | ~5 次 |
| Disgust | ~55% | 1.8 | ~6 次 |

### 优化建议

1. **使用最佳模型**：使用训练好的最佳检查点
   ```bash
   --ckpt checkpoints/best_model.ckpt
   ```

2. **使用 GPU**：大幅提升预测速度
   ```bash
   --device GPU
   ```

3. **调整最大尝试次数**：
   - 高准确率模型（>70%）：默认 1000 次足够
   - 低准确率模型（<60%）：增加到 2000-5000 次

4. **使用更大的数据集分割**：
   - `Training`：~28,000 样本（最大选择空间）
   - `PublicTest`：~3,500 样本（推荐）
   - `PrivateTest`：~3,500 样本

## 与普通样例生成的对比

| 特性 | 普通样例生成 | 正确样例生成 |
|------|-------------|-------------|
| 样例选择 | 随机抽取 | 持续尝试直到正确 |
| 预测结果 | 可能正确或错误 | 保证正确 |
| 生成速度 | 快 | 较慢（取决于准确率） |
| 用途 | 展示整体性能 | 展示最佳效果 |
| 误差分析 | 可分析错误 | 无法分析错误 |

## 使用场景

### 1. 项目展示
生成最佳效果的样例用于：
- README.md 展示
- 演示文稿
- 项目主页

### 2. 效果验证
验证模型在理想情况下的表现：
- 检查预测置信度
- 观察概率分布
- 验证模型理解

### 3. 对比展示
与错误样例对比，展示模型的能力边界

### 4. 教学材料
生成清晰的正确样例用于教学

## 故障排除

### Q: 某个表情一直找不到正确样例？
**A:** 可能原因：
1. **准确率太低**：该表情的准确率很低（<30%）
   - 解决：增加 `--max_attempts` 到 2000 或更高
   - 或使用更好的模型

2. **数据集太小**：该表情的样本数量太少
   - 解决：使用 `--usage Training`（更多样本）

3. **模型问题**：模型在该表情上表现极差
   - 解决：重新训练模型或使用其他检查点

### Q: 运行速度太慢？
**A:** 优化方法：
1. 使用 GPU：`--device GPU`
2. 减少样例数：`--num_samples 1`
3. 使用更好的模型（准确率更高）

### Q: 如何查看哪些表情难以找到正确样例？
**A:** 观察运行输出：
- 尝试次数多的表情：准确率低
- 显示 "Attempt 100..." 的表情：准确率很低
- 失败的表情：准确率极低（<10%）

### Q: 想要特定置信度的样例？
**A:** 修改脚本中的 `find_correct_sample` 函数，添加置信度条件：
```python
if pred_idx == emotion_id and confidence >= 0.8:  # 只接受置信度 >= 80% 的样例
    return image, pred_emotion, confidence, probs, attempts
```

## 快速复制命令

**最常用命令（复制即用）**：

```bash
# 基本使用
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --num_samples 3

# GPU 加速
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --device GPU --num_samples 3

# 快速测试（每种表情1个）
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --num_samples 1

# 生成更多样例
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --num_samples 5

# 困难表情（增加尝试次数）
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --max_attempts 2000 --num_samples 3
```

## 相关文档

- [SAMPLES_README.md](SAMPLES_README.md) - 普通样例生成说明
- [SAMPLES_EXAMPLES.md](SAMPLES_EXAMPLES.md) - 样例展示示例
- [README.md](README.md) - 项目主文档
