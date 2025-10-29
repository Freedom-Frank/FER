# 🚀 FER2013 项目 - 5分钟快速开始

欢迎使用 FER2013 面部表情识别项目！这是一个快速入门指南,帮助你在 5 分钟内开始使用。

## 📋 你想做什么？

### 🎥 1. 我想立即试用摄像头功能

**最快方式**（Windows）：
```bash
run_webcam.bat
```

**手动方式**：
```bash
# 1. 激活环境（如果使用 conda）
conda activate fer

# 2. 运行摄像头
python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt
```

**操作指南**：
- 按 `q` 退出
- 按 `s` 保存截图

**遇到问题？**
- WSL 用户：[docs/setup/WSL_WEBCAM_SETUP.md](docs/setup/WSL_WEBCAM_SETUP.md)
- PIL 错误：[docs/troubleshooting/FIX_PIL_ERROR.md](docs/troubleshooting/FIX_PIL_ERROR.md)
- OpenCV 错误：[docs/troubleshooting/OPENCV_FIX.md](docs/troubleshooting/OPENCV_FIX.md)
- 综合诊断：`python diagnose.bat`

**详细指南**：[docs/guides/WEBCAM_GUIDE.md](docs/guides/WEBCAM_GUIDE.md)

---

### 🖼️ 2. 我想测试单张图片

```bash
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg
```

结果保存在 `output/image/` 目录。

---

### 📁 3. 我想批量处理图片

**方式 1：处理目录**
```bash
python tools/demo_visualization.py --mode batch --ckpt checkpoints_50epoch/best_model.ckpt --input test_images/
```

**方式 2：CSV 批量评估**
```bash
python src/batch_eval_csv.py \
  --csv /path/to/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --device CPU
```

详细说明：[docs/guides/QUICK_START_BATCH.md](docs/guides/QUICK_START_BATCH.md)

---

### 🎓 4. 我想训练模型

```bash
python train.py \
  --data_csv /path/to/fer2013.csv \
  --epochs 50 \
  --batch_size 64 \
  --lr 7e-4 \
  --device_target GPU \
  --augment \
  --mixup
```

完整训练指南：查看 [README.md](README.md) 的"核心脚本说明"部分

---

### 🎬 5. 我想处理视频文件

```bash
python tools/demo_visualization.py --mode video --ckpt checkpoints_50epoch/best_model.ckpt --input video.mp4
```

---

## 🛠️ 常用命令速查

| 功能 | 命令 |
|------|------|
| 摄像头（快捷） | `run_webcam.bat` |
| 摄像头（手动） | `python tools/demo_visualization.py --mode webcam --ckpt <模型>` |
| 单张图片 | `python tools/demo_visualization.py --mode image --ckpt <模型> --input <图片>` |
| 批量处理 | `python tools/demo_visualization.py --mode batch --ckpt <模型> --input <目录>` |
| 视频处理 | `python tools/demo_visualization.py --mode video --ckpt <模型> --input <视频>` |
| 系统诊断 | `python diagnose.bat` 或 `python scripts/tests/diagnose.py` |
| 摄像头测试 | `python scripts/tests/test_camera.py` |
| 模型测试 | `python scripts/tests/test_model.py` |

---

## 📚 文档导航

### 新手必读
- **[README.md](README.md)** - 完整项目文档
- [docs/quickref/READY_TO_RUN.md](docs/quickref/READY_TO_RUN.md) - 摄像头功能准备指南
- [docs/setup/WINDOWS_SETUP.md](docs/setup/WINDOWS_SETUP.md) - Windows 环境配置

### 使用指南
- [docs/guides/WEBCAM_GUIDE.md](docs/guides/WEBCAM_GUIDE.md) - 摄像头完整使用指南
- [docs/guides/QUICK_START_BATCH.md](docs/guides/QUICK_START_BATCH.md) - 批量处理指南
- [docs/guides/QUICK_START_CSV_BATCH.md](docs/guides/QUICK_START_CSV_BATCH.md) - CSV 批量评估

