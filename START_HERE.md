# 🚀 快速开始 - 从这里开始！

## 第一步：进入项目目录

**这是最重要的一步！所有命令都必须在项目目录下运行。**

### Windows CMD
```bash
cd /d E:\Users\Meng\Projects\VScodeProjects\FER
```

### Windows PowerShell
```bash
cd E:\Users\Meng\Projects\VScodeProjects\FER
```

### WSL2/Linux
```bash
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER
```

### 确认位置
```bash
pwd
# 应该输出项目路径
```

---

## 第二步：检查环境

```bash
# 检查 MindSpore
python -c "import mindspore; print('MindSpore:', mindspore.__version__)"

# 检查数据集存在
# WSL2:
ls /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv

# Windows:
dir E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv
```

如果报错，查看 [环境配置文档](docs/setup.md)

---

## 第三步：训练模型

### 🔥 GPU用户（推荐，50-100分钟）

```bash
bash train_50_epochs.sh
```

### 💻 CPU用户（8-16小时）

```bash
# Windows: 双击运行
train_50_epochs.bat

# 或在CMD中运行：
train_50_epochs.bat
```

---

## 第四步：验证模型

训练完成后：

```bash
# 检查文件大小（应该约1.3MB）
ls -lh checkpoints_50epoch/best_model.ckpt

# 运行验证工具
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt
```

**期望看到**：
- ✓ File size: 1.3 MB
- ✓ Model produces non-uniform predictions
- ✓ VERDICT: Model appears to be WORKING!

---

## 第五步：生成可视化

### WSL2/Linux (GPU)
```bash
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --device GPU \
  --num_samples 3
```

### Windows (CPU)
```bash
python tools\generate_correct_samples.py --csv E:\Users\Meng\Datasets\FER2013CSV\fer2013.csv --ckpt checkpoints_50epoch\best_model.ckpt --num_samples 3
```

**结果**：在 `visualization_samples/` 或 `correct_samples/` 目录查看

---

## 🎉 完成！

现在你应该有：
- ✓ 训练好的模型（1.3MB）
- ✓ 可视化样例展示
- ✓ 正常的概率分布（不是14.3%均匀分布）

---

## 📚 更多功能

### 单张图片可视化
```bash
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg
```

### 批量处理
```bash
python tools/demo_visualization.py --mode batch --ckpt checkpoints_50epoch/best_model.ckpt --input test_images/
```

### 实时摄像头
```bash
python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt
```

---

## ❓ 遇到问题？

### 问题1: 找不到模块
**确保你在项目目录下！**重新执行第一步。

### 问题2: 模型概率是14.3%
说明模型没训练好，检查：
- 模型文件大小是否 >1MB？
- 训练时是否看到 "Saved best model to..." 消息？

### 问题3: 内存不足
减小 batch_size：
- 编辑 `train_50_epochs.sh` 或 `train_50_epochs.bat`
- 将 `batch_size` 从 96 改为 64 或 32

---

## 📖 详细文档

- **完整工作流程**: [COMPLETE_WORKFLOW.md](COMPLETE_WORKFLOW.md)
- **快速命令清单**: [QUICK_COMMANDS.txt](QUICK_COMMANDS.txt)
- **50轮训练指南**: [TRAINING_GUIDE_50_EPOCHS.md](TRAINING_GUIDE_50_EPOCHS.md)
- **模型保存修复**: [MODEL_SAVE_FIX.md](MODEL_SAVE_FIX.md)

---

## 🆘 快速帮助

```bash
# 完整流程（一次性运行所有命令）
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER
bash train_50_epochs.sh
python verify_model.py --ckpt checkpoints_50epoch/best_model.ckpt
python tools/generate_correct_samples.py --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv --ckpt checkpoints_50epoch/best_model.ckpt --device GPU --num_samples 3
```

**就这么简单！** 🎊
