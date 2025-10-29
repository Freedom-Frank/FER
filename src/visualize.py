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
        # 尝试多种方式加载 Haar Cascade 文件
        cascade_path = None
        try:
            # 方法 1：使用 cv2.data（OpenCV 4.x）
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        except AttributeError:
            # 方法 2：使用 OpenCV 安装路径
            cv2_base = os.path.dirname(cv2.__file__)
            cascade_path = os.path.join(cv2_base, 'data', 'haarcascade_frontalface_default.xml')

            # 方法 3：如果上面的路径不存在，尝试其他常见位置
            if not os.path.exists(cascade_path):
                # Windows conda 环境的常见路径
                import sys
                possible_paths = [
                    os.path.join(sys.prefix, 'Library', 'etc', 'haarcascades', 'haarcascade_frontalface_default.xml'),
                    os.path.join(sys.prefix, 'share', 'opencv4', 'haarcascades', 'haarcascade_frontalface_default.xml'),
                    os.path.join(cv2_base, '..', 'data', 'haarcascade_frontalface_default.xml'),
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        cascade_path = path
                        break

        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # 验证是否加载成功
        if self.face_cascade.empty():
            raise RuntimeError(f"Failed to load face cascade from {cascade_path}")

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

            # 检测人脸 - 使用更宽松的参数以提高检测率
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20),
                flags=cv2.CASCADE_SCALE_IMAGE
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

            # 检测人脸 - 使用更宽松的参数以提高检测率
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20),
                flags=cv2.CASCADE_SCALE_IMAGE
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

        # 检测人脸 - 使用更宽松的参数以提高检测率
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
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

    def process_batch(self, image_dir, pattern='*.jpg', save_images=False):
        """
        批量处理单个类别的图片

        Args:
            image_dir: 图片目录（单个类别）
            pattern: 文件匹配模式
            save_images: 是否保存标注后的图片（默认False，只保存统计图）

        Returns:
            包含统计信息的字典
        """
        import glob

        image_paths = glob.glob(os.path.join(image_dir, pattern))
        print(f"[INFO] Found {len(image_paths)} images in {image_dir}")

        if len(image_paths) == 0:
            print("[WARNING] No images found")
            return None

        # 从输入目录名提取类别名称（如 sad, happy 等）
        category_name = os.path.basename(os.path.normpath(image_dir))

        # 统计结果
        emotion_counts = {emotion: 0 for emotion in EMOTIONS}
        total_images = 0
        correct_predictions = 0

        for i, image_path in enumerate(image_paths, 1):
            if i % 50 == 0 or i == 1:  # 减少打印频率
                print(f"[{i}/{len(image_paths)}] Processing...")

            # 读取图片
            img = cv2.imread(image_path)
            if img is None:
                continue

            # 检测人脸
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces) == 0:
                continue

            # 处理第一个人脸
            x, y, w, h = faces[0]
            face_img = img[y:y+h, x:x+w]
            emotion, probability, probs = self.predict_emotion(face_img)

            emotion_counts[emotion] += 1
            total_images += 1

            # 计算准确率（真实标签是目录名）
            if emotion == category_name:
                correct_predictions += 1

            # 只在需要时保存图片
            if save_images:
                self.draw_prediction(img, x, y, w, h, emotion, probability, probs)
                basename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(self.output_dir, f'{basename}_result.jpg')
                cv2.imwrite(output_path, img)

        # 计算准确率
        accuracy = correct_predictions / total_images if total_images > 0 else 0

        print(f"\n[INFO] Category: {category_name.upper()}")
        print(f"[INFO] Total images processed: {total_images}")
        print(f"[INFO] Correct predictions: {correct_predictions}")
        print(f"[INFO] Accuracy: {accuracy:.2%}")
        print("\n[STATISTICS] Prediction distribution:")
        for emotion, count in emotion_counts.items():
            percentage = count / total_images * 100 if total_images > 0 else 0
            marker = " ← TRUE LABEL" if emotion == category_name else ""
            print(f"  {emotion}: {count} ({percentage:.1f}%){marker}")

        # 返回统计结果
        return {
            'category': category_name,
            'total': total_images,
            'correct': correct_predictions,
            'accuracy': accuracy,
            'distribution': emotion_counts
        }

    def process_batch_multi_category(self, parent_dir, pattern='*.jpg', save_images=False):
        """
        批量处理多个类别的图片

        Args:
            parent_dir: 父目录（包含多个类别子目录）
            pattern: 文件匹配模式
            save_images: 是否保存标注后的图片
        """
        print("\n" + "="*70)
        print("BATCH PROCESSING - MULTI-CATEGORY MODE")
        print("="*70)

        # 查找所有子目录（假设每个子目录是一个类别）
        subdirs = [d for d in os.listdir(parent_dir)
                   if os.path.isdir(os.path.join(parent_dir, d))]

        # 过滤只保留已知的表情类别
        categories = [d for d in subdirs if d.lower() in [e.lower() for e in EMOTIONS]]

        if len(categories) == 0:
            print(f"[ERROR] No valid emotion categories found in {parent_dir}")
            print(f"[INFO] Expected categories: {', '.join(EMOTIONS)}")
            return

        print(f"[INFO] Found {len(categories)} categories: {', '.join(categories)}")
        print(f"[INFO] Save images: {save_images}")
        print()

        # 处理每个类别
        all_results = []
        for i, category in enumerate(categories, 1):
            print(f"\n{'='*70}")
            print(f"[{i}/{len(categories)}] Processing category: {category.upper()}")
            print(f"{'='*70}")

            category_path = os.path.join(parent_dir, category)
            result = self.process_batch(category_path, pattern, save_images)

            if result:
                all_results.append(result)
                # 生成该类别的统计图
                self.save_statistics_to_dir(
                    result['distribution'],
                    self.output_dir,
                    result['category'],
                    result['accuracy']
                )

        # 生成总体统计报告
        if len(all_results) > 0:
            self.generate_overall_report(all_results)

        print(f"\n{'='*70}")
        print("ALL CATEGORIES PROCESSED!")
        print(f"Results saved to: {self.output_dir}")
        print(f"{'='*70}\n")

    def generate_overall_report(self, results):
        """
        生成总体准确率报告

        Args:
            results: 所有类别的统计结果列表
        """
        print("\n" + "="*70)
        print("OVERALL ACCURACY REPORT")
        print("="*70)

        # 按准确率排序
        sorted_results = sorted(results, key=lambda x: x['accuracy'], reverse=True)

        # 打印表格
        print(f"\n{'Category':<12} {'Total':<8} {'Correct':<8} {'Accuracy':<10} {'Rank':<6}")
        print("-" * 70)
        for i, result in enumerate(sorted_results, 1):
            print(f"{result['category']:<12} {result['total']:<8} "
                  f"{result['correct']:<8} {result['accuracy']:<10.2%} #{i}")

        # 计算平均准确率
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        print("-" * 70)
        print(f"{'AVERAGE':<12} {'':<8} {'':<8} {avg_accuracy:<10.2%}")
        print()

        # 生成准确率对比图
        self.save_accuracy_comparison(sorted_results)

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

    def save_statistics_to_dir(self, emotion_counts, output_dir, category_name, accuracy=None):
        """
        保存统计图表到指定目录

        Args:
            emotion_counts: 表情统计字典
            output_dir: 输出目录
            category_name: 类别名称（用于标题）
            accuracy: 准确率（可选）
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())

        # 设置颜色：真实类别用特殊颜色标记
        colors = []
        for e in emotions:
            if e == category_name:
                colors.append((0.2, 0.8, 0.2))  # 绿色标记真实类别
            else:
                color = EMOTION_COLORS[e]
                colors.append((color[2]/255, color[1]/255, color[0]/255))

        bars = ax.bar(emotions, counts, color=colors, edgecolor='black', linewidth=1.5)

        # 添加标签
        ax.set_xlabel('Predicted Emotion', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')

        # 标题包含准确率信息
        title = f'Prediction Distribution - TRUE LABEL: {category_name.upper()}'
        if accuracy is not None:
            title += f'\nAccuracy: {accuracy:.2%}'
        ax.set_title(title, fontsize=14, fontweight='bold')

        # 添加数值标签
        total = sum(counts)
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            percentage = count / total * 100 if total > 0 else 0
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}\n({percentage:.1f}%)',
                   ha='center', va='bottom', fontsize=9)

        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=(0.2, 0.8, 0.2), edgecolor='black', label='True Label'),
            Patch(facecolor=(0.5, 0.5, 0.5), edgecolor='black', label='Other Emotions')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        output_path = os.path.join(output_dir, f'statistics_{category_name}.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Statistics saved to {output_path}")

    def save_accuracy_comparison(self, results):
        """
        保存准确率对比图

        Args:
            results: 排序后的结果列表
        """
        fig, ax = plt.subplots(figsize=(12, 7))

        categories = [r['category'] for r in results]
        accuracies = [r['accuracy'] * 100 for r in results]  # 转换为百分比

        # 使用颜色渐变：从绿到红
        colors = []
        for acc in accuracies:
            if acc >= 70:
                colors.append((0.2, 0.8, 0.2))  # 绿色
            elif acc >= 50:
                colors.append((1.0, 0.8, 0.0))  # 黄色
            else:
                colors.append((1.0, 0.2, 0.2))  # 红色

        bars = ax.bar(categories, accuracies, color=colors, edgecolor='black', linewidth=2)

        ax.set_xlabel('Emotion Category', fontsize=13, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
        ax.set_title('Accuracy Comparison by Category\n(Ranked from Highest to Lowest)',
                    fontsize=15, fontweight='bold')
        ax.set_ylim(0, 100)

        # 添加网格
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # 添加数值标签和排名
        for i, (bar, acc, result) in enumerate(zip(bars, accuracies, results), 1):
            height = bar.get_height()
            # 显示准确率
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{acc:.1f}%',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
            # 显示排名
            ax.text(bar.get_x() + bar.get_width()/2., height - 5,
                   f'#{i}',
                   ha='center', va='top', fontsize=10, color='white', fontweight='bold')
            # 显示样本数
            ax.text(bar.get_x() + bar.get_width()/2., 3,
                   f'n={result["total"]}',
                   ha='center', va='bottom', fontsize=8, color='black')

        # 添加平均线
        avg_acc = sum(accuracies) / len(accuracies)
        ax.axhline(y=avg_acc, color='blue', linestyle='--', linewidth=2, label=f'Average: {avg_acc:.1f}%')
        ax.legend(loc='lower left', fontsize=11)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'accuracy_comparison.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"[SAVE] Accuracy comparison saved to {output_path}")


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
