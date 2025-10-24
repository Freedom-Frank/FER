# eval.py
import argparse
import mindspore as ms
from mindspore.train import Model
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from mindspore.dataset import GeneratorDataset
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


from dataset import FER2013Dataset
from model import SimpleCNN
import numpy as np





def create_dataset(csv_path, usage, batch_size):
    ds_generator = FER2013Dataset(csv_path, usage=usage)
    ds = GeneratorDataset(ds_generator, column_names=['image','label'], shuffle=False)
    ds = ds.batch(batch_size)
    return ds




def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_csv', type=str, required=True)
    parser.add_argument('--ckpt_path', type=str, required=True)
    parser.add_argument('--device_target', type=str, default='CPU', choices=['CPU','GPU','Ascend'])
    parser.add_argument('--batch_size', type=int, default=64)
    return parser.parse_args()




def main():
    args = parse_args()
    context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)


    net = SimpleCNN(num_classes=7)
    param_dict = load_checkpoint(args.ckpt_path)
    load_param_into_net(net, param_dict)


    val_ds = create_dataset(args.data_csv, usage='PublicTest', batch_size=args.batch_size)


    model = Model(net)


    y_true = []
    y_pred = []
    for data in val_ds.create_dict_iterator():
        imgs = data['image']
        labels = data['label']
        preds = model.predict(ms.Tensor(imgs))
        preds = np.argmax(preds.asnumpy(), axis=1)
        y_pred.extend(preds.tolist())
        y_true.extend(labels.asnumpy().tolist())


    print('Classification report:')
    print(classification_report(y_true, y_pred, digits=4))
    print('Confusion matrix:')
    print(confusion_matrix(y_true, y_pred))


if __name__ == '__main__':
    main()