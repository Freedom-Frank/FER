# Checkpoint 文件说明

## 什么是 Checkpoint？

Checkpoint（检查点）是训练过程中保存的模型快照，可以用于：
1. **恢复训练**：如果训练中断，可以从 checkpoint 继续
2. **模型选择**：从不同 epoch 选择最佳模型
3. **备份**：防止训练失败导致模型丢失

---

## Checkpoint 文件命名规则

### 格式：`fer-{epoch}_{step}.ckpt`

例如：`fer-5_449.ckpt`

- `fer`：前缀（项目名称）
- `5`：**epoch 编号**（第 5 轮训练）
- `449`：**step 编号**（该轮的第 449 步）

### 详细解释

假设你有 28,709 张训练图片，batch_size = 64：
- 每个 epoch 有：28,709 ÷ 64 = **449 个 batch**（steps）
- 每个 epoch 结束时（第 449 步），保存一次 checkpoint

所以：
- `fer-1_449.ckpt` = **第 1 轮**结束时的模型
- `fer-5_449.ckpt` = **第 5 轮**结束时的模型
- `fer-50_449.ckpt` = **第 50 轮**结束时的模型

---

## 你的 checkpoints/ 目录中的文件

### 1. `fer_1-50_*.ckpt` 系列

```
fer_1-50_99.ckpt
fer_1-50_199.ckpt
fer_1-50_299.ckpt
fer_1-50_399.ckpt
fer_1-50_449.ckpt
```

**含义**：
- 这是一次 **50 轮训练**的 checkpoints
- `1-50` 表示从第 1 轮到第 50 轮的某次训练
- 每 100 steps 保存一次（99, 199, 299, 399, 449）

**为什么有多个？**
- MindSpore 的 `ModelCheckpoint` 配置为每个 epoch 保存，但会保留最近几个
- 你的配置是：`keep_checkpoint_max=5`（保留最近 5 个）

### 2. `fer-5_*.ckpt` 系列

```
fer-5_104.ckpt
fer-5_204.ckpt
fer-5_304.ckpt
fer-5_404.ckpt
fer-5_449.ckpt
```

**含义**：
- 这是另一次训练的 checkpoints
- 只有**第 5 轮**的 checkpoints（可能训练被中断了）
- 或者是设置了只保存第 5 轮的多个中间步骤

### 3. `best_model.ckpt`（最重要！）

```
best_model.ckpt  (434KB - 有问题) ❌
best_model.ckpt  (1.3MB - 正常)  ✓
```

**含义**：
- **验证准确率最高**的模型
- 由 `EvalCallback` 自动保存（修复后）
- **这是你应该用于可视化的模型**

**之前的问题**：
- 旧版本没有正确保存 `best_model.ckpt`
- 只有 434KB，是不完整的
- 修复后，每次准确率提升都会更新这个文件

### 4. `final_model.ckpt`

```
final_model.ckpt
```

**含义**：
- 训练**最后一轮**结束时的模型
- 不一定是最好的（可能准确率已经下降了）
- 由训练脚本在结束时保存

---

## 各种 Checkpoint 的区别

| 文件 | 保存时机 | 用途 | 推荐使用 |
|------|----------|------|----------|
| `fer-{epoch}_{step}.ckpt` | 每个 epoch 结束 | 训练过程快照，断点恢复 | ⭐⭐⭐ |
| `best_model.ckpt` | 验证准确率提升时 | **最佳性能模型** | ⭐⭐⭐⭐⭐ |
| `final_model.ckpt` | 训练结束 | 最终模型（不一定最好） | ⭐⭐ |

---

## 训练代码中的 Checkpoint 配置

### 在 `src/train.py` 中：

```python
# 1. 每个 epoch 保存的 checkpoints
config_ck = CheckpointConfig(
    save_checkpoint_steps=train_size,  # 每个 epoch 保存一次
    keep_checkpoint_max=5              # 只保留最近 5 个
)
ckpoint_cb = ModelCheckpoint(
    prefix='fer',                      # 前缀
    directory=args.save_dir,           # 保存目录
    config=config_ck
)

# 2. 最佳模型保存（修复后）
class EvalCallback(Callback):
    def on_train_epoch_end(self, run_context):
        # ...评估验证集
        if acc > self.best_acc:
            self.best_acc = acc
            # ✓ 保存最佳模型
            best_model_path = os.path.join(self.save_dir, 'best_model.ckpt')
            save_checkpoint(cb_params.train_network, best_model_path)
            print(f"Saved best model to: {best_model_path}")

# 3. 最终模型保存
final_path = os.path.join(args.save_dir, 'final_model.ckpt')
save_checkpoint(net, final_path)
```

