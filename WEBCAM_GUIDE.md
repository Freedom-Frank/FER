# 实时摄像头表情识别使用指南

## 快速开始

### Windows 用户

1. **一键启动**（最简单）：
   ```bash
   # 双击运行或命令行执行
   run_webcam.bat
   ```

2. **命令行方式**：
   ```bash
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints\best_model.ckpt
   ```

### Linux/WSL 用户

1. **一键启动**（最简单）：
   ```bash
   bash run_webcam.sh
   ```

2. **命令行方式**：
   ```bash
   # CPU模式
   python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --device CPU

   # GPU模式（推荐）
   python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --device GPU
   ```

## 功能特性

### 实时显示内容

1. **人脸检测框**：
   - 自动检测视频中的人脸
   - 彩色边框标记不同表情
   - 支持多人脸同时检测

2. **表情识别结果**：
   - 显示识别出的表情名称（如 happy, sad, angry 等）
   - 显示置信度百分比
   - 颜色编码：
     - 红色 (angry) - 生气
     - 绿色 (disgust) - 厌恶
     - 品红 (fear) - 恐惧
     - 黄色 (happy) - 开心
     - 蓝色 (sad) - 悲伤
     - 橙色 (surprise) - 惊讶
     - 灰色 (neutral) - 中性

3. **概率条形图**（右侧显示）：
   - 7种表情的概率分布
   - 实时更新
   - 直观的可视化展示

4. **性能指标**：
   - 实时FPS显示
   - 每10帧更新一次

### 交互控制

| 按键 | 功能 |
|------|------|
| `q` | 退出程序 |
| `s` | 保存当前帧到 `output/webcam/` |

## 高级用法

### 使用不同的摄像头

如果你的电脑有多个摄像头（如内置摄像头 + 外接USB摄像头）：

```bash
# Windows
python tools\demo_visualization.py --mode webcam --ckpt checkpoints\best_model.ckpt --camera_id 0

# Linux/WSL
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --camera_id 0
```

常见摄像头ID：
- `0` - 默认摄像头（通常是内置摄像头）
- `1` - 第二个摄像头（通常是外接USB摄像头）
- `2+` - 额外的摄像头

### GPU加速

如果你有NVIDIA GPU并已配置CUDA环境：

```bash
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --device GPU
```

**性能对比**：
- CPU模式：约 10-20 FPS
- GPU模式：约 30-60 FPS

### 使用不同的模型

```bash
# 使用训练好的特定epoch模型
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/fer-5_449.ckpt

# 使用最佳模型
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt
```

## 常见问题

### 1. 摄像头无法打开

**错误信息**：
```
[ERROR] Cannot open webcam
VIDEOIO(V4L2:/dev/video0): can't open camera by index
```

**可能原因**：
- 摄像头未连接
- 摄像头被其他程序占用
- 权限不足
- **WSL 环境下无法直接访问 USB 摄像头**（最常见）

**解决方法**：

**如果你在 WSL 中遇到此错误** ⭐ 推荐解决方案：

在 Windows 上直接运行（最简单）：

```powershell
# 在 Windows PowerShell 中
cd E:\Users\Meng\Projects\VScodeProjects\FER
.\run_webcam.bat
```

**详细的 WSL 摄像头配置指南**: 查看 [WSL_WEBCAM_SETUP.md](WSL_WEBCAM_SETUP.md)

**其他解决方法**：

```bash
# 1. 检查摄像头是否正常工作（Windows）
# 打开"相机"应用测试

# 2. 关闭占用摄像头的其他程序（如Zoom、Teams等）

# 3. 尝试使用不同的摄像头ID
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --camera_id 1

# 4. 测试摄像头
python test_camera.py
```

### 2. 无法检测到人脸

**现象**：视频显示正常，但没有检测框出现

**可能原因**：
- 光线太暗
- 人脸角度太偏
- 距离摄像头太远或太近
- 人脸被遮挡

**解决方法**：
- 确保光线充足
- 正面对着摄像头
- 保持适当距离（约50-100cm）
- 移除遮挡物（如口罩、墨镜等）

### 3. 识别准确率低

**可能原因**：
- 人脸图像质量差
- 表情不够明显
- 模型未充分训练

**解决方法**：
```bash
# 1. 使用GPU加速提高处理速度
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --device GPU

# 2. 使用训练更多epoch的模型
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/fer-200_449.ckpt

# 3. 重新训练模型以提高准确率
python src/train.py --data_csv data/FER2013/fer2013.csv --epochs 200 --augment --mixup
```

### 4. FPS太低

**现象**：视频卡顿，FPS < 10

**解决方法**：
```bash
# 1. 使用GPU加速（最有效）
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt --device GPU

# 2. 降低摄像头分辨率（修改代码）
# 在 src/visualize.py 的 process_webcam 方法中添加：
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 3. 关闭其他占用CPU的程序
```

### 5. 缺少依赖库

**错误信息**：`ModuleNotFoundError: No module named 'cv2'`

**解决方法**：
```bash
# 安装OpenCV
pip install opencv-python

# 安装所有依赖
pip install -r requirements.txt
```

## 技术细节

### 人脸检测

使用 OpenCV 的 Haar Cascade 人脸检测器：
- 检测器文件：`haarcascade_frontalface_default.xml`
- 参数优化：`scaleFactor=1.05, minNeighbors=3, minSize=(20, 20)`
- 支持多人脸同时检测

### 图像预处理

1. 从视频帧中提取人脸区域
2. 转换为灰度图像
3. 调整大小到 48x48 像素
4. 归一化到 [0, 1] 范围
5. 扩展维度为 [1, 1, 48, 48]

### 表情识别

1. 使用 MindSpore 深度学习框架
2. ResNet架构 + 注意力机制
3. 输出7种表情的概率分布
4. 选择概率最高的表情作为预测结果

### 性能优化

- 每10帧更新一次FPS显示
- 使用GPU加速推理（如果可用）
- 优化的人脸检测参数
- 实时概率条形图更新

## 保存的文件

当你按下 `s` 键保存帧时，文件会保存到：

```
output/webcam/webcam_YYYYMMDD_HHMMSS.jpg
```

例如：
```
output/webcam/webcam_20250129_143052.jpg
```

文件包含：
- 检测到的人脸边界框
- 表情识别结果标签
- 7种表情的概率条形图

## 下一步

1. **处理图片**：[image 模式使用指南](README.md#单张图片处理)
2. **处理视频**：[video 模式使用指南](README.md#视频文件处理)
3. **批量处理**：[batch 模式使用指南](README.md#批量图片处理)
4. **模型训练**：[训练指南](docs/guides/training_guide.md)

## 参考资料

- [完整文档](README.md)
- [可视化指南](docs/visualization_guide.md)
- [环境配置](docs/setup.md)
- [常见问题](docs/troubleshooting.md)
