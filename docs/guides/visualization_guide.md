# 可视化功能完整指南

FER2013 可视化功能使用指南（适用于 WSL/Linux 环境）。

---

## 🎨 功能概览

- ✅ 单张图片处理
- ✅ 批量图片处理
- ✅ 视频文件处理
- ✅ 实时摄像头识别（可选）
- ✅ GPU 加速支持

---

## 🚀 快速开始

### 方法 1: 使用交互式脚本（推荐）

```bash
./quick_start.sh
```

然后按提示选择功能。

### 方法 2: 直接运行命令

```bash
# 处理单张图片
python3 demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input photo.jpg

# 批量处理
python3 demo_visualization.py --mode batch --ckpt checkpoints/best_model.ckpt --input photos/

# 处理视频
python3 demo_visualization.py --mode video --ckpt checkpoints/best_model.ckpt --input video.mp4

# GPU 加速
python3 demo_visualization.py --mode batch --ckpt checkpoints/best_model.ckpt --input photos/ --device GPU
```

---

## 📖 详细使用说明

### 1️⃣ 单张图片处理

**基础用法：**
```bash
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/best_model.ckpt \
  --input /path/to/image.jpg
```

**输出文件：**
- `output/images/image_annotated.jpg` - 标注图（带边框和标签）
- `output/images/image_result.png` - 分析图（人脸 + 概率图）

**显示内容：**
- 检测到的人脸数量
- 每个人脸的表情和置信度
- 保存路径

---

### 2️⃣ 批量图片处理

**基础用法：**
```bash
python3 demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /path/to/images/
```

**输出文件：**
- `output/batch/image1_result.jpg` - 每张图片的标注结果
- `output/batch/statistics.png` - 表情分布统计图

**统计信息：**
```
[STATISTICS]
  happy: 25
  neutral: 7
  sad: 8
  angry: 3
  surprise: 4
  fear: 2
  disgust: 1
```

---

### 3️⃣ 视频文件处理

**基础用法：**
```bash
python3 demo_visualization.py \
  --mode video \
  --ckpt checkpoints/best_model.ckpt \
  --input video.mp4
```

**高级选项：**
```bash
python3 src/visualize.py \
  --mode video \
  --ckpt_path checkpoints/best_model.ckpt \
  --input video.mp4 \
  --save_video \
  --output_dir output/videos
```

**处理信息：**
```
[INFO] Processing video: video.mp4
[INFO] Video: 1920x1080 @ 30fps, 3600 frames
[PROGRESS] 25.0% (900/3600) - FPS: 12.8 - ETA: 211s
[SAVE] Video saved to output/videos/processed_20241027_120000.mp4
```

---

### 4️⃣ 实时摄像头识别（可选）

**注意：** 需要配置摄像头，参考 [故障排除](troubleshooting.md#usbip-错误)

```bash
python3 demo_visualization.py \
  --mode webcam \
  --ckpt checkpoints/best_model.ckpt
```

**操作说明：**
- 按 `q` 退出
- 按 `s` 保存当前帧

**显示内容：**
- 实时人脸检测框
- 表情标签和置信度
- 概率条形图
- FPS 计数器

---

## 🎨 可视化元素

### 彩色边界框

不同表情使用不同颜色：

| 表情 | 颜色 |
|------|------|
| 😠 angry | 🔴 红色 |
| 🤢 disgust | 🟢 绿色 |
| 😨 fear | 🟣 品红 |
| 😊 happy | 🟡 黄色 |
| 😢 sad | 🔵 蓝色 |
| 😮 surprise | 🟠 橙色 |
| 😐 neutral | ⚪ 灰色 |

### 概率条形图

实时显示 7 种表情的概率分布。

### 统计图表

批量处理时生成表情分布柱状图。

---

## ⚡ 性能优化

### GPU 加速

```bash
# 使用 GPU（速度提升 5-10 倍）
python3 demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input photos/ \
  --device GPU
```

### 性能对比

| 任务 | CPU (i7) | GPU (RTX 3060) | 加速比 |
|------|----------|----------------|--------|
| 单张图片 (1080p) | 0.8s | 0.15s | 5.3x |
| 批量 100 张 | 85s | 16s | 5.3x |
| 视频 (1080p, 30fps) | 3-5 FPS | 15-25 FPS | 5x |

### 优化建议

1. **使用 GPU**: 在 WSL2 中配置 CUDA
2. **降低分辨率**: 对于实时应用
3. **跳帧处理**: 不需要处理每一帧
4. **批量处理**: 一次处理多个样本

---

## 📁 输出目录

```
output/
├── images/              # 单张图片结果
│   ├── photo_annotated.jpg
│   └── photo_result.png
├── batch/               # 批量处理结果
│   ├── image1_result.jpg
│   ├── image2_result.jpg
│   └── statistics.png
├── videos/              # 视频处理结果
│   └── processed_YYYYMMDD_HHMMSS.mp4
└── webcam/              # 摄像头截图
    └── webcam_YYYYMMDD_HHMMSS.jpg
```

**在 Windows 中查看：**
```bash
explorer.exe output\\images
```

---

## 🛠️ 高级用法

### Python 集成

```python
import sys
sys.path.insert(0, 'src')
from visualize import FERVisualizer

# 创建可视化器
viz = FERVisualizer('checkpoints/best_model.ckpt', device_target='GPU')

# 处理图片
viz.process_image('photo.jpg', save_result=True)

# 批量处理
viz.process_batch('photos/', pattern='*.jpg')
```

### 自定义输出

```python
# 修改 src/visualize.py 中的配置
EMOTION_COLORS = {
    'happy': (0, 255, 255),  # 自定义颜色
    # ...
}
```

---

## 📋 完整参数说明

### demo_visualization.py

```
--mode           处理模式 [webcam|image|video|batch]
--ckpt          模型检查点路径
--input         输入文件/目录路径
--device        计算设备 [CPU|GPU]
```

### src/visualize.py

```
--mode           处理模式
--ckpt_path      模型检查点路径
--input          输入文件/目录路径
--device_target  设备类型
--output_dir     输出目录
--save_video     保存处理后的视频（video 模式）
--save_frames    保存关键帧（webcam/video 模式）
--camera_id      摄像头 ID（webcam 模式）
--pattern        文件匹配模式（batch 模式）
```

---

## 🔍 示例场景

### 场景 1: 分析照片集合

```bash
python3 demo_visualization.py \
  --mode batch \
  --ckpt checkpoints/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test/happy/

# 查看统计
cat output/batch/statistics.png
```

### 场景 2: 处理视频会议录像

```bash
python3 demo_visualization.py \
  --mode video \
  --ckpt checkpoints/best_model.ckpt \
  --input meeting.mp4 \
  --device GPU
```

### 场景 3: 快速测试单张图片

```bash
python3 demo_visualization.py \
  --mode image \
  --ckpt checkpoints/best_model.ckpt \
  --input test.jpg
```

---

## 📚 更多资源

- **快速参考**: [quick-reference/visualization.md](quick-reference/visualization.md)
- **命令清单**: [quick-reference/commands.txt](quick-reference/commands.txt)
- **故障排除**: [troubleshooting.md](troubleshooting.md)
- **WSL 命令**: [wsl_commands.md](wsl_commands.md)

---

**返回**: [快速开始](getting_started.md) | [文档目录](README.md)
