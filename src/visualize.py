"""
FER2013 面部表情识别可视化工具
支持实时摄像头、视频文件、图片批量处理和结果可视化
适用于 WSL/Linux 环境
"""

import argparse
import cv2
import numpy as np
import mindspore as ms
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from model import SimpleCNN
try:
    from model_legacy import SimpleCNN_Legacy
except ImportError:
    SimpleCNN_Legacy = None
import matplotlib
matplotlib.use('Agg')  # 无GUI环境使用
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time

# 表情标签和颜色
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_COLORS = {
    'angry': (0, 0, 255),      # 红色
    'disgust': (0, 255, 0),    # 绿色
    'fear': (255, 0, 255),     # 品红
    'happy': (0, 255, 255),    # 黄色
    'sad': (255, 0, 0),        # 蓝色
    'surprise': (255, 165, 0), # 橙色
    'neutral': (128, 128, 128) # 灰色
}

# 中文标签（用于保存）
EMOTION_CN = {
    'angry': '生气',
    'disgust': '厌恶',
    'fear': '恐惧',
    'happy': '开心',
    'sad': '悲伤',
    'surprise': '惊讶',
    'neutral': '中性'
}


class FERVisualizer:
    """面部表情识别可视化器"""

    def __init__(self, ckpt_path, device_target='CPU', output_dir='output'):
        """
        初始化可视化器

        Args:
            ckpt_path: 模型检查点路径
            device_target: 设备类型 ('CPU' 或 'GPU')
            output_dir: 输出目录
        """
        # 设置设备
        context.set_context(mode=context.GRAPH_MODE, device_target=device_target)

        # 加载模型 - 自动检测模型版本
        print(f"[INFO] Loading model from {ckpt_path}")
        self.net = self._load_model_with_auto_detection(ckpt_path)
        self.net.set_train(False)

        # 创建输出目录
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 人脸检测器
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        print(f"[INFO] Visualizer initialized. Output: {output_dir}")

    def _load_model_with_auto_detection(self, ckpt_path):
        """
        自动检测并加载正确版本的模型

        Args:
            ckpt_path: 检查点路径

        Returns:
            加载好的模型
        """
        # 加载检查点
        param_dict = load_checkpoint(ckpt_path)

        # 检查分类器第一层的形状来判断模型版本
        # 新版本: classifier.0.weight shape = (256, 512)
        # 旧版本: classifier.0.weight shape = (128, 128)
        classifier_key = 'classifier.0.weight'

        if classifier_key in param_dict:
            classifier_shape = param_dict[classifier_key].shape
            print(f"[INFO] Detected classifier shape: {classifier_shape}")

            # 判断是旧版本模型 (128, 128)
            if classifier_shape == (128, 128):
                if SimpleCNN_Legacy is None:
                    print("[ERROR] Legacy model detected but model_legacy.py not found")
                    raise ImportError("Please ensure model_legacy.py exists in src/")

                print("[INFO] Loading legacy model (128 -> 128 -> 7)")
                net = SimpleCNN_Legacy(7)
                load_param_into_net(net, param_dict)
                return net

            # 新版本模型 (256, 512)
            elif classifier_shape == (256, 512):
                print("[INFO] Loading current model (512 -> 256 -> 128 -> 7)")
                net = SimpleCNN(7)
                load_param_into_net(net, param_dict)
                return net

            else:
                print(f"[WARNING] Unknown classifier shape: {classifier_shape}")
                print("[INFO] Attempting to load as current model...")
                net = SimpleCNN(7)
                try:
                    load_param_into_net(net, param_dict)
                    return net
                except Exception as e:
                    print(f"[ERROR] Failed to load: {e}")
                    raise
        else:
            print("[WARNING] Cannot determine model version, using current model")
            net = SimpleCNN(7)
            load_param_into_net(net, param_dict)
            return net

    def preprocess_face(self, face_img):
        """
        预处理人脸图像

        Args:
            face_img: 人脸图像 (BGR格式)

        Returns:
            预处理后的张量
        """
        # 转灰度
        if len(face_img.shape) == 3:
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = face_img

        # 调整大小
        resized = cv2.resize(gray, (48, 48))

        # 归一化
        normalized = resized.astype('float32') / 255.0

        # 扩展维度 [1, 1, 48, 48]
        tensor = np.expand_dims(normalized, (0, 1))

        return tensor

    def predict_emotion(self, face_img):
        """
        预测人脸表情

        Args:
            face_img: 人脸图像

        Returns:
            (emotion, probability, all_probs)
        """
        # 预处理
        tensor = self.preprocess_face(face_img)

        # 推理
        output = self.net(ms.Tensor(tensor))
        probs = ms.ops.softmax(output)[0].asnumpy()

        # 获取最高概率的表情
        idx = int(np.argmax(probs))
        emotion = EMOTIONS[idx]
        probability = float(probs[idx])

        return emotion, probability, probs

    def draw_prediction(self, frame, x, y, w, h, emotion, probability, probs):
        """
        在帧上绘制预测结果

        Args:
            frame: 视频帧
            x, y, w, h: 人脸边界框
            emotion: 预测的表情
            probability: 概率
            probs: 所有类别的概率
        """
        # 绘制人脸框
        color = EMOTION_COLORS.get(emotion, (255, 255, 255))
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # 绘制标签
        label = f"{emotion}: {probability:.2%}"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

        # 绘制标签背景
        cv2.rectangle(frame,
                     (x, y - label_size[1] - 10),
                     (x + label_size[0], y),
                     color, -1)

        # 绘制标签文字
        cv2.putText(frame, label, (x, y - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 在右侧绘制概率条
        self.draw_probability_bars(frame, probs)

    def draw_probability_bars(self, frame, probs, start_x=None, start_y=10, bar_width=150, bar_height=20):
        """
        绘制概率条形图

        Args:
            frame: 视频帧
            probs: 概率数组
            start_x: 起始x坐标（None表示右侧）
            start_y: 起始y坐标
            bar_width: 条形宽度
            bar_height: 条形高度
        """
        if start_x is None:
            start_x = frame.shape[1] - bar_width - 10

        for i, (emotion, prob) in enumerate(zip(EMOTIONS, probs)):
            y = start_y + i * (bar_height + 5)

            # 绘制背景条
            cv2.rectangle(frame,
                         (start_x, y),
                         (start_x + bar_width, y + bar_height),
                         (50, 50, 50), -1)

            # 绘制概率条
            bar_len = int(bar_width * prob)
            color = EMOTION_COLORS.get(emotion, (255, 255, 255))
            cv2.rectangle(frame,
                         (start_x, y),
                         (start_x + bar_len, y + bar_height),
                         color, -1)

            # 绘制标签
            label = f"{emotion}: {prob:.1%}"
            cv2.putText(frame, label,
                       (start_x + 5, y + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                       (255, 255, 255), 1)

    def save_result_plot(self, face_img, emotion, probs, output_path):
        """
        保存结果图（人脸+概率图）

        Args:
            face_img: 人脸图像
            emotion: 预测的表情
            probs: 概率数组
            output_path: 输出路径
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # 显示人脸
        if len(face_img.shape) == 3:
            ax1.imshow(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
        else:
            ax1.imshow(face_img, cmap='gray')
        ax1.set_title(f'Predicted: {emotion}', fontsize=14, fontweight='bold')
        ax1.axis('off')

        # 绘制概率条形图
        colors = [EMOTION_COLORS[e] for e in EMOTIONS]
        colors = [(b/255, g/255, r/255) for r, g, b in colors]  # BGR -> RGB

        bars = ax2.barh(EMOTIONS, probs, color=colors)
        ax2.set_xlabel('Probability', fontsize=12)
        ax2.set_title('Emotion Probabilities', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 1)

        # 添加数值标签
        for bar, prob in zip(bars, probs):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'{prob:.2%}',
                    ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Result saved to {output_path}")

    def process_webcam(self, camera_id=0, save_frames=False):
        """
        处理摄像头实时视频

        Args:
            camera_id: 摄像头ID
            save_frames: 是否保存帧
        """
        print(f"[INFO] Starting webcam {camera_id}. Press 'q' to quit, 's' to save frame")

        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("[ERROR] Cannot open webcam")
            return

        frame_count = 0
        fps_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Cannot read frame")
                break

            # 检测人脸
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            # 处理每个人脸
            for (x, y, w, h) in faces:
                # 提取人脸
                face_img = frame[y:y+h, x:x+w]

                # 预测表情
                emotion, probability, probs = self.predict_emotion(face_img)

                # 绘制结果
                self.draw_prediction(frame, x, y, w, h, emotion, probability, probs)

            # 计算FPS
            frame_count += 1
            if frame_count % 10 == 0:
                fps = 10 / (time.time() - fps_time)
                fps_time = time.time()
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 显示帧
            cv2.imshow('FER - Press q to quit, s to save', frame)

            # 按键处理
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and len(faces) > 0:
                # 保存当前帧
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                frame_path = os.path.join(self.output_dir, f'webcam_{timestamp}.jpg')
                cv2.imwrite(frame_path, frame)
                print(f"[SAVE] Frame saved to {frame_path}")

        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Webcam closed")

    def process_video(self, video_path, save_video=True, save_frames=False):
        """
        处理视频文件

        Args:
            video_path: 视频文件路径
            save_video: 是否保存处理后的视频
            save_frames: 是否保存关键帧
        """
        print(f"[INFO] Processing video: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"[ERROR] Cannot open video: {video_path}")
            return

        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"[INFO] Video: {width}x{height} @ {fps}fps, {total_frames} frames")

        # 创建视频写入器
        if save_video:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f'processed_{timestamp}.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 检测人脸
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            # 处理每个人脸
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                emotion, probability, probs = self.predict_emotion(face_img)
                self.draw_prediction(frame, x, y, w, h, emotion, probability, probs)

            # 写入视频
            if save_video:
                out.write(frame)

            # 显示进度
            if frame_count % 30 == 0:
                progress = frame_count / total_frames * 100
                elapsed = time.time() - start_time
                fps_avg = frame_count / elapsed
                eta = (total_frames - frame_count) / fps_avg if fps_avg > 0 else 0
                print(f"[PROGRESS] {progress:.1f}% ({frame_count}/{total_frames}) "
                      f"- FPS: {fps_avg:.1f} - ETA: {eta:.0f}s")

        cap.release()
        if save_video:
            out.release()
            print(f"[SAVE] Video saved to {output_path}")

        print(f"[INFO] Video processing completed in {time.time() - start_time:.1f}s")

    def process_image(self, image_path, save_result=True):
        """
        处理单张图片

        Args:
            image_path: 图片路径
            save_result: 是否保存结果
        """
        print(f"[INFO] Processing image: {image_path}")

        # 读取图片
        img = cv2.imread(image_path)
        if img is None:
            print(f"[ERROR] Cannot read image: {image_path}")
            return

        # 检测人脸
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        if len(faces) == 0:
            print("[WARNING] No faces detected in image")
            return

        print(f"[INFO] Detected {len(faces)} face(s)")

        # 处理每个人脸
        for i, (x, y, w, h) in enumerate(faces):
            face_img = img[y:y+h, x:x+w]
            emotion, probability, probs = self.predict_emotion(face_img)

            print(f"  Face {i+1}: {emotion} ({probability:.2%})")

            # 绘制结果
            self.draw_prediction(img, x, y, w, h, emotion, probability, probs)

            # 保存结果
            if save_result:
                # 保存标注图片
                basename = os.path.splitext(os.path.basename(image_path))[0]
                annotated_path = os.path.join(self.output_dir, f'{basename}_annotated.jpg')
                cv2.imwrite(annotated_path, img)

                # 保存详细结果图
                result_path = os.path.join(self.output_dir, f'{basename}_result.png')
                self.save_result_plot(face_img, emotion, probs, result_path)

        print(f"[INFO] Image processing completed")

    def process_batch(self, image_dir, pattern='*.jpg'):
        """
        批量处理图片

        Args:
            image_dir: 图片目录
            pattern: 文件匹配模式
        """
        import glob

        image_paths = glob.glob(os.path.join(image_dir, pattern))
        print(f"[INFO] Found {len(image_paths)} images in {image_dir}")

        if len(image_paths) == 0:
            print("[WARNING] No images found")
            return

        # 统计结果
        emotion_counts = {emotion: 0 for emotion in EMOTIONS}

        for i, image_path in enumerate(image_paths, 1):
            print(f"\n[{i}/{len(image_paths)}] Processing: {os.path.basename(image_path)}")

            # 读取图片
            img = cv2.imread(image_path)
            if img is None:
                print(f"[ERROR] Cannot read image")
                continue

            # 检测人脸
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            if len(faces) == 0:
                print("[WARNING] No faces detected")
                continue

            # 处理第一个人脸
            x, y, w, h = faces[0]
            face_img = img[y:y+h, x:x+w]
            emotion, probability, probs = self.predict_emotion(face_img)

            emotion_counts[emotion] += 1
            print(f"  Result: {emotion} ({probability:.2%})")

            # 绘制并保存
            self.draw_prediction(img, x, y, w, h, emotion, probability, probs)
            basename = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(self.output_dir, f'{basename}_result.jpg')
            cv2.imwrite(output_path, img)

        # 生成统计图
        self.save_statistics(emotion_counts)

        print(f"\n[INFO] Batch processing completed")
        print("\n[STATISTICS]")
        for emotion, count in emotion_counts.items():
            print(f"  {emotion}: {count}")

    def save_statistics(self, emotion_counts):
        """
        保存统计图表

        Args:
            emotion_counts: 表情统计字典
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())
        colors = [EMOTION_COLORS[e] for e in emotions]
        colors = [(b/255, g/255, r/255) for r, g, b in colors]

        bars = ax.bar(emotions, counts, color=colors)
        ax.set_xlabel('Emotion', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Emotion Distribution', fontsize=14, fontweight='bold')

        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'statistics.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Statistics saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='FER2013 面部表情识别可视化工具')

    # 模型参数
    parser.add_argument('--ckpt_path', type=str, required=True,
                       help='模型检查点路径')
    parser.add_argument('--device_target', type=str, default='CPU',
                       choices=['CPU', 'GPU'], help='设备类型')
    parser.add_argument('--output_dir', type=str, default='output',
                       help='输出目录')

    # 输入源
    parser.add_argument('--mode', type=str, required=True,
                       choices=['webcam', 'video', 'image', 'batch'],
                       help='处理模式')
    parser.add_argument('--input', type=str,
                       help='输入文件/目录路径 (video/image/batch 模式需要)')
    parser.add_argument('--camera_id', type=int, default=0,
                       help='摄像头ID (webcam 模式使用)')
    parser.add_argument('--pattern', type=str, default='*.jpg',
                       help='文件匹配模式 (batch 模式使用)')

    # 输出选项
    parser.add_argument('--save_video', action='store_true',
                       help='保存处理后的视频')
    parser.add_argument('--save_frames', action='store_true',
                       help='保存关键帧')

    args = parser.parse_args()

    # 创建可视化器
    visualizer = FERVisualizer(
        ckpt_path=args.ckpt_path,
        device_target=args.device_target,
        output_dir=args.output_dir
    )

    # 根据模式处理
    if args.mode == 'webcam':
        visualizer.process_webcam(camera_id=args.camera_id, save_frames=args.save_frames)

    elif args.mode == 'video':
        if not args.input:
            print("[ERROR] --input required for video mode")
            return
        visualizer.process_video(args.input, save_video=args.save_video,
                                save_frames=args.save_frames)

    elif args.mode == 'image':
        if not args.input:
            print("[ERROR] --input required for image mode")
            return
        visualizer.process_image(args.input, save_result=True)

    elif args.mode == 'batch':
        if not args.input:
            print("[ERROR] --input required for batch mode")
            return
        visualizer.process_batch(args.input, pattern=args.pattern)


if __name__ == '__main__':
    main()
