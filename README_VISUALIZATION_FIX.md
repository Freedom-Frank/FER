# 可视化问题诊断与修复

## 问题分析

根据你提供的信息和检查结果，发现了以下问题：

### 1. 模型预测问题 ❌

**现象**：所有情感的概率都在 13-15% 左右，非常接近 (7 个类别的均匀分布应该是 14.3%)

**原因**：
- `best_model.ckpt` 文件大小只有 434KB，而其他 checkpoint 有 1.3MB
- 这表明 `best_model.ckpt` 可能是：
  - 一个**未训练完成**的模型
  - 一个**保存不完整**的检查点
  - 一个**错误的**模型文件

**证据**：
```
best_model.ckpt:    434KB  ← 太小！
fer-5_449.ckpt:    1.3MB   ← 正常大小
fer-5_404.ckpt:    1.3MB   ← 正常大小
```

### 2. 人脸检测问题 ⚠️

**现象**：
- 很多图片检测不到人脸
- 检测到的人脸区域有大量黑色背景

**原因**：
- Haar Cascade 检测器的参数设置过于严格
- 默认参数：`scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)`
- 这些参数在某些情况下会漏检人脸

## 解决方案

### 方案 1：使用正确的模型文件 ✅ **推荐**

```bash
# 使用完整训练的模型
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input your_image.jpg
```

### 方案 2：改进人脸检测参数

编辑 `src/visualize.py` 的人脸检测部分（第 457-459 行和其他类似位置）：

```python
# 原来的代码
faces = self.face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
)

# 改进的代码 - 使用更宽松的参数
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,      # 降低 (1.1 → 1.05) - 更精细的扫描
    minNeighbors=3,        # 降低 (5 → 3) - 更容易检测
    minSize=(20, 20),      # 降低 (30x30 → 20x20) - 检测更小的脸
    flags=cv2.CASCADE_SCALE_IMAGE
)
```

### 方案 3：使用修复脚本

我创建了一个改进的脚本 `fix_visualization.py`，它会：
1. 测试多个 checkpoint 文件
2. 使用改进的人脸检测参数
3. 显示详细的诊断信息

```bash
# 使用方法
python3 fix_visualization.py <图片路径> [checkpoint路径]

# 示例
python3 fix_visualization.py test.jpg
python3 fix_visualization.py test.jpg checkpoints/fer-5_449.ckpt
```

## 快速修复步骤

### 步骤 1：更新 visualize.py 中的默认 checkpoint

编辑 `demo_visualization.py` 第 100 行：

```python
# 改变默认使用的模型
--ckpt checkpoints/fer-5_449.ckpt  # 而不是 best_model.ckpt
```

### 步骤 2：应用人脸检测补丁

在 `src/visualize.py` 中找到所有 `detectMultiScale` 调用并替换参数：

```python
# 搜索：detectMultiScale(gray, scaleFactor=1.1
# 替换为：detectMultiScale(gray, scaleFactor=1.05
```

有 4 处需要修改：
- 第 325-327 行 (`process_webcam`)
- 第 409-411 行 (`process_video`)
- 第 457-459 行 (`process_image`)
- 第 521-523 行 (`process_batch`)

### 步骤 3：重新测试

```bash
# 测试单张图片
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input test.jpg

# 测试批量
python3 demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input test_images/
```

## 为什么 happy 被识别成 angry？

这是因为 `best_model.ckpt` 模型未正确训练。当模型输出接近均匀分布时：
- 最高概率可能只是 15.5%
- 任何微小的波动都会改变预测结果
- 实际上模型并不"知道"图片是什么表情

使用正确的模型 `fer-5_449.ckpt` 后，你应该看到：
- 最高概率至少 40-60% 以上
- 明显的概率差异
- 更准确的预测结果

## 验证修复

运行以下命令来验证：

```bash
# 1. 检查模型大小
ls -lh checkpoints/

# 2. 使用正确的模型测试
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/fer-5_449.ckpt \
  --input <your_test_image>

# 3. 检查输出
# 你应该看到：
#   - 更高的置信度 (>40%)
#   - 明显的概率分布差异
#   - 正确的情感识别
```

## 其他建议

1. **删除或重命名有问题的文件**：
   ```bash
   mv checkpoints/best_model.ckpt checkpoints/best_model.ckpt.backup
   cp checkpoints/fer-5_449.ckpt checkpoints/best_model.ckpt
   ```

2. **如果需要，重新训练模型**：
   ```bash
   python3 src/train.py \
     --data_csv data/FER2013/fer2013.csv \
     --epochs 50 \
     --batch_size 64
   ```

3. **考虑使用更好的人脸检测器**：
   - MTCNN
   - RetinaFace
   - MediaPipe Face Detection

## 总结

主要问题：
- ✅ **使用了错误/不完整的模型文件** `best_model.ckpt`
- ✅ **人脸检测参数过于严格**

解决方法：
1. 使用 `fer-5_449.ckpt` 而不是 `best_model.ckpt`
2. 调整人脸检测参数为更宽松的设置

期望结果：
- 更高的人脸检测率
- 准确的情感识别
- 清晰的概率分布（最高概率 > 40%）
