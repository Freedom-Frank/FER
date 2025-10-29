# 模型文件说明

## 模型目录结构

你的项目有以下模型目录：

```
FER/
├── checkpoints_50epoch/           # 50轮训练的模型（推荐使用）
│   ├── best_model.ckpt           # 最佳模型 (131MB) ⭐ 推荐
│   ├── final_model.ckpt          # 最终模型 (44MB)
│   └── fer-*.ckpt                # 各个epoch的检查点
│
└── checkpoints/                   # 其他训练的模型
    ├── best_model.ckpt           # 最佳模型
    └── fer-*.ckpt                # 各个epoch的检查点
```

## 推荐使用的模型

### 1. checkpoints_50epoch/best_model.ckpt ⭐ 推荐

这是经过 50 轮训练后性能最好的模型：

- **文件大小**: 131MB
- **训练轮数**: 50 epochs
- **特点**: 完整模型，包含所有参数
- **使用场景**:
  - 实时摄像头识别
  - 图片/视频处理
  - 批量评估

**使用方法**：
```bash
# 实时摄像头
python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt

# 图片处理
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg

# 批量评估
python src/batch_eval_csv.py --csv data/FER2013/fer2013.csv --ckpt checkpoints_50epoch/best_model.ckpt
```

### 2. checkpoints_50epoch/final_model.ckpt

这是第 50 轮训练结束时的模型：

- **文件大小**: 44MB
- **特点**: 可能是简化版本或不同保存格式
- **使用场景**: 如果遇到内存限制可以尝试使用

## 模型性能对比

根据你的训练记录：

| 模型 | 训练轮数 | 文件大小 | 推荐程度 | 备注 |
|------|---------|---------|---------|------|
| checkpoints_50epoch/best_model.ckpt | 50 | 131MB | ⭐⭐⭐⭐⭐ | 最佳选择 |
| checkpoints/best_model.ckpt | 不详 | 变化 | ⭐⭐⭐ | 备用选择 |

## 自动模型选择

一键启动脚本会按以下优先级自动查找模型：

1. `checkpoints_50epoch/best_model.ckpt` ⭐ 优先
2. `checkpoints/best_model.ckpt`
3. `checkpoints_50epoch/fer-50_299.ckpt`
4. `checkpoints/fer-5_449.ckpt`

只需运行：
```bash
# Windows
run_webcam.bat

# Linux/WSL
bash run_webcam.sh
```

脚本会自动找到最合适的模型并使用。

## 训练新模型

如果你想训练新的模型：

```bash
# 完整优化训练（推荐）
python src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 200 \
  --lr 7e-4 \
  --patience 30 \
  --weight_decay 3e-5 \
  --label_smoothing 0.12 \
  --augment \
  --mixup \
  --mixup_alpha 0.4 \
  --save_dir checkpoints_200epoch
```

训练完成后，模型会保存在指定的 `save_dir` 目录中。

## 模型评估

评估模型性能：

```bash
# 在测试集上评估
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --device_target GPU

# CSV批量评估（无漏检）
python src/batch_eval_csv.py \
  --csv data/FER2013/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

## 模型兼容性

所有模型都支持自动版本检测：

- 可视化脚本会自动检测模型版本（新版 vs 旧版）
- 自动加载正确的模型架构
- 无需手动指定模型类型

详见 [docs/model_compatibility.md](docs/model_compatibility.md)

## 常见问题

### Q: 为什么 best_model.ckpt 是 131MB？

这是完整的模型文件，包含：
- 模型权重
- 优化器状态
- 训练历史信息

### Q: 可以删除其他 epoch 的检查点吗？

可以。如果磁盘空间有限，只保留：
- `best_model.ckpt` - 用于实际使用
- 最后几个 epoch 的检查点 - 用于故障恢复

### Q: 如何知道哪个模型性能最好？

查看训练日志或运行评估脚本：

```bash
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --device_target GPU
```

会输出准确率、精确率、召回率等指标。

## 下一步

- **使用模型**: 查看 [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md)
- **训练指南**: 查看 [docs/guides/training_guide.md](docs/guides/training_guide.md)
- **评估方法**: 查看 [README.md](README.md#评估脚本-srcevalpy)