### 问题解决
- [docs/troubleshooting/FIX_PIL_ERROR.md](docs/troubleshooting/FIX_PIL_ERROR.md) - PIL/Pillow 错误
- [docs/troubleshooting/OPENCV_FIX.md](docs/troubleshooting/OPENCV_FIX.md) - OpenCV 错误
- [docs/troubleshooting/QUICK_FIX_WSL_WEBCAM.md](docs/troubleshooting/QUICK_FIX_WSL_WEBCAM.md) - WSL 快速修复
- [docs/setup/WSL_WEBCAM_SETUP.md](docs/setup/WSL_WEBCAM_SETUP.md) - WSL 完整配置

### 快速参考
- [docs/quickref/WEBCAM_QUICKREF.txt](docs/quickref/WEBCAM_QUICKREF.txt) - 摄像头快速参考卡
- [docs/quickref/START_WEBCAM_WINDOWS.txt](docs/quickref/START_WEBCAM_WINDOWS.txt) - Windows 启动指南
- [docs/quickref/FINAL_STATUS.txt](docs/quickref/FINAL_STATUS.txt) - 项目最终状态报告

### 技术参考
- [docs/reference/MODEL_INFO.md](docs/reference/MODEL_INFO.md) - 模型详细信息
- [docs/reference/WEBCAM_IMPLEMENTATION_SUMMARY.md](docs/reference/WEBCAM_IMPLEMENTATION_SUMMARY.md) - 实现细节
- [docs/reference/UPDATES_SUMMARY.md](docs/reference/UPDATES_SUMMARY.md) - 更新历史

---

## 🎯 表情类别

模型可识别 7 种表情：
1. 😠 **angry** (生气)
2. 🤢 **disgust** (厌恶)
3. 😨 **fear** (恐惧)
4. 😊 **happy** (高兴)
5. 😢 **sad** (悲伤)
6. 😮 **surprise** (惊讶)
7. 😐 **neutral** (中性)

---

## 💡 快速提示

### 模型位置
项目包含两个模型目录：
- `checkpoints/` - 5 轮训练的模型
- `checkpoints_50epoch/` - 50 轮训练的模型（**推荐使用**）

### 输出位置
所有结果保存在 `output/` 目录：
- `output/webcam/` - 摄像头截图
- `output/image/` - 单图处理结果
- `output/batch/` - 批量处理结果
- `output/video/` - 视频处理结果

### 性能优化
- **CPU 模式**（默认）：`--device CPU` 或 `--device_target CPU`
- **GPU 模式**（需 NVIDIA GPU + CUDA）：`--device GPU` 或 `--device_target GPU`

---

## ❓ 遇到问题？

### 常见错误快速修复

**1. PIL/Pillow 错误**
```bash
pip install Pillow==9.5.0
```

**2. OpenCV 错误**
```bash
pip uninstall opencv-python
pip install opencv-python
```

**3. WSL 摄像头无法打开**
→ 在 Windows 上运行，不要在 WSL 中运行

**4. conda 命令不可用**
→ 使用 Anaconda Prompt 而不是普通 PowerShell

**5. 综合诊断**
```bash
python diagnose.bat  # Windows
python scripts/tests/diagnose.py  # 直接调用
```

---

## 📞 获取帮助

1. **查看详细文档**：[README.md](README.md)
2. **常见问题**：README.md 的"常见问题 FAQ"部分
3. **运行诊断**：`python diagnose.bat` 获取系统状态
4. **查看项目结构**：[PROJECT_RESTRUCTURE_PLAN.md](PROJECT_RESTRUCTURE_PLAN.md)

---

## 🎉 开始使用

现在你已经掌握了基础知识，选择上面的任一功能开始体验吧！

**推荐从摄像头功能开始**：
```bash
run_webcam.bat
```

祝使用愉快！ 🚀
