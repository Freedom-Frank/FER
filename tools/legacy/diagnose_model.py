#!/usr/bin/env python3
"""
诊断模型问题的脚本
"""
import sys
sys.path.insert(0, 'src')

import numpy as np
import cv2
import mindspore as ms
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from model import SimpleCNN
try:
    from model_legacy import SimpleCNN_Legacy
except ImportError:
    SimpleCNN_Legacy = None

# 表情标签
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def test_model_predictions():
    """测试模型预测是否正常"""
    print("="*60)
    print("诊断模型问题")
    print("="*60)

    # 设置上下文
    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')

    # 加载模型
    ckpt_path = 'checkpoints/best_model.ckpt'
    print(f"\n[1] 加载模型: {ckpt_path}")

    param_dict = load_checkpoint(ckpt_path)

    # 检查模型结构
    print(f"\n[2] 检查模型参数:")
    for key in list(param_dict.keys())[:5]:
        print(f"  {key}: {param_dict[key].shape}")

    # 检测模型版本
    classifier_key = 'classifier.0.weight'
    if classifier_key in param_dict:
        classifier_shape = param_dict[classifier_key].shape
        print(f"\n  分类器形状: {classifier_shape}")

        if classifier_shape == (128, 128):
            print("  检测到: 旧版本模型 (可能未正确训练)")
            if SimpleCNN_Legacy:
                net = SimpleCNN_Legacy(7)
            else:
                print("[ERROR] 需要 model_legacy.py")
                return
        else:
            print("  检测到: 当前版本模型")
            net = SimpleCNN(7)
    else:
        net = SimpleCNN(7)

    load_param_into_net(net, param_dict)
    net.set_train(False)

    # 测试：随机输入
    print(f"\n[3] 测试随机输入:")
    random_input = np.random.randn(1, 1, 48, 48).astype('float32')
    output = net(ms.Tensor(random_input))
    probs = ms.ops.softmax(output)[0].asnumpy()

    print("  概率分布:")
    for emotion, prob in zip(EMOTIONS, probs):
        print(f"    {emotion:10s}: {prob:.4f}")

    max_prob = np.max(probs)
    min_prob = np.min(probs)
    std_prob = np.std(probs)

    print(f"\n  统计:")
    print(f"    最大概率: {max_prob:.4f}")
    print(f"    最小概率: {min_prob:.4f}")
    print(f"    标准差:   {std_prob:.4f}")

    # 判断模型是否正常
    print(f"\n[4] 诊断结果:")
    if std_prob < 0.1:
        print("  ❌ 问题: 模型输出接近均匀分布 (标准差 < 0.1)")
        print("     可能原因:")
        print("       1. 模型未训练或训练不充分")
        print("       2. 使用了错误的模型文件")
        print("       3. 模型权重初始化问题")
        print("\n  建议:")
        print("       - 检查训练日志")
        print("       - 使用其他checkpoint文件 (如 fer-5_449.ckpt)")
        print("       - 重新训练模型")
    else:
        print("  ✓ 模型输出分布正常")

    # 测试：全0输入
    print(f"\n[5] 测试全0输入:")
    zero_input = np.zeros((1, 1, 48, 48), dtype='float32')
    output = net(ms.Tensor(zero_input))
    probs = ms.ops.softmax(output)[0].asnumpy()

    print("  概率分布:")
    for emotion, prob in zip(EMOTIONS, probs):
        print(f"    {emotion:10s}: {prob:.4f}")

    # 测试：全1输入
    print(f"\n[6] 测试全1输入:")
    one_input = np.ones((1, 1, 48, 48), dtype='float32')
    output = net(ms.Tensor(one_input))
    probs = ms.ops.softmax(output)[0].asnumpy()

    print("  概率分布:")
    for emotion, prob in zip(EMOTIONS, probs):
        print(f"    {emotion:10s}: {prob:.4f}")

    print("\n" + "="*60)


def test_face_detection():
    """测试人脸检测"""
    print("\n" + "="*60)
    print("测试人脸检测")
    print("="*60)

    # 加载人脸检测器
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # 测试不同参数
    test_images = [
        'output/images/PrivateTest_5142883_annotated.jpg',
        'output/images/PrivateTest_6518376_annotated.jpg'
    ]

    for img_path in test_images:
        print(f"\n测试图片: {img_path}")
        img = cv2.imread(img_path)
        if img is None:
            print(f"  无法读取图片")
            continue

        print(f"  图片大小: {img.shape}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 测试不同参数
        params = [
            {'scaleFactor': 1.1, 'minNeighbors': 5, 'minSize': (30, 30)},
            {'scaleFactor': 1.05, 'minNeighbors': 3, 'minSize': (20, 20)},
            {'scaleFactor': 1.2, 'minNeighbors': 4, 'minSize': (40, 40)},
        ]

        for i, param in enumerate(params, 1):
            faces = face_cascade.detectMultiScale(gray, **param)
            print(f"  参数组{i}: 检测到 {len(faces)} 个人脸")
            print(f"    {param}")
            if len(faces) > 0:
                for j, (x, y, w, h) in enumerate(faces):
                    print(f"    人脸{j+1}: x={x}, y={y}, w={w}, h={h}")


if __name__ == '__main__':
    test_model_predictions()
    test_face_detection()
