# WSL 摄像头配置指南

## 问题说明

你遇到的错误：
```
[ERROR] Cannot open webcam
VIDEOIO(V4L2:/dev/video0): can't open camera by index
```

这是因为 **WSL (Windows Subsystem for Linux) 默认不支持 USB 设备访问**，包括摄像头。

## 解决方案

### 方案 1：在 Windows 上运行（推荐 - 最简单）

**直接在 Windows 环境下运行摄像头功能**：

1. **打开 Windows PowerShell 或 CMD**

2. **进入项目目录**：
   ```powershell
   cd E:\Users\Meng\Projects\VScodeProjects\FER
   ```

3. **激活 Python 环境**（如果有的话）：
   ```powershell
   # 如果使用 conda
   conda activate fer

   # 或使用 venv
   .\.venv\Scripts\activate
   ```

4. **运行摄像头功能**：
   ```powershell
   # 一键启动
   .\run_webcam.bat

   # 或手动运行
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
   ```

**优点**：
- ✅ 最简单，无需额外配置
- ✅ 摄像头直接可用
- ✅ 性能好

**缺点**：
- ❌ 只能使用 CPU（Windows 下 MindSpore 不支持 GPU）

---

### 方案 2：使用 WSLg（Windows 11）

如果你使用的是 **Windows 11** 并且已经安装了 WSLg，可以尝试：

1. **更新 WSL**：
   ```powershell
   # 在 Windows PowerShell (管理员) 中运行
   wsl --update
   wsl --shutdown
   ```

2. **检查 WSLg 版本**：
   ```bash
   # 在 WSL 中运行
   wslg --version
   ```

3. **安装 USB 支持**（实验性功能）：

   参考官方文档：https://learn.microsoft.com/en-us/windows/wsl/connect-usb

4. **尝试运行**：
   ```bash
   python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt --device GPU
   ```

**优点**：
- ✅ 可以使用 GPU
- ✅ Linux 环境

**缺点**：
- ❌ 配置复杂
- ❌ 需要 Windows 11
- ❌ USB 支持是实验性功能，可能不稳定

---

### 方案 3：使用 IP 摄像头（远程方案）

如果你有 Android/iOS 手机，可以将手机作为网络摄像头：

1. **安装手机 APP**：
   - Android: "IP Webcam" 或 "DroidCam"
   - iOS: "EpocCam" 或 "iVCam"

2. **在 WSL 中使用网络流**：

   修改代码以支持 RTSP/HTTP 流（需要修改 `demo_visualization.py`）

**优点**：
- ✅ 可以在 WSL 中使用
- ✅ 可以使用 GPU

**缺点**：
- ❌ 需要额外的手机和 APP
- ❌ 可能有延迟
- ❌ 需要修改代码

---

### 方案 4：使用虚拟摄像头（开发/测试）

如果只是测试功能，可以使用虚拟摄像头：

1. **在 Windows 上安装 OBS Studio**

2. **配置 OBS Virtual Camera**

3. **在 WSL 中通过 USB/IP 转发使用**

**优点**：
- ✅ 可以测试功能
- ✅ 可以录制固定视频进行测试

**缺点**：
- ❌ 配置非常复杂
- ❌ 不是真实摄像头

---

## 推荐方案对比

| 方案 | 难度 | GPU | 摄像头 | 推荐度 |
|-----|------|-----|--------|--------|
| Windows (方案1) | ⭐ | ❌ | ✅ | ⭐⭐⭐⭐⭐ |
| WSLg (方案2) | ⭐⭐⭐⭐ | ✅ | ⚠️ | ⭐⭐ |
| IP摄像头 (方案3) | ⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐ |
| 虚拟摄像头 (方案4) | ⭐⭐⭐⭐⭐ | ✅ | ⚠️ | ⭐ |

---

## 🎯 立即解决方案（最推荐）

### 直接在 Windows 上运行

**步骤 1：在 Windows PowerShell 中进入项目目录**

```powershell
cd E:\Users\Meng\Projects\VScodeProjects\FER
```

**步骤 2：检查 Python 环境**

```powershell
# 检查 Python
python --version

# 检查依赖
python -c "import cv2, mindspore; print('OK')"
```

如果提示缺少模块：
```powershell
pip install opencv-python mindspore
```

**步骤 3：运行摄像头功能**

```powershell
# 最简单的方式 - 双击
.\run_webcam.bat

# 或命令行
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

**步骤 4：测试摄像头**

```powershell
python test_camera.py
```

---

## 其他可视化功能（无需摄像头）

如果暂时无法使用摄像头，你仍然可以使用其他功能：

### 1. 图片处理

```bash
# WSL 中运行（GPU加速）
python tools/demo_visualization.py \
  --mode image \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test.jpg \
  --device GPU
```

### 2. 视频文件处理

```bash
python tools/demo_visualization.py \
  --mode video \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test.mp4 \
  --device GPU
```

### 3. 批量处理

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input test_images/ \
  --device GPU
```

### 4. CSV 批量评估（推荐）

```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

---

## 快速测试脚本

创建一个测试脚本来验证所有功能：

```bash
# 在 WSL 中创建测试脚本
cat > test_all_features.sh << 'EOF'
#!/bin/bash
echo "测试 FER 项目功能"
echo "================================"

# 1. 测试模型加载
echo "1. 测试模型加载..."
python test_model.py

# 2. 测试 CSV 评估（无需摄像头）
echo "2. 测试 CSV 评估（从数据集随机选择10个样本）..."
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU \
  --limit 10

echo "================================"
echo "测试完成！"
EOF

chmod +x test_all_features.sh
./test_all_features.sh
```

---

## Windows 环境配置（如果需要）

如果你的 Windows 环境还没有配置好：

1. **安装 Python**（如果没有）：
   - 下载：https://www.python.org/downloads/
   - 确保勾选 "Add Python to PATH"

2. **安装依赖**：
   ```powershell
   pip install mindspore opencv-python numpy matplotlib
   ```

3. **验证安装**：
   ```powershell
   python test_model.py
   python test_camera.py
   ```

---

## 总结

**最佳实践**：

1. **实时摄像头** → 在 Windows 上运行（方案 1）
2. **GPU 训练/评估** → 在 WSL 中运行
3. **图片/视频处理** → WSL 或 Windows 都可以

**推荐工作流程**：

```bash
# WSL - 用于训练和批量评估（GPU）
python src/train.py --data_csv data.csv --device GPU
python src/batch_eval_csv.py --csv data.csv --ckpt model.ckpt --device GPU

# Windows - 用于实时摄像头演示（CPU）
run_webcam.bat
```

---

## 需要帮助？

如果遇到其他问题：

1. **查看完整文档**: [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md)
2. **查看常见问题**: [docs/troubleshooting.md](docs/troubleshooting.md)
3. **测试摄像头**: `python test_camera.py`
4. **测试模型**: `python test_model.py`

---

## 快速命令参考

```bash
# Windows PowerShell
cd E:\Users\Meng\Projects\VScodeProjects\FER
.\run_webcam.bat

# WSL - 其他功能
python test_model.py
python src/batch_eval_csv.py --csv data.csv --ckpt checkpoints_50epoch/best_model.ckpt --device GPU
```

祝使用愉快！ 🎉
