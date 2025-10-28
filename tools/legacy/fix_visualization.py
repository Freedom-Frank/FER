#!/usr/bin/env python3
"""
修复后的可视化脚本 - 解决人脸检测和模型预测问题
"""
import sys
sys.path.insert(0, 'src')

import cv2
import numpy as np
import mindspore as ms
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from model import SimpleCNN
import matplotlib.pyplot as plt
import os

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_COLORS = {
    'angry': (0, 0, 255),
    'disgust': (0, 255, 0),
    'fear': (255, 0, 255),
    'happy': (0, 255, 255),
    'sad': (255, 0, 0),
    'surprise': (255, 165, 0),
    'neutral': (128, 128, 128)
}

def test_different_checkpoints(image_path):
    """测试不同的checkpoint文件"""
    print("="*60)
    print("测试不同的checkpoint文件")
    print("="*60)

    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')

    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return

    print(f"\n测试图片: {image_path}")
    print(f"图片大小: {img.shape}")

    # 改进的人脸检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用更宽松的参数
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # 尝试多个参数组合
    all_faces = []
    param_sets = [
        {'scaleFactor': 1.05, 'minNeighbors': 3, 'minSize': (20, 20)},
        {'scaleFactor': 1.1, 'minNeighbors': 4, 'minSize': (30, 30)},
        {'scaleFactor': 1.15, 'minNeighbors': 5, 'minSize': (25, 25)},
    ]

    for params in param_sets:
        faces = face_cascade.detectMultiScale(gray, **params)
        if len(faces) > 0:
            all_faces.extend(faces)

    if len(all_faces) == 0:
        print("⚠️  未检测到人脸")
        print("\n可能的原因:")
        print("  1. 图片不包含清晰的正面人脸")
        print("  2. 图片分辨率过低")
        print("  3. 人脸被遮挡或角度不佳")
        return

    # 去重 (简单的重叠检测)
    unique_faces = []
    for face in all_faces:
        is_duplicate = False
        x1, y1, w1, h1 = face
        for existing in unique_faces:
            x2, y2, w2, h2 = existing
            # 检查重叠
            overlap_x = max(0, min(x1+w1, x2+w2) - max(x1, x2))
            overlap_y = max(0, min(y1+h1, y2+h2) - max(y1, y2))
            overlap_area = overlap_x * overlap_y
            if overlap_area > 0.5 * min(w1*h1, w2*h2):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_faces.append(face)

    faces = np.array(unique_faces)
    print(f"✓ 检测到 {len(faces)} 个人脸")

    # 测试不同的checkpoint
    checkpoints = [
        'checkpoints/best_model.ckpt',
        'checkpoints/fer-5_449.ckpt',
        'checkpoints/fer-5_404.ckpt',
    ]

    for ckpt_path in checkpoints:
        if not os.path.exists(ckpt_path):
            continue

        print(f"\n{'='*60}")
        print(f"测试: {ckpt_path}")
        print('='*60)

        try:
            # 加载模型
            param_dict = load_checkpoint(ckpt_path)
            net = SimpleCNN(7)
            load_param_into_net(net, param_dict)
            net.set_train(False)

            # 处理第一个人脸
            x, y, w, h = faces[0]
            face_img = img[y:y+h, x:x+w]

            # 预处理
            face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY) if len(face_img.shape) == 3 else face_img
            face_resized = cv2.resize(face_gray, (48, 48))
            face_normalized = face_resized.astype('float32') / 255.0
            face_tensor = np.expand_dims(face_normalized, (0, 1))

            # 预测
            output = net(ms.Tensor(face_tensor))
            probs = ms.ops.softmax(output)[0].asnumpy()

            # 显示结果
            print("\n预测结果:")
            sorted_indices = np.argsort(probs)[::-1]
            for idx in sorted_indices:
                emotion = EMOTIONS[idx]
                prob = probs[idx]
                bar = '█' * int(prob * 50)
                print(f"  {emotion:10s}: {prob:6.2%}  {bar}")

            max_idx = np.argmax(probs)
            predicted_emotion = EMOTIONS[max_idx]
            print(f"\n最终预测: {predicted_emotion} ({probs[max_idx]:.2%})")

            # 统计信息
            std = np.std(probs)
            print(f"概率标准差: {std:.4f}")

            if std < 0.05:
                print("⚠️  警告: 概率分布过于均匀，模型可能未正确训练")
            elif std < 0.1:
                print("⚠️  警告: 概率分布较均匀，模型性能可能不佳")
            else:
                print("✓ 概率分布正常")

        except Exception as e:
            print(f"❌ 加载失败: {e}")

    print("\n" + "="*60)


