# WSL 摄像头问题 - 快速解决方案

## 问题

你在 WSL 中遇到的错误：
```
[ERROR] Cannot open webcam
VIDEOIO(V4L2:/dev/video0): can't open camera by index
```

## 原因

**WSL (Windows Subsystem for Linux) 默认不支持 USB 设备**，包括摄像头。

这是 WSL 的架构限制，不是你的代码或配置问题。

## ✅ 最简单的解决方案（推荐）

### 在 Windows 上运行实时摄像头功能

#### 步骤 1：打开 Windows PowerShell

按 `Win + X`，选择 "Windows PowerShell" 或 "终端"

#### 步骤 2：进入项目目录

```powershell
cd E:\Users\Meng\Projects\VScodeProjects\FER
```

#### 步骤 3：运行摄像头功能

```powershell
# 最简单 - 双击或运行
.\run_webcam.bat
```

就这么简单！摄像头会立即工作。

## 工作流程建议

### 最佳实践：分工使用 WSL 和 Windows

**WSL 用于**（GPU加速）：
```bash
# 训练模型
python src/train.py --data_csv data.csv --device GPU

# 批量评估
python src/batch_eval_csv.py --csv data.csv --ckpt model.ckpt --device GPU

# 图片/视频处理
python tools/demo_visualization.py --mode image --ckpt model.ckpt --input test.jpg --device GPU
```

**Windows 用于**（摄像头）：
```powershell
# 实时摄像头演示
.\run_webcam.bat
```

## 快速测试命令

### 在 WSL 中（不需要摄像头）

```bash
# 测试模型
python test_model.py

# CSV 批量评估（推荐 - 无需摄像头）
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

### 在 Windows PowerShell 中

```powershell
cd E:\Users\Meng\Projects\VScodeProjects\FER

# 测试摄像头
python test_camera.py

# 运行实时识别
.\run_webcam.bat
```

## 为什么不推荐在 WSL 中配置 USB 摄像头？

1. **配置复杂**：需要 USB/IP 支持，配置步骤繁琐
2. **不稳定**：WSL 的 USB 支持仍是实验性功能
3. **性能问题**：可能有延迟和兼容性问题
4. **没有必要**：Windows 上运行摄像头功能更简单、更稳定

## 完整文档

- **详细配置指南**：[WSL_WEBCAM_SETUP.md](WSL_WEBCAM_SETUP.md)
- **使用指南**：[WEBCAM_GUIDE.md](WEBCAM_GUIDE.md)
- **快速参考**：[WEBCAM_QUICKREF.txt](WEBCAM_QUICKREF.txt)

## 总结

✅ **在 Windows 上运行摄像头** = 简单 + 稳定 + 即用

```powershell
cd E:\Users\Meng\Projects\VScodeProjects\FER
.\run_webcam.bat
```

就是这么简单！🎉
