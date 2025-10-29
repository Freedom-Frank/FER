#!/usr/bin/env python3
"""
验证训练好的模型是否可用
检查模型文件大小、权重是否正确加载、预测是否正常
"""
import os
import sys
import argparse
import numpy as np

sys.path.insert(0, 'src')

import mindspore as ms
from mindspore import context
from inference import load_model_auto

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def check_model_file(ckpt_path):
    """检查模型文件"""
    print("\n" + "="*60)
    print("Step 1: Checking Model File")
    print("="*60)

    if not os.path.exists(ckpt_path):
        print(f"❌ ERROR: Model file not found: {ckpt_path}")
        return False

    file_size = os.path.getsize(ckpt_path) / (1024 * 1024)  # MB
    print(f"Model file: {ckpt_path}")
    print(f"File size: {file_size:.2f} MB")

    if file_size < 0.5:
        print(f"⚠️  WARNING: File size too small ({file_size:.2f} MB < 0.5 MB)")
        print("   This model may not be fully trained or saved correctly.")
        print("   Expected size: ~1.3 MB")
        return False
    elif file_size < 1.0:
        print(f"⚠️  WARNING: File size smaller than expected ({file_size:.2f} MB)")
        print("   Expected size: ~1.3 MB")
    else:
        print(f"✓ File size looks good ({file_size:.2f} MB)")

    return True

def test_model_loading(ckpt_path, device='CPU'):
    """测试模型加载"""
    print("\n" + "="*60)
    print("Step 2: Loading Model")
    print("="*60)

    try:
        context.set_context(mode=context.GRAPH_MODE, device_target=device)
        net = load_model_auto(ckpt_path)
        net.set_train(False)
        print("✓ Model loaded successfully")
        return net
    except Exception as e:
        print(f"❌ ERROR: Failed to load model: {e}")
        return None

def test_random_inference(net):
    """测试随机输入的推理"""
    print("\n" + "="*60)
    print("Step 3: Testing Random Inference")
    print("="*60)

    try:
        # 创建随机输入 (48x48 grayscale image)
        random_img = np.random.rand(1, 1, 48, 48).astype(np.float32)
        tensor = ms.Tensor(random_img, dtype=ms.float32)

        # 推理
        output = net(tensor)
        probs = ms.ops.softmax(output, axis=1)[0].asnumpy()

        print("Prediction probabilities:")
        for emotion, prob in zip(EMOTIONS, probs):
            bar = '#' * int(prob * 50)
            print(f"  {emotion:10s} {prob:6.2%} {bar}")

        # 检查是否为均匀分布（未训练的标志）
        is_uniform = all(abs(p - 1/7) < 0.05 for p in probs)

        if is_uniform:
            print("\n⚠️  WARNING: Probability distribution is nearly uniform (≈14.3% each)")
            print("   This suggests the model is NOT properly trained!")
            print("   All predictions are essentially random.")
            return False
        else:
            max_idx = int(np.argmax(probs))
            max_prob = float(probs[max_idx])
            print(f"\n✓ Model produces non-uniform predictions")
            print(f"  Predicted: {EMOTIONS[max_idx]} ({max_prob:.2%})")

            # 检查最高概率是否合理
            if max_prob < 0.2:
                print(f"⚠️  WARNING: Highest probability is quite low ({max_prob:.2%})")
                print("   Model may have poor confidence.")

            return True

    except Exception as e:
        print(f"❌ ERROR: Inference failed: {e}")
        return False

def test_multiple_inferences(net, num_tests=5):
    """测试多次推理，检查预测多样性"""
    print("\n" + "="*60)
    print("Step 4: Testing Multiple Random Inputs")
    print("="*60)

    predictions = []

    for i in range(num_tests):
        random_img = np.random.rand(1, 1, 48, 48).astype(np.float32)
        tensor = ms.Tensor(random_img, dtype=ms.float32)

        output = net(tensor)
        probs = ms.ops.softmax(output, axis=1)[0].asnumpy()
        pred_idx = int(np.argmax(probs))
        pred_emotion = EMOTIONS[pred_idx]
        confidence = float(probs[pred_idx])

        predictions.append((pred_emotion, confidence))
        print(f"  Test {i+1}: {pred_emotion:10s} ({confidence:.2%})")

    # 分析预测多样性
    unique_predictions = len(set([p[0] for p in predictions]))
    avg_confidence = np.mean([p[1] for p in predictions])

    print(f"\nAnalysis:")
    print(f"  Unique predictions: {unique_predictions}/{num_tests}")
    print(f"  Average confidence: {avg_confidence:.2%}")

    if unique_predictions == 1:
        print(f"⚠️  WARNING: Model always predicts the same class")
        print("   This may indicate a bias issue.")

    return True

def main():
    parser = argparse.ArgumentParser(description='Verify trained model')
    parser.add_argument('--ckpt', type=str, required=True,
                       help='Path to checkpoint file')
    parser.add_argument('--device', type=str, default='CPU',
                       choices=['CPU', 'GPU'],
                       help='Device to use')
    args = parser.parse_args()

    print("="*60)
    print("FER2013 Model Verification Tool")
    print("="*60)
    print(f"Checkpoint: {args.ckpt}")
    print(f"Device: {args.device}")

    # Step 1: Check file
    if not check_model_file(args.ckpt):
        print("\n" + "="*60)
        print("VERDICT: Model file has issues!")
        print("="*60)
        print("\nRecommendations:")
        print("1. Re-train the model with proper configuration")
        print("2. Ensure training completes without errors")
        print("3. Check that validation accuracy improves during training")
        sys.exit(1)

    # Step 2: Load model
    net = test_model_loading(args.ckpt, args.device)
    if net is None:
        print("\n" + "="*60)
        print("VERDICT: Model cannot be loaded!")
        print("="*60)
        sys.exit(1)

    # Step 3: Test inference
    inference_ok = test_random_inference(net)

    # Step 4: Test multiple inferences
    if inference_ok:
        test_multiple_inferences(net)

    # Final verdict
    print("\n" + "="*60)
    if inference_ok:
        print("VERDICT: Model appears to be WORKING! ✓")
        print("="*60)
        print("\nThe model:")
        print("  ✓ Has appropriate file size")
        print("  ✓ Loads successfully")
        print("  ✓ Produces non-uniform predictions")
        print("\nYou can now use this model for visualization!")
        print("\nNext steps:")
        print(f"  python tools/demo_visualization.py --mode image --ckpt {args.ckpt} --input test.jpg")
        print(f"  python tools/generate_correct_samples.py --csv data/... --ckpt {args.ckpt} --num_samples 3")
    else:
        print("VERDICT: Model has ISSUES! ⚠️")
        print("="*60)
        print("\nThe model appears to be untrained or corrupted.")
        print("Predictions are uniform (random), which means:")
        print("  - Model weights are not properly trained")
        print("  - OR model file is incomplete/corrupted")
        print("\nRecommendations:")
        print("1. Re-train the model using the training scripts")
        print("2. Monitor training progress (loss should decrease, accuracy should increase)")
        print("3. Ensure training completes successfully")
        print("4. Use the provided train_50_epochs.sh or train_50_epochs.bat scripts")

    print("="*60)

if __name__ == '__main__':
    main()