def create_improved_visualization(image_path, ckpt_path, output_dir='output/fixed'):
    """创建改进的可视化结果"""
    print(f"\n{'='*60}")
    print("创建改进的可视化")
    print('='*60)

    os.makedirs(output_dir, exist_ok=True)

    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')

    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return

    # 改进的人脸检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # 使用更好的参数
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(20, 20),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) == 0:
        print("未检测到人脸")
        return

    print(f"检测到 {len(faces)} 个人脸")

    # 加载模型
    param_dict = load_checkpoint(ckpt_path)
    net = SimpleCNN(7)
    load_param_into_net(net, param_dict)
    net.set_train(False)

    # 创建输出图像
    img_annotated = img.copy()

    for i, (x, y, w, h) in enumerate(faces):
        # 提取人脸
        face_img = img[y:y+h, x:x+w]

        # 预处理
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY) if len(face_img.shape) == 3 else face_img
        face_resized = cv2.resize(face_gray, (48, 48))
        face_normalized = face_resized.astype('float32') / 255.0
        face_tensor = np.expand_dims(face_normalized, (0, 1))

        # 预测
        output = net(ms.Tensor(face_tensor))
        probs = ms.ops.softmax(output)[0].asnumpy()

        max_idx = np.argmax(probs)
        emotion = EMOTIONS[max_idx]
        probability = probs[max_idx]

        print(f"\n人脸 {i+1}: {emotion} ({probability:.2%})")

        # 绘制边框和标签
        color = EMOTION_COLORS[emotion]
        cv2.rectangle(img_annotated, (x, y), (x+w, y+h), color, 2)

        label = f"{emotion}: {probability:.1%}"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

        # 标签背景
        cv2.rectangle(img_annotated,
                     (x, y - label_size[1] - 10),
                     (x + label_size[0], y),
                     color, -1)

        # 标签文字
        cv2.putText(img_annotated, label, (x, y - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 保存详细结果图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # 显示人脸
        ax1.imshow(face_resized, cmap='gray')
        ax1.set_title(f'Face {i+1}: {emotion}', fontsize=14, fontweight='bold')
        ax1.axis('off')

        # 概率柱状图
        colors = [EMOTION_COLORS[e] for e in EMOTIONS]
        colors = [(b/255, g/255, r/255) for r, g, b in colors]

        bars = ax2.barh(EMOTIONS, probs, color=colors)
        ax2.set_xlabel('Probability', fontsize=12)
        ax2.set_title('Emotion Probabilities', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 1)

        for bar, prob in zip(bars, probs):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'{prob:.1%}',
                    ha='left', va='center', fontsize=10)

        plt.tight_layout()
        result_path = os.path.join(output_dir, f'face_{i+1}_detail.png')
        plt.savefig(result_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  保存详细图: {result_path}")

    # 保存标注图
    basename = os.path.splitext(os.path.basename(image_path))[0]
    annotated_path = os.path.join(output_dir, f'{basename}_fixed.jpg')
    cv2.imwrite(annotated_path, img_annotated)
    print(f"\n保存标注图: {annotated_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python fix_visualization.py <image_path> [checkpoint_path]")
        print("\n示例:")
        print("  python fix_visualization.py output/images/PrivateTest_5142883_annotated.jpg")
        print("  python fix_visualization.py test.jpg checkpoints/fer-5_449.ckpt")
        sys.exit(1)

    image_path = sys.argv[1]
    ckpt_path = sys.argv[2] if len(sys.argv) > 2 else 'checkpoints/fer-5_449.ckpt'

    # 测试不同的checkpoints
    test_different_checkpoints(image_path)

    # 创建改进的可视化
    create_improved_visualization(image_path, ckpt_path)

    print("\n✓ 完成!")
