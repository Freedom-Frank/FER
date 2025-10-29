# OpenCV cv2.data 错误修复

## 问题

错误信息：
```
AttributeError: module 'cv2' has no attribute 'data'
```

## 原因

OpenCV 的不同版本对 `cv2.data` 属性的支持不同，某些版本或安装方式可能没有这个属性。

## ✅ 已修复

我已经更新了 `src/visualize.py` 文件，现在代码会自动尝试多种方式加载 Haar Cascade 文件：

1. 使用 `cv2.data.haarcascades`（标准方式）
2. 从 OpenCV 安装目录查找
3. 从 conda 环境的常见路径查找

## 🚀 立即测试

在 Anaconda Prompt 中运行：

```bash
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

应该可以正常工作了！🎉

## 如果还是报错

### 方案 1：重新安装 OpenCV（推荐）

```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python
```

### 方案 2：手动下载 Haar Cascade 文件

1. 下载文件：
   - 从 GitHub 下载：https://github.com/opencv/opencv/tree/master/data/haarcascades
   - 或使用项目提供的文件

2. 放到项目 `data` 目录：
   ```
   FER/data/haarcascade_frontalface_default.xml
   ```

3. 修改代码使用本地文件（已包含在修复中）

### 方案 3：检查 OpenCV 安装

```bash
# 检查 OpenCV 版本
python -c "import cv2; print(cv2.__version__)"

# 检查 cv2.data 是否可用
python -c "import cv2; print(hasattr(cv2, 'data'))"

# 查找 Haar Cascade 文件位置
python -c "import cv2, os; print(os.path.dirname(cv2.__file__))"
```

## 成功标志

修复成功后，你会看到：

```
[INFO] Loading model from checkpoints_50epoch\best_model.ckpt
[INFO] Detected classifier shape: (256, 512)
[INFO] Loading current model (512 -> 256 -> 128 -> 7)
[INFO] Visualizer initialized. Output: output/webcam
[INFO] Starting webcam 0. Press 'q' to quit, 's' to save frame
```

然后摄像头窗口会打开！🎉
