# 准备就绪 - 启动摄像头

## 已完成的修复

### ✅ 1. PIL/Pillow 兼容性 (已修复)
- 问题：`AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'`
- 修复：降级到 Pillow 9.5.0
- 状态：**已解决**

### ✅ 2. OpenCV Cascade 加载 (刚修复)
- 问题：`AttributeError: module 'cv2' has no attribute 'data'`
- 修复：在 [src/visualize.py](src/visualize.py#L73-L103) 实现了多路径回退逻辑
- 状态：**已修复，等待测试**

### ✅ 3. 摄像头检测 (已确认)
- 状态：检测到 1 个可用摄像头
- 输出：`检测到 1 个可用摄像头`

### ✅ 4. 模型加载 (已确认)
- 路径：`checkpoints_50epoch/best_model.ckpt`
- 大小：131 MB
- 架构：512 → 256 → 128 → 7
- 状态：**加载成功**

---

## 🚀 现在可以运行了！

### 在 Anaconda Prompt 中执行：

```bash
# 确保在正确的目录
cd /d E:\Users\Meng\Projects\VScodeProjects\FER

# 激活环境
conda activate fer

# 运行摄像头（使用你的模型）
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

---

## 🎯 应该看到的输出

成功启动时，你会看到：

```
[INFO] Loading model from checkpoints_50epoch/best_model.ckpt
[INFO] Detected classifier shape: (256, 512)
[INFO] Loading current model (512 -> 256 -> 128 -> 7)
[INFO] Visualizer initialized. Output: output/webcam
[INFO] Starting webcam 0. Press 'q' to quit, 's' to save frame
```

然后会打开一个窗口，显示：
- 实时摄像头画面
- 绿色方框标记人脸
- 识别的表情（7种之一）
- 置信度百分比

---

## 🎮 使用说明

### 快捷键

| 按键 | 功能 |
|------|------|
| `q` | 退出程序 |
| `s` | 保存当前帧到 `output/webcam/` |
| ESC | 也可以退出 |

### 7种表情

程序会识别以下表情：
1. 😠 angry (生气)
2. 🤢 disgust (厌恶)
3. 😨 fear (恐惧)
4. 😊 happy (高兴)
5. 😢 sad (悲伤)
6. 😮 surprise (惊讶)
7. 😐 neutral (中性)

---

## ⚠️ 如果还有错误

### OpenCV 错误
如果遇到任何 OpenCV 相关错误：

```bash
pip uninstall opencv-python
pip install opencv-python
```

然后重新运行。

### 完整诊断
运行诊断脚本检查所有依赖：

```bash
python diagnose.py
```

### 测试单独组件

```bash
# 测试摄像头
python test_camera.py

# 测试模型
python test_model.py

# 测试 Cascade 加载
python test_cascade.py
```

---

## 📁 修改的文件

本次修复只修改了一个文件：

- **[src/visualize.py](src/visualize.py#L73-L103)**: 增强 Haar Cascade 加载逻辑
  - 添加了 3 种回退方法
  - 处理 `cv2.data` 不存在的情况
  - 支持 Windows、Linux、conda 等多种环境

**变更摘要**：
```python
# 旧代码（单一路径，容易失败）：
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

# 新代码（多路径回退，更健壮）：
try:
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
except AttributeError:
    # 尝试多个备用路径...
```

---

## 🎉 预期结果

一切正常的话，你会看到：

1. **模型加载信息** - 几秒钟内完成
2. **摄像头窗口打开** - 显示实时画面
3. **人脸检测** - 绿色方框
4. **表情识别** - 实时显示情绪标签
5. **FPS 显示** - 右上角（约 15-30 FPS）

---

## 📚 相关文档

- [OPENCV_FIX.md](OPENCV_FIX.md) - OpenCV 错误详细说明
- [FIX_PIL_ERROR.md](FIX_PIL_ERROR.md) - PIL 错误修复指南
- [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md) - 完整使用指南
- [START_WEBCAM_WINDOWS.txt](START_WEBCAM_WINDOWS.txt) - Windows 快速指南

---

## ✨ 快捷启动

如果你希望一键启动，使用这些脚本：

### Windows:
```bash
run_webcam_conda.bat
```
或
```bash
fix_and_run.bat
```

### Linux/WSL:
```bash
bash run_webcam.sh
```

---

## 💡 性能优化提示

### CPU 模式（默认）
```bash
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt --device CPU
```

### GPU 模式（如果有 NVIDIA GPU）
```bash
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt --device GPU
```

GPU 模式会更快，但需要：
- NVIDIA GPU
- CUDA 支持
- MindSpore GPU 版本

---

## 🐛 问题排查

### 问题 1：摄像头无法打开
- **检查**：摄像头是否被其他程序占用（Zoom、Teams 等）
- **测试**：`python test_camera.py`

### 问题 2：人脸检测不到
- **原因**：光线太暗、人脸角度、距离太远
- **解决**：调整光线、正对摄像头、距离适中

### 问题 3：识别不准确
- **原因**：模型基于 FER2013 数据集，有一定局限性
- **说明**：这是正常的，表情识别本身是一个有挑战的任务

### 问题 4：FPS 太低
- **原因**：CPU 处理速度限制
- **解决**：
  1. 使用 GPU 模式（如果可用）
  2. 降低摄像头分辨率
  3. 关闭其他占用 CPU 的程序

---

## 🎊 准备好了吗？

所有修复已完成，现在执行：

```bash
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

**祝使用愉快！** 🚀

---

*最后更新：修复 OpenCV Cascade 加载问题*
*所有依赖：Python, OpenCV, MindSpore, Pillow 9.5.0*
