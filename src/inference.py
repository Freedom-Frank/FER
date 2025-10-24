import argparse
import cv2
import numpy as np
import mindspore as ms
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from model import SimpleCNN

EMOTIONS = ['angry','disgust','fear','happy','sad','surprise','neutral']

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

    net = SimpleCNN(7)
    load_param_into_net(net, load_checkpoint(args.ckpt_path))

    img = preprocess_image(args.image_path)
    out = net(ms.Tensor(img))
    probs = ms.ops.softmax(out)[0].asnumpy()
    idx = int(np.argmax(probs))
    print('Prediction:', EMOTIONS[idx], 'Probability:', float(probs[idx]))
    
if __name__ == '__main__':
    main()