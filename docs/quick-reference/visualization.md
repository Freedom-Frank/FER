# FER2013 可视化功能快速指南

本文档提供可视化功能的快速上手指南。完整文档请查看 [docs/visualization.md](docs/visualization.md)。

## 快速开始

### 1. 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt

# 或仅安装可视化相关依赖
pip install matplotlib>=3.3.0 seaborn>=0.11.0 opencv-python>=4.5.0
```

### 2. 准备模型

确保你有训练好的模型检查点：

```bash
# 检查模型文件
ls checkpoints/best.ckpt

# 如果没有，需要先训练模型
python src/train.py --data_csv data/FER2013/fer2013.csv --epochs 50
```

### 3. 选择模式运行

#### 🎥 实时摄像头识别

```bash
python demo_visualization.py --mode webcam --ckpt checkpoints/best.ckpt
```

**操作提示:**
- 按 `q` 退出
- 按 `s` 保存当前帧

**显示内容:**
- 彩色人脸边界框
- 表情标签 + 置信度
- 实时概率条形图
- FPS 显示

---

#### 🖼️ 单张图片处理

```bash
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input photo.jpg
```

**输出文件:**
- `output/images/photo_annotated.jpg` - 标注后的图片
- `output/images/photo_result.png` - 人脸 + 概率图

---

#### 🎬 视频文件处理

```bash
python demo_visualization.py --mode video --ckpt checkpoints/best.ckpt --input video.mp4
```

**输出:**
- 处理后的视频文件
- 实时进度显示
- ETA 预估

---

#### 📁 批量图片处理

```bash
python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input test_images/
```

**输出:**
- 每张图片的标注结果
- `output/batch/statistics.png` - 表情分布统计图
- 详细的统计信息

---

## 高级选项

### GPU 加速

```bash
# 使用 GPU（速度提升 5-10 倍）
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input photo.jpg --device GPU
```

### 指定输出目录

```bash
python src/visualize.py \
  --mode image \
  --ckpt_path checkpoints/best.ckpt \
  --input photo.jpg \
  --output_dir my_output
```

### 视频保存选项

```bash
python src/visualize.py \
  --mode video \
  --ckpt_path checkpoints/best.ckpt \
  --input video.mp4 \
  --save_video \
  --output_dir output/videos
```

## 表情颜色编码

| 表情 | 英文 | 颜色 |
|------|------|------|
| 😠 生气 | angry | 🔴 红色 |
| 🤢 厌恶 | disgust | 🟢 绿色 |
| 😨 恐惧 | fear | 🟣 品红 |
| 😊 开心 | happy | 🟡 黄色 |
| 😢 悲伤 | sad | 🔵 蓝色 |
| 😮 惊讶 | surprise | 🟠 橙色 |
| 😐 中性 | neutral | ⚪ 灰色 |

## 测试脚本

使用交互式测试脚本：

```bash
# Linux/WSL
chmod +x scripts/test_visualization.sh
./scripts/test_visualization.sh

# 然后选择测试选项
```

## 输出目录结构

```
output/
├── webcam/           # 摄像头保存的帧
├── images/           # 单张图片处理结果
│   ├── photo_annotated.jpg
│   └── photo_result.png
├── videos/           # 视频处理结果
│   └── processed_YYYYMMDD_HHMMSS.mp4
└── batch/            # 批量处理结果
    ├── image1_result.jpg
    ├── image2_result.jpg
    └── statistics.png
```

## 性能参考

| 模式 | CPU (i7) | GPU (RTX 3060) |
|------|----------|----------------|
| 摄像头 (640x480) | 10-15 FPS | 30-60 FPS |
| 视频 (1080p) | 3-5 FPS | 15-25 FPS |
| 图片 (1920x1080) | 0.5-1s | 0.1-0.2s |

## 常见问题

### WSL 摄像头配置

```bash
# 1. 安装 USB/IP
sudo apt install linux-tools-generic hwdata

# 2. 在 Windows PowerShell (管理员) 中:
usbipd wsl list
usbipd wsl attach --busid <BUSID>

# 3. 检查设备
ls /dev/video*
```

### X11 显示问题

```bash
# 安装 X11
sudo apt install x11-apps

# 设置 DISPLAY
export DISPLAY=:0

# 测试
xclock
```

### OpenCV 显示错误

如果遇到 "no display" 错误，脚本已经使用 `matplotlib.use('Agg')` 后端，无需显示窗口即可保存图像。

## 示例命令集合

```bash
# 快速测试（单张图片）
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input test.jpg

# 实时摄像头
python demo_visualization.py --mode webcam --ckpt checkpoints/best.ckpt

# 处理视频
python demo_visualization.py --mode video --ckpt checkpoints/best.ckpt --input video.mp4

# 批量处理
python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input photos/

# GPU 加速处理
python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input photos/ --device GPU

# 查看帮助
python demo_visualization.py --mode menu --ckpt checkpoints/best.ckpt
```

## 集成到项目

```python
from src.visualize import FERVisualizer

# 创建可视化器
viz = FERVisualizer('checkpoints/best.ckpt', device_target='CPU')

# 处理图片
viz.process_image('photo.jpg', save_result=True)

# 批量处理
viz.process_batch('photos/', pattern='*.jpg')
```

## 下一步

- 📚 查看完整文档: [docs/visualization.md](docs/visualization.md)
- 🚀 训练你的模型: [docs/quickstart.md](docs/quickstart.md)
- ⚙️ 配置环境: [docs/setup.md](docs/setup.md)
- 🔧 优化技巧: [docs/optimization.md](docs/optimization.md)

## 问题反馈

如遇到问题，请在 GitHub Issues 中提交，并提供：
- 系统信息 (OS, Python 版本)
- 完整错误信息
- 使用的命令

---

**快速链接:**
- [主 README](README.md)
- [完整可视化文档](docs/visualization.md)
- [项目仓库](https://github.com/yourusername/FER)
