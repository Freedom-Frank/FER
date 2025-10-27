# 可视化功能示例

本文档展示各种可视化功能的实际使用示例和输出效果。

## 示例 1: 实时摄像头表情识别

### 命令

```bash
python demo_visualization.py --mode webcam --ckpt checkpoints/best.ckpt
```

### 效果说明

**实时显示窗口包含:**
1. **人脸检测框**: 彩色边界框，颜色代表识别的表情
2. **表情标签**: 显示在人脸框上方，格式 "emotion: XX.XX%"
3. **概率条**: 屏幕右侧显示所有7种表情的概率分布
4. **FPS 计数器**: 左上角显示实时帧率

**交互操作:**
- 按 `q`: 退出程序
- 按 `s`: 保存当前帧到 `output/webcam/webcam_TIMESTAMP.jpg`

**适用场景:**
- 实时表情监测
- 互动应用
- 演示和展示
- 数据收集

---

## 示例 2: 单张图片详细分析

### 命令

```bash
python demo_visualization.py --mode image --ckpt checkpoints/best.ckpt --input portrait.jpg
```

### 输出文件

#### 1. `portrait_annotated.jpg` - 标注图
- 原图 + 人脸框 + 标签
- 彩色边界框
- 表情和置信度

#### 2. `portrait_result.png` - 分析图
左侧:
- 检测到的人脸图像
- 清晰显示表情

右侧:
- 7种表情的概率条形图
- 彩色编码
- 精确到小数点后两位的概率值

**适用场景:**
- 照片表情分析
- 心理学研究
- 情感计算研究
- 数据标注辅助

---

## 示例 3: 视频表情追踪

### 命令

```bash
python demo_visualization.py --mode video --ckpt checkpoints/best.ckpt --input interview.mp4
```

### 处理流程

```
[INFO] Processing video: interview.mp4
[INFO] Video: 1920x1080 @ 30fps, 3600 frames

[PROGRESS] 8.3% (300/3600) - FPS: 12.5 - ETA: 264s
[PROGRESS] 16.7% (600/3600) - FPS: 13.1 - ETA: 229s
[PROGRESS] 25.0% (900/3600) - FPS: 12.8 - ETA: 211s
...

[SAVE] Video saved to output/videos/processed_20240101_120000.mp4
[INFO] Video processing completed in 280.5s
```

### 输出视频特点

- 保留原视频分辨率和帧率
- 每一帧标注人脸和表情
- 实时概率条显示
- MP4 格式，易于分享

**适用场景:**
- 访谈分析
- 视频情感标注
- 行为研究
- 教育演示

---

## 示例 4: 批量图片统计分析

### 命令

```bash
python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input photos/
```

### 处理过程

```
[INFO] Found 50 images in photos/

[1/50] Processing: person001.jpg
  Result: happy (87.34%)

[2/50] Processing: person002.jpg
  Result: neutral (76.21%)

[3/50] Processing: person003.jpg
  Result: sad (82.56%)
...

[INFO] Batch processing completed

[STATISTICS]
  angry: 3
  disgust: 1
  fear: 2
  happy: 25
  sad: 8
  surprise: 4
  neutral: 7

[SAVE] Statistics saved to output/batch/statistics.png
```

### 输出内容

#### 1. 标注图片
- 每张原图的标注版本
- 文件名: `personXXX_result.jpg`

#### 2. `statistics.png` - 统计图表
- 柱状图显示表情分布
- 彩色编码
- 数量标注
- 适合放入报告

**适用场景:**
- 数据集分析
- 群体情感研究
- 社交媒体分析
- 市场调研

---

## 示例 5: GPU 加速处理

### 命令

```bash
# CPU 处理
time python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input photos/ --device CPU

# GPU 处理
time python demo_visualization.py --mode batch --ckpt checkpoints/best.ckpt --input photos/ --device GPU
```

### 性能对比

```
# CPU 模式
[INFO] Batch processing completed
real    0m45.234s
user    0m42.891s
sys     0m1.987s

# GPU 模式
[INFO] Batch processing completed
real    0m8.567s
user    0m7.234s
sys     0m1.102s

速度提升: 5.3x
```

**建议:**
- 批量处理使用 GPU
- 小量数据 CPU 即可
- WSL2 配置 CUDA 支持

---

## 示例 6: 高级用法 - Python 集成

### 场景: 自动化表情分析流水线

