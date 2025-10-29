# 📍 FER2013 项目导航

> 快速找到你需要的文档和功能

## 🎯 我想要...

### 快速开始使用
→ **[START_HERE.md](START_HERE.md)** ⭐ 5分钟上手

### 训练模型
→ **[docs/guides/training_guide.md](docs/guides/training_guide.md)** - 50轮训练方案
→ **[docs/reference/quick_commands.txt](docs/reference/quick_commands.txt)** - 命令速查

### 生成可视化
→ **[docs/guides/final_guide.md](docs/guides/final_guide.md)** - 第2步
→ **[docs/visualization_guide.md](docs/visualization_guide.md)** - 完整说明

### 理解Checkpoint
→ **[docs/guides/checkpoint_guide.md](docs/guides/checkpoint_guide.md)** - 文件说明

### 解决问题
→ **[docs/troubleshooting.md](docs/troubleshooting.md)** - 故障排除
→ **[docs/guides/model_save_fix.md](docs/guides/model_save_fix.md)** - 模型问题

### 查找命令
→ **[docs/reference/quick_commands.txt](docs/reference/quick_commands.txt)** - 所有命令

---

## 📚 文档分类

### 核心入口
- **[README.md](README.md)** - 项目主页
- **[START_HERE.md](START_HERE.md)** - 快速开始
- **[docs/README.md](docs/README.md)** - 文档中心

### 使用指南
- [docs/guides/training_guide.md](docs/guides/training_guide.md)
- [docs/guides/complete_workflow.md](docs/guides/complete_workflow.md)
- [docs/guides/checkpoint_guide.md](docs/guides/checkpoint_guide.md)
- [docs/guides/model_save_fix.md](docs/guides/model_save_fix.md)
- [docs/guides/final_guide.md](docs/guides/final_guide.md)

### 快速参考
- [docs/reference/quick_commands.txt](docs/reference/quick_commands.txt)
- [docs/quick-reference/visualization.md](docs/quick-reference/visualization.md)

### 其他文档
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/visualization_guide.md](docs/visualization_guide.md)
- [docs/setup.md](docs/setup.md)

---

## ⚡ 最常用命令

### 训练
```bash
bash scripts/training/train_gpu.sh
```

### 验证
```bash
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt
```

### 可视化
```bash
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints/fer-5_449.ckpt \
  --device GPU \
  --num_samples 3
```

---

**[返回主页](README.md)** | **[文档中心](docs/README.md)** | **[快速开始](START_HERE.md)**
