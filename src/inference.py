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

EMOTIONS = ['angry','disgust','fear','happy','sad','surprise','neutral']

def load_model_auto(ckpt_path):
    """自动检测并加载正确版本的模型"""
    param_dict = load_checkpoint(ckpt_path)
    classifier_key = 'classifier.0.weight'

    if classifier_key in param_dict:
        classifier_shape = param_dict[classifier_key].shape
        print(f'[INFO] Detected classifier shape: {classifier_shape}')

        # 旧版本模型
        if classifier_shape == (128, 128):
            if SimpleCNN_Legacy is None:
                raise ImportError("Legacy model detected but model_legacy.py not found")
            print('[INFO] Loading legacy model')
            net = SimpleCNN_Legacy(7)
            load_param_into_net(net, param_dict)
            return net

        # 新版本模型
        elif classifier_shape == (256, 512):
            print('[INFO] Loading current model')
            net = SimpleCNN(7)
            load_param_into_net(net, param_dict)
            return net

    # 默认尝试当前模型
    print('[INFO] Using current model')
    net = SimpleCNN(7)
    load_param_into_net(net, param_dict)
    return net

def preprocess_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48,48))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, (0,1))
    return img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', required=True)
    parser.add_argument('--ckpt_path', required=True)
    parser.add_argument('--device_target', default='CPU')
    args = parser.parse_args()

    context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)

    # 使用自动检测加载模型
    net = load_model_auto(args.ckpt_path)

    img = preprocess_image(args.image_path)
    out = net(ms.Tensor(img))
    probs = ms.ops.softmax(out)[0].asnumpy()
    idx = int(np.argmax(probs))
    print('Prediction:', EMOTIONS[idx], 'Probability:', float(probs[idx]))
    
if __name__ == '__main__':
    main()