```python
#!/usr/bin/env python3
"""
自动化表情分析流水线示例
处理目录中的所有图片，生成分析报告
"""

import os
import sys
sys.path.insert(0, 'src')

from visualize import FERVisualizer
import glob
from datetime import datetime

def analyze_directory(input_dir, output_dir, model_path):
    """分析目录中的所有图片"""

    # 创建可视化器
    print(f"[INFO] Loading model from {model_path}")
    viz = FERVisualizer(model_path, device_target='GPU', output_dir=output_dir)

    # 获取所有图片
    image_patterns = ['*.jpg', '*.jpeg', '*.png']
    image_paths = []
    for pattern in image_patterns:
        image_paths.extend(glob.glob(os.path.join(input_dir, pattern)))

    print(f"[INFO] Found {len(image_paths)} images")

    # 统计信息
    results = []

    # 处理每张图片
    for i, image_path in enumerate(image_paths, 1):
        print(f"\n[{i}/{len(image_paths)}] Processing: {os.path.basename(image_path)}")

        # 处理图片
        viz.process_image(image_path, save_result=True)

        # 记录结果（这里简化，实际可以从 process_image 返回）
        results.append({
            'image': os.path.basename(image_path),
            'timestamp': datetime.now()
        })

    # 生成报告
    generate_report(results, output_dir)

    print(f"\n[INFO] Processing completed!")
    print(f"[INFO] Results saved to: {output_dir}")

def generate_report(results, output_dir):
    """生成分析报告"""
    report_path = os.path.join(output_dir, 'report.txt')

    with open(report_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("Face Expression Recognition Analysis Report\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total images processed: {len(results)}\n")
        f.write(f"Report generated: {datetime.now()}\n\n")

        f.write("Processed files:\n")
        for result in results:
            f.write(f"  - {result['image']}\n")

    print(f"[SAVE] Report saved to {report_path}")

if __name__ == '__main__':
    analyze_directory(
        input_dir='input_photos',
        output_dir='analysis_results',
        model_path='checkpoints/best.ckpt'
    )
```

### 运行

```bash
python analyze_pipeline.py
```

---

## 示例 7: 实时表情统计

### 场景: 会议情绪监测

```python
#!/usr/bin/env python3
"""
实时表情统计示例
适合会议、课堂等场景的情绪监测
"""

import sys
sys.path.insert(0, 'src')

import cv2
import time
from collections import defaultdict
from visualize import FERVisualizer

def realtime_emotion_stats(model_path, camera_id=0, duration=60):
    """
    实时表情统计

    Args:
        model_path: 模型路径
        camera_id: 摄像头ID
        duration: 监测时长（秒）
    """

    # 创建可视化器
    viz = FERVisualizer(model_path, device_target='GPU')

    # 打开摄像头
    cap = cv2.VideoCapture(camera_id)

    # 统计数据
    emotion_counts = defaultdict(int)
    frame_count = 0
    start_time = time.time()

    print(f"[INFO] Starting emotion monitoring for {duration} seconds...")
    print("[INFO] Press 'q' to quit early")

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = viz.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        # 处理每个人脸
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            emotion, prob, probs = viz.predict_emotion(face_img)

            # 统计
            emotion_counts[emotion] += 1

            # 绘制
            viz.draw_prediction(frame, x, y, w, h, emotion, prob, probs)

        # 显示统计
        elapsed = int(time.time() - start_time)
        remaining = duration - elapsed
        cv2.putText(frame, f"Time: {elapsed}s / {duration}s", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 显示当前统计
        y_pos = 60
        for emotion, count in sorted(emotion_counts.items()):
            text = f"{emotion}: {count}"
            cv2.putText(frame, text, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_pos += 25

        cv2.imshow('Emotion Statistics', frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # 输出最终统计
    print("\n" + "=" * 50)
    print("Emotion Statistics Summary")
    print("=" * 50)
    print(f"Duration: {elapsed} seconds")
    print(f"Frames processed: {frame_count}")
    print(f"Average FPS: {frame_count / elapsed:.1f}")
    print("\nEmotion counts:")
    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = count / sum(emotion_counts.values()) * 100
        print(f"  {emotion:10s}: {count:4d} ({percentage:5.1f}%)")

if __name__ == '__main__':
    realtime_emotion_stats('checkpoints/best.ckpt', duration=60)
```

---

## 使用技巧

### 1. 提高检测准确率

```python
# 调整检测参数
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,     # 更小的值 = 更敏感（默认1.1）
    minNeighbors=3,       # 更小的值 = 更敏感（默认5）
    minSize=(48, 48),     # 调整最小人脸尺寸
    flags=cv2.CASCADE_SCALE_IMAGE
)
```

### 2. 性能优化

```python
# 跳帧处理
frame_skip = 2
if frame_count % frame_skip == 0:
    # 只在某些帧上运行检测
    faces = detect_faces(frame)
```

### 3. 保存高质量输出

```python
# 修改保存参数
cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])

# matplotlib 高分辨率
plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

### 4. 多人脸处理

```python
# 跟踪多个人脸
face_tracker = {}
for i, (x, y, w, h) in enumerate(faces):
    face_id = f"face_{i}"
    emotion, prob, probs = viz.predict_emotion(face_img)
    face_tracker[face_id] = {'emotion': emotion, 'prob': prob}
```

---

## 总结

可视化功能提供了丰富的表情识别应用场景：

✅ **实时监测**: 摄像头实时识别
✅ **视频分析**: 视频文件批处理
✅ **图片处理**: 单张或批量图片
✅ **数据统计**: 表情分布分析
✅ **灵活集成**: 易于集成到其他项目

更多信息请参考:
- [完整文档](../docs/visualization.md)
- [快速指南](../VISUALIZATION_README.md)
- [主 README](../README.md)
