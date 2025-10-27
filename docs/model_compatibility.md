# 模型兼容性说明

## 问题背景

如果你在使用可视化功能时遇到以下错误：

```
RuntimeError: For 'load_param_into_net', classifier.0.weight in the argument 'net' should have the same shape as classifier.0.weight in the argument 'parameter_dict'. But got its shape (256, 512) in the argument 'net' and shape (128, 128) in the argument 'parameter_dict'.
```

这是因为你的模型检查点文件是用**旧版本**的模型结构训练的，而当前代码使用的是**新版本**的模型结构。

## 模型版本对比

### 旧版本模型（Legacy）
- **分类器结构**: 128 → 128 → 7
- **特征提取**: 最后一层输出 128 通道
- **检查点特征**: `classifier.0.weight` shape = (128, 128)

### 新版本模型（Current）
- **分类器结构**: 512 → 256 → 128 → 7
- **特征提取**: 最后一层输出 512 通道
- **检查点特征**: `classifier.0.weight` shape = (256, 512)

## 解决方案

### 方案 1: 自动检测加载（推荐）✅

**已自动实现！** 现在的代码会自动检测检查点版本并加载正确的模型。

你只需要正常运行命令即可：

```bash
# 可视化功能会自动检测模型版本
python3 demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input test.jpg

# 推理脚本也会自动检测
python3 src/inference.py --ckpt_path checkpoints/best_model.ckpt --image_path test.jpg
```

运行时会看到类似输出：
```
[INFO] Loading model from checkpoints/best_model.ckpt
[INFO] Detected classifier shape: (128, 128)
[INFO] Loading legacy model (128 -> 128 -> 7)
[INFO] Visualizer initialized. Output: output/images
```

### 方案 2: 重新训练模型（可选）

如果你想使用新版本的模型结构（性能更好），可以重新训练：

```bash
# 使用新版本模型训练
python3 src/train.py \
  --data_csv data/FER2013/fer2013.csv \
  --device_target GPU \
  --batch_size 96 \
  --epochs 200 \
  --augment \
  --mixup
```

这会生成使用新模型结构的检查点文件。

## 技术细节

### 自动检测机制

代码会检查检查点文件中 `classifier.0.weight` 的形状：

```python
def _load_model_with_auto_detection(self, ckpt_path):
    param_dict = load_checkpoint(ckpt_path)
    classifier_key = 'classifier.0.weight'

    if classifier_key in param_dict:
        classifier_shape = param_dict[classifier_key].shape

        # 旧版本: (128, 128)
        if classifier_shape == (128, 128):
            net = SimpleCNN_Legacy(7)
            load_param_into_net(net, param_dict)
            return net

        # 新版本: (256, 512)
        elif classifier_shape == (256, 512):
            net = SimpleCNN(7)
            load_param_into_net(net, param_dict)
            return net
```

### 新增文件

- **[src/model_legacy.py](src/model_legacy.py)** - 旧版本模型定义
  - 包含 `SimpleCNN_Legacy` 类
  - 用于加载旧的检查点文件

### 修改文件

1. **[src/visualize.py](src/visualize.py)**
   - 添加了 `_load_model_with_auto_detection()` 方法
   - 自动检测并加载正确版本的模型

2. **[src/inference.py](src/inference.py)**
   - 添加了 `load_model_auto()` 函数
   - 支持自动检测模型版本

## 检查你的模型版本

如果想手动检查你的模型版本，可以运行：

```bash
python3 -c "
import mindspore as ms
ckpt = ms.load_checkpoint('checkpoints/best_model.ckpt')
shape = ckpt['classifier.0.weight'].shape
print(f'Classifier shape: {shape}')
if shape == (128, 128):
    print('Model version: Legacy (old)')
elif shape == (256, 512):
    print('Model version: Current (new)')
else:
    print('Model version: Unknown')
"
```

## 性能对比

| 模型版本 | 分类器参数 | 性能 | 说明 |
|---------|-----------|------|------|
| Legacy | 128→128→7 | 较好 | 旧版本检查点 |
| Current | 512→256→128→7 | 更好 | 新版本，参数更多 |

建议：如果有时间，重新训练使用新版本模型。

## 常见问题

### Q1: 为什么有两个版本的模型？

A: 项目在开发过程中进行了优化，新版本模型结构更深，性能更好。为了兼容之前训练的模型，保留了旧版本的支持。

### Q2: 我应该使用哪个版本？

A:
- 如果已有旧版本检查点：自动加载功能会处理，无需更改
- 如果要重新训练：会自动使用新版本，性能更好

### Q3: 自动检测会影响性能吗？

A: 不会。检测只在模型加载时进行一次，加载后的推理速度完全相同。

### Q4: 我可以手动指定模型版本吗？

A: 当前是自动检测，如需手动指定，可以修改代码：

```python
# 手动加载旧版本
from model_legacy import SimpleCNN_Legacy
net = SimpleCNN_Legacy(7)

# 手动加载新版本
from model import SimpleCNN
net = SimpleCNN(7)
```

## 总结

✅ **无需任何操作** - 代码已自动处理模型版本兼容性

✅ **自动检测** - 根据检查点自动选择正确的模型结构

✅ **向后兼容** - 旧的检查点文件仍然可以使用

✅ **性能优化** - 新训练的模型使用更好的结构

只需要正常使用可视化功能即可，系统会自动处理一切！

---

**相关文件:**
- [src/model.py](src/model.py) - 新版本模型（当前）
- [src/model_legacy.py](src/model_legacy.py) - 旧版本模型（兼容）
- [src/visualize.py](src/visualize.py) - 可视化工具（已更新）
- [src/inference.py](src/inference.py) - 推理脚本（已更新）
