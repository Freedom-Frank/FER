# 快速修复指南

## 问题症状

- ❌ 人脸检测失败率高
- ❌ 所有情感概率都在 13-15% 左右（接近随机）
- ❌ Happy 被错误识别为 Angry

## 快速解决方案

### 方法 1：使用正确的模型文件（最简单）✅

```bash
# 使用完整训练的模型，而不是 best_model.ckpt
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input your_image.jpg
```

**为什么？**
- `best_model.ckpt` = 434KB (不完整/未训练好)
- `fer-5_449.ckpt` = 1.3MB (完整模型) ✅

### 方法 2：替换默认模型

```bash
# 备份旧文件
mv checkpoints/best_model.ckpt checkpoints/best_model.ckpt.backup

# 复制正确的模型
cp checkpoints/fer-5_449.ckpt checkpoints/best_model.ckpt
```

现在你可以继续使用原来的命令。

### 方法 3：已应用的改进

我已经更新了 `src/visualize.py`，改进了人脸检测：

**变更：**
- ✅ `scaleFactor`: 1.1 → 1.05 (更精细的扫描)
- ✅ `minNeighbors`: 5 → 3 (更容易检测)
- ✅ `minSize`: (30, 30) → (20, 20) (检测更小的脸)

## 测试修复

```bash
# 测试单张图片
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input test.jpg

# 期望看到：
# ✓ 检测到人脸
# ✓ 最高概率 > 40% (而不是 15%)
# ✓ 正确的情感识别
```

## 验证结果

好的预测应该看起来像：
```
Emotion Probabilities:
  happy:     68.5%  ████████████████████████████████████
  neutral:   15.2%  ████████
  surprise:   8.3%  ████
  sad:        4.1%  ██
  angry:      2.0%  █
  fear:       1.5%  █
  disgust:    0.4%
```

坏的预测（使用 best_model.ckpt）：
```
Emotion Probabilities:
  angry:     15.5%  ████████
  neutral:   15.0%  ████████
  surprise:  15.0%  ████████
  sad:       14.7%  ███████
  happy:     13.0%  ███████  ← 这是随机猜测！
  fear:      12.9%  ███████
  disgust:   13.9%  ███████
```

## 文件参考

- 详细说明: [README_VISUALIZATION_FIX.md](README_VISUALIZATION_FIX.md)
- 诊断脚本: [diagnose_model.py](diagnose_model.py)
- 修复脚本: [fix_visualization.py](fix_visualization.py)

## 总结

**主要问题**：使用了未完整训练的 `best_model.ckpt` (434KB)

**解决方案**：使用 `fer-5_449.ckpt` (1.3MB)

```bash
# 一行命令修复
python3 demo_visualization.py --mode image --ckpt checkpoints/fer-5_449.ckpt --input test.jpg
```

完成！🎉
