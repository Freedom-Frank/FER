# 故障排除指南

本文档汇总所有常见问题和解决方案。

---

## 🔧 模型加载错误

### 问题描述

```
RuntimeError: For 'load_param_into_net', classifier.0.weight in the argument 'net'
should have the same shape as classifier.0.weight in the argument 'parameter_dict'.
But got its shape (256, 512) in the argument 'net' and shape (128, 128) in the
argument 'parameter_dict'.
```

### 解决方案

✅ **已自动修复**！系统会自动检测并加载正确版本的模型。

**运行时会看到：**
```
[INFO] Loading model from checkpoints/best_model.ckpt
[INFO] Detected classifier shape: (128, 128)
[INFO] Loading legacy model (128 -> 128 -> 7)
[INFO] Visualizer initialized.
```

**如果还有问题：**
1. 确认 `src/model_legacy.py` 文件存在
2. 运行测试：`python3 test_model_loading.py`

**详细说明：** [模型兼容性文档](model_compatibility.md)

---

## 🔧 USBip 安装错误

### 问题描述

```
update-alternatives: error: error creating symbolic link '/usr/local/bin/usbip.dpkg-tmp':
No such file or directory
```

### 解决方案

⚠️ **这个错误不影响核心功能**！USBip 只用于摄像头，是可选功能。

**方案 1：跳过摄像头（推荐）**
直接使用图片/视频模式，不需要摄像头：
```bash
python3 demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input IMAGE.jpg
```

**方案 2：修复 USBip**
```bash
# 创建目录
sudo mkdir -p /usr/local/bin

# 重新安装
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/5.15.0-160-generic/usbip 20
```

**方案 3：使用原生摄像头**
如果在原生 Linux 环境：
```bash
ls /dev/video*  # 检查摄像头
```

---

## 🔧 依赖安装失败

### Python 依赖问题

```bash
# 升级 pip
pip3 install --upgrade pip

# 清除缓存
pip3 cache purge

# 重新安装
pip3 install -r requirements.txt

# 或逐个安装
pip3 install mindspore
pip3 install opencv-python
pip3 install matplotlib
```

### 系统依赖问题

```bash
# 更新系统
sudo apt update

# 安装依赖
sudo apt install -y python3 python3-pip python3-dev
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

---

## 🔧 OpenCV 错误

### ImportError: libGL.so.1

```bash
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

### 重新安装 OpenCV

```bash
pip3 uninstall opencv-python
pip3 install opencv-python
```

---

## 🔧 Matplotlib 显示错误

### "no display name and no $DISPLAY"

```bash
# 设置后端
export MPLBACKEND=Agg

# 永久生效
echo 'export MPLBACKEND=Agg' >> ~/.bashrc
source ~/.bashrc
```

**注意：** 可视化脚本已使用 'Agg' 后端，无需显示窗口。

---

## 🔧 人脸检测失败

### 调整检测参数

编辑 `src/visualize.py`，修改检测参数：

```python
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,    # 减小值提高敏感度（默认 1.1）
    minNeighbors=3,      # 减小值提高敏感度（默认 5）
    minSize=(30, 30)     # 调整最小人脸尺寸
)
```

---

## 🔧 X11 显示问题

### WSL2 中无法显示窗口

1. **安装 X11**
```bash
sudo apt install -y x11-apps
```

2. **设置 DISPLAY**
```bash
export DISPLAY=:0
echo 'export DISPLAY=:0' >> ~/.bashrc
```

3. **在 Windows 安装 X Server**
- 下载 [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
- 或 [X410](https://x410.dev/)

4. **启动 X Server 并测试**
```bash
xclock  # 应该弹出时钟窗口
```

---

## 🔧 权限问题

### Permission denied

```bash
# 修改文件权限
chmod -R 755 /mnt/e/Users/Meng/Projects/VScodeProjects/FER

# 或使用 --user 安装
pip3 install --user -r requirements.txt
```

---

## 🔧 视频处理问题

### 无法保存视频

尝试不同的编码器，编辑 `src/visualize.py`：

```python
# 尝试不同的 fourcc
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 或
fourcc = cv2.VideoWriter_fourcc(*'H264')
```

### 处理速度太慢

1. 使用 GPU：`--device GPU`
2. 降低视频分辨率
3. 跳帧处理
4. 使用更小的模型

---

## 🔧 内存不足

### Out of Memory

1. 减小 batch size
2. 使用 CPU 模式
3. 分批处理大量图片
4. 关闭其他程序

---

## 🔧 GPU 相关问题

### 检查 GPU 是否可用

```bash
nvidia-smi
```

### MindSpore GPU 错误

```bash
# 检查 CUDA
nvcc --version

# 检查 MindSpore
python3 -c "import mindspore; print(mindspore.__version__)"
```

**配置 GPU：** 参考 [环境配置文档](setup.md#wsl2-gpu-配置)

---

## 📞 获取更多帮助

### 运行诊断脚本

```bash
# 测试模型加载
python3 test_model_loading.py

# 完整测试
./test_now.sh
```

### 查看日志

```bash
# 重定向错误输出
python3 demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input test.jpg 2>&1 | tee error.log
cat error.log
```

### 检查环境

```bash
# Python 版本
python3 --version

# 已安装包
pip3 list | grep -E "mindspore|opencv|matplotlib"

# 系统信息
uname -a
```

---

## 📚 相关文档

- [快速开始](getting_started.md)
- [环境配置](setup.md)
- [模型兼容性](model_compatibility.md)
- [WSL 命令清单](wsl_commands.md)

---

**还有问题？** 查看 [完整文档索引](README.md)
