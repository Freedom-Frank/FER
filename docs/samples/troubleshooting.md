# 样例生成故障排除指南

## 问题：无法找到正确的样例

如果看到类似以下错误：
```
[WARNING] Failed to generate for:
  - angry (sample 1)
  - angry (sample 2)
  - angry (sample 3)
  ...
```

## 🔍 步骤 1：诊断问题

首先运行诊断脚本，查看模型在每种表情上的准确率：

```bash
python diagnose_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt
```

**输出示例**：
```
============================================================
诊断模型预测性能
============================================================

加载模型: checkpoints/best_model.ckpt
✓ 模型加载成功

读取数据集: /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv
✓ 数据集加载成功 (PublicTest: 3589 样本)

============================================================
测试每种表情的准确率
============================================================

angry      - 准确率:  72.0% ( 72/100) - 预期尝试:    1.4 次
disgust    - 准确率:  55.0% ( 55/100) - 预期尝试:    1.8 次
fear       - 准确率:  65.0% ( 65/100) - 预期尝试:    1.5 次
happy      - 准确率:  87.0% ( 87/100) - 预期尝试:    1.1 次
sad        - 准确率:  58.0% ( 58/100) - 预期尝试:    1.7 次
surprise   - 准确率:  82.0% ( 82/100) - 预期尝试:    1.2 次
neutral    - 准确率:  75.0% ( 75/100) - 预期尝试:    1.3 次
```

---

## 🛠️ 解决方案

### 情况 1：所有表情准确率都是 0% 或接近 0%

**可能原因**：
- 模型文件损坏
- 模型与代码版本不匹配
- 数据预处理有问题

**解决方法**：

#### A. 检查模型文件

```bash
# 查看模型文件大小
ls -lh checkpoints/best_model.ckpt

# 应该至少有几百 KB，如果只有几 KB 说明文件不完整
```

#### B. 尝试其他模型

```bash
# 列出所有可用模型
ls -lh checkpoints/*.ckpt

# 尝试使用其他模型
python diagnose_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/fer-5_449.ckpt
```

#### C. 重新训练模型

```bash
# 重新训练一个新模型
python src/train.py \
    --data_csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --device_target GPU \
    --epochs 50 \
    --batch_size 64 \
    --augment
```

---

### 情况 2：准确率很低（< 20%）

**可能原因**：
- 模型训练不充分
- 使用了不合适的模型检查点

**解决方法**：

#### A. 使用训练好的最佳模型

```bash
# 检查哪个模型最好
# 查看训练日志或使用 eval.py 评估

python src/eval.py \
    --data_csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt_path checkpoints/best_model.ckpt

python src/eval.py \
    --data_csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt_path checkpoints/fer-5_449.ckpt
```

#### B. 增加训练轮数

如果准确率太低，可能需要更多训练：

```bash
python src/train.py \
    --data_csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --device_target GPU \
    --epochs 200 \
    --batch_size 96 \
    --augment \
    --mixup
```

---

### 情况 3：准确率中等（20-50%）

**可能原因**：
- 模型还可以，但需要更多尝试次数

**解决方法**：

#### 增加最大尝试次数

```bash
# 将最大尝试次数增加到 5000 次
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --max_attempts 5000 \
    --num_samples 3
```

**预期尝试次数计算**：
- 准确率 50%：平均需要 2 次尝试
- 准确率 33%：平均需要 3 次尝试
- 准确率 20%：平均需要 5 次尝试
- 准确率 10%：平均需要 10 次尝试

设置 `max_attempts` 为预期尝试次数的 100-1000 倍比较安全。

---

### 情况 4：准确率正常（> 50%），但仍然失败

**可能原因**：
- 运气不好（概率问题）
- 数据集分割有问题

**解决方法**：

#### A. 增加尝试次数

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --max_attempts 2000 \
    --num_samples 3
```

#### B. 使用训练集（更多样本）

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --usage Training \
    --max_attempts 2000 \
    --num_samples 3
```

训练集有 ~28,000 个样本，比测试集的 ~3,500 多得多。

#### C. 启用详细模式查看问题

```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 1 \
    --verbose
```

这会显示前 10 次尝试的预测结果，帮助你诊断问题。

---

### 情况 5：某些特定表情失败

**可能原因**：
- 模型在某些表情上表现较差
- 数据不平衡

**解决方法**：

#### A. 针对困难表情增加尝试次数

查看诊断输出，找出准确率最低的表情，然后针对性处理：

```bash
# 假设 disgust 准确率最低（30%）
# 增加最大尝试次数到 10000
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --max_attempts 10000 \
    --num_samples 1
```

#### B. 使用不同的脚本生成混合样例

如果实在无法生成某些表情的正确样例，使用普通脚本：

```bash
# 生成包含正确和错误的样例
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 10
```

然后手动从输出中挑选正确的样例。

---

## 🎯 推荐的完整诊断流程

### 步骤 1：诊断模型

```bash
python diagnose_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_test 100
```

### 步骤 2：根据结果选择策略

**如果平均准确率 > 60%**：
```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3 \
    --max_attempts 1000
```

**如果平均准确率 40-60%**：
```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3 \
    --max_attempts 3000 \
    --usage Training
```

**如果平均准确率 20-40%**：
```bash
python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 1 \
    --max_attempts 10000 \
    --usage Training
```

**如果平均准确率 < 20%**：
```bash
# 模型质量太差，考虑重新训练或使用混合样例
python generate_samples_simple.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 5
```

---

## 💡 其他技巧

### 1. 使用 GPU 加速

所有脚本都支持 GPU，可以大幅提升速度：

```bash
python diagnose_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU

python generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --device GPU \
    --num_samples 3
```

### 2. 分批生成

如果某些表情很困难，可以先生成容易的表情（如 happy, surprise），再处理困难的：

```bash
# 修改脚本，只处理特定表情
# 或先生成 num_samples=1，成功后再增加
```

### 3. 混合策略

结合正确和混合样例：

```bash
# 先生成正确样例
python generate_correct_samples.py ... --num_samples 2

# 再生成混合样例作为补充
python generate_samples_simple.py ... --num_samples 3
```

### 4. 检查数据集完整性

```bash
# 验证数据集文件
python -c "
import pandas as pd
df = pd.read_csv('/mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv')
print(f'Total samples: {len(df)}')
print(f'Emotions distribution:')
print(df['emotion'].value_counts().sort_index())
print(f'Usage distribution:')
print(df['Usage'].value_counts())
"
```

预期输出：
```
Total samples: 35887
Emotions distribution:
0     4953  (angry)
1      547  (disgust)
2     5121  (fear)
3     8989  (happy)
4     6077  (sad)
5     4002  (surprise)
6     6198  (neutral)

Usage distribution:
Training        28709
PublicTest       3589
PrivateTest      3589
```

---

## 📞 需要更多帮助？

1. 查看完整文档：[CORRECT_SAMPLES_README.md](CORRECT_SAMPLES_README.md)
2. 查看主文档：[README.md](README.md)
3. 运行帮助命令：
   ```bash
   python generate_correct_samples.py --help
   python diagnose_correct_samples.py --help
   ```

---

## 🎯 快速命令参考

```bash
# 诊断模型
python diagnose_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt

# 标准生成（推荐）
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --num_samples 3

# 增加尝试次数
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --max_attempts 5000 --num_samples 3

# 使用训练集
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --usage Training --max_attempts 3000 --num_samples 3

# GPU 加速
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --device GPU --num_samples 3

# 详细调试
python generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv --ckpt checkpoints/best_model.ckpt --verbose --num_samples 1
```
