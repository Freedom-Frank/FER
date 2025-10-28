# 快速开始指南

欢迎使用 FER2013 面部表情识别项目！

---

## ⚡ 3 步开始

### 步骤 1: 打开 WSL
```powershell
wsl
```

### 步骤 2: 进入项目
```bash
cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER
```

### 步骤 3: 运行测试
```bash
# 使用交互式脚本（推荐）
./quick_start.sh

# 或快速测试
./test_now.sh
```

---

## 📖 主要功能

### 🎨 可视化功能

**单张图片处理：**
```bash
python3 demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input YOUR_IMAGE.jpg
```

**批量处理：**
```bash
python3 demo_visualization.py --mode batch --ckpt checkpoints/best_model.ckpt --input YOUR_FOLDER/
```

**视频处理：**
```bash
python3 demo_visualization.py --mode video --ckpt checkpoints/best_model.ckpt --input YOUR_VIDEO.mp4
```

**详细文档：** [可视化完整指南](visualization_guide.md)

### 🏋️ 模型训练

```bash
# GPU 训练（推荐）
python3 src/train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --epochs 200 --augment --mixup

# CPU 训练
python3 src/train.py --data_csv data/FER2013/fer2013.csv --epochs 50
```

**详细文档：** [训练指南](quickstart.md)

---

## 🔧 常见问题

### 模型加载错误
如果遇到 `classifier.0.weight` 错误：
- ✅ **已自动修复**！直接运行即可
- 📖 详情：[问题修复](troubleshooting.md#模型加载错误)

### USBip 错误
- ⚠️ 不影响核心功能，可跳过
- 📖 详情：[问题修复](troubleshooting.md#usbip-错误)

### 更多问题
查看 [完整故障排除指南](troubleshooting.md)

---

## 📚 文档导航

- [可视化完整指南](visualization_guide.md)
- [环境配置](setup.md)
- [模型优化](optimization.md)
- [故障排除](troubleshooting.md)
- [所有文档](README.md)

---

返回 [项目主页](../README.md)