---

## 哪个 Checkpoint 应该用？

### ✅ 推荐使用：`best_model.ckpt`

```bash
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3
```

**原因**：
- ✓ 验证集准确率最高
- ✓ 泛化能力最好
- ✓ 专门保存的最优模型

### ⚠️ 备选使用：`fer-{best_epoch}_449.ckpt`

如果 `best_model.ckpt` 有问题，可以使用 epoch checkpoints：

```bash
# 假设第 25 轮准确率最高
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints/fer-25_449.ckpt \
  --num_samples 3
```

### ❌ 不推荐：`final_model.ckpt`

- 可能已经过拟合（准确率下降）
- 不一定是最好的性能

---

## 训练完成后会生成什么？

### 50 轮训练后，`checkpoints_50epoch/` 目录：

```
checkpoints_50epoch/
├── best_model.ckpt          ← 最佳模型（准确率最高）⭐
├── final_model.ckpt         ← 最终模型
├── fer-46_449.ckpt          ← 第 46 轮
├── fer-47_449.ckpt          ← 第 47 轮
├── fer-48_449.ckpt          ← 第 48 轮
├── fer-49_449.ckpt          ← 第 49 轮
└── fer-50_449.ckpt          ← 第 50 轮
```

**为什么只有最后 5 个 epoch？**
- 配置了 `keep_checkpoint_max=5`
- 自动删除旧的 checkpoints，节省空间
- 通常最后几轮的模型最有用

---

## 如何选择最佳 epoch？

### 方法1：看训练日志

```
Epoch 20 - Validation Accuracy: 0.6543
New best accuracy: 0.6543 at epoch 20
Saved best model to: checkpoints_50epoch/best_model.ckpt  ← 这个就是最佳

Epoch 25 - Validation Accuracy: 0.6821
New best accuracy: 0.6821 at epoch 25
Saved best model to: checkpoints_50epoch/best_model.ckpt  ← 更新为更好的

Epoch 30 - Validation Accuracy: 0.6734  ← 没有提升，不保存
```

训练结束后，`best_model.ckpt` = 第 25 轮的模型（准确率最高）

### 方法2：手动测试每个 checkpoint

```bash
# 测试第 46 轮
python verify_model.py --ckpt checkpoints_50epoch/fer-46_449.ckpt

# 测试第 47 轮
python verify_model.py --ckpt checkpoints_50epoch/fer-47_449.ckpt

# ... 找到最好的
```

---

## 常见问题

### Q1: 为什么有些 checkpoint 命名不同？

A: 不同训练任务生成的：
- `fer_1-50_*.ckpt` - 第一次 50 轮训练
- `fer-5_*.ckpt` - 另一次训练（可能中断）

### Q2: 可以删除旧的 checkpoints 吗？

A: 可以，但建议保留：
- ✓ 保留：`best_model.ckpt`（必须）
- ✓ 保留：最近几个 `fer-*_449.ckpt`（备用）
- ✗ 可删除：很旧的或明显性能差的

### Q3: 为什么 best_model.ckpt 只有 434KB？

A: 旧版本的 BUG，训练代码没有正确保存。
- 解决方案：使用修复后的代码重新训练
- 临时方案：使用 `fer-5_449.ckpt` 等完整的 checkpoint

### Q4: Checkpoint 文件很大，正常吗？

A: 完全正常！
- ResNet 模型参数很多
- 正常大小：**1.2-1.5 MB**
- 如果 < 500KB：模型不完整

---

## 总结

| 问题 | 答案 |
|------|------|
| **什么是 checkpoint？** | 训练过程中保存的模型快照 |
| **命名规则** | `fer-{epoch}_{step}.ckpt` |
| **哪个最重要？** | `best_model.ckpt`（验证准确率最高） |
| **为什么有多个？** | 保留最近几轮，防止训练问题 |
| **应该用哪个？** | **best_model.ckpt**（修复后） |
| **正常大小** | **1.2-1.5 MB** |

---

## 快速命令

```bash
# 查看所有 checkpoints
ls -lh checkpoints_50epoch/*.ckpt

# 验证最佳模型
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt

# 使用最佳模型可视化
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --num_samples 3
```

记住：**优先使用 `best_model.ckpt`，这是训练过程中准确率最高的模型！** ⭐
