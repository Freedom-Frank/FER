# 样例生成快速入门

## 最快方式（推荐）

### 单张图片识别
```bash
python demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input your_image.jpg
```

输出：
- `output/images/your_image_annotated.jpg` - 标注后的图片
- `output/images/your_image_result.png` - 概率分布图

### 批量图片处理
```bash
python demo_visualization.py --mode batch --ckpt checkpoints/best_model.ckpt --input your_images_folder/
```

输出：
- `output/batch/` 目录下的所有处理结果
- `output/batch/statistics.png` - 统计图

## 从数据集生成样例

### 方法 1：快速脚本（最简单）
```bash
python quick_samples.py --num_samples 2
```

### 方法 2：简化脚本
```bash
python generate_samples_simple.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 2
```

### 方法 3：完整脚本（包含对比表）
```bash
python generate_samples.py \
    --csv data/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3
```

## 样例格式

```
┌─────────────────┬──────────────────────┐
│  原图48x48      │  概率分布柱状图       │
│  [人脸]         │  angry    ███ 5%     │
│                 │  disgust  █ 1%       │
│  真实: Happy    │  fear     ██ 3%      │
│  [绿/红标题]    │  happy    █████ 85%  │
│                 │  sad      █ 2%       │
│                 │  surprise ██ 3%      │
│                 │  neutral  █ 1%       │
│                 │                      │
│                 │  预测: happy (85%) ✓ │
│                 │  [绿/红标题]         │
└─────────────────┴──────────────────────┘
```

## 颜色说明

- **绿色标题**：预测正确 ✓
- **红色标题**：预测错误 ✗
- **红色柱子**：真实表情
- **橙色柱子**：错误预测的表情

## 常见问题

### Q: 生成的图片在哪里？
**A:**
- 方法1（可视化）：`output/images/` 或 `output/batch/`
- 方法2/3（数据集）：`samples_output/`

### Q: 只想生成一个表情的样例？
**A:** 使用方法1，准备该表情的图片，然后批量处理

### Q: 如何提高准确率？
**A:**
- 使用训练好的最佳模型：`checkpoints/best_model.ckpt`
- 或使用 `checkpoints/fer-5_449.ckpt`（推荐）

### Q: 脚本运行失败？
**A:** 检查：
1. 数据集是否存在：`data/FER2013/fer2013.csv`
2. 模型是否存在：`checkpoints/best_model.ckpt`
3. 依赖是否安装：`pip install -r requirements.txt`

## 更多信息

- 详细说明：[SAMPLES_README.md](SAMPLES_README.md)
- 样例示例：[SAMPLES_EXAMPLES.md](SAMPLES_EXAMPLES.md)
- 可视化指南：[docs/visualization_guide.md](docs/visualization_guide.md)
