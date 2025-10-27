# model_legacy.py
"""
旧版本的模型定义，用于兼容旧的检查点文件
根据错误信息，旧模型的分类器结构为: 128 -> 128 -> 7
"""
import mindspore.nn as nn
import mindspore.ops as ops
from mindspore.common import initializer as init


class ChannelAttention(nn.Cell):
    """通道注意力模块（SENet）"""
    def __init__(self, channels, reduction=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = ops.AdaptiveAvgPool2D((1, 1))
        self.fc = nn.SequentialCell([
            nn.Dense(channels, channels // reduction),
            nn.ReLU(),
            nn.Dense(channels // reduction, channels),
            nn.Sigmoid()
        ])
        self.reshape = ops.Reshape()

    def construct(self, x):
        b, c, _, _ = x.shape
        y = self.avg_pool(x)
        y = self.reshape(y, (b, c))
        y = self.fc(y)
        y = self.reshape(y, (b, c, 1, 1))
        return x * y


class SpatialAttention(nn.Cell):
    """空间注意力模块"""
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, pad_mode='pad',
                             padding=kernel_size//2, has_bias=False)
        self.sigmoid = nn.Sigmoid()
        self.concat = ops.Concat(axis=1)

    def construct(self, x):
        avg_out = ops.mean(x, 1, keep_dims=True)
        max_out = ops.max(x, 1, keep_dims=True)[0]
        x_cat = self.concat((avg_out, max_out))
        attention = self.sigmoid(self.conv(x_cat))
        return x * attention


class ResidualBlock(nn.Cell):
    """增强的残差块，添加注意力机制"""
    def __init__(self, in_channels, out_channels, stride=1, use_attention=True):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride,
                               pad_mode='pad', padding=1, has_bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1,
                               pad_mode='pad', padding=1, has_bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.use_attention = use_attention
        if use_attention:
            self.channel_attention = ChannelAttention(out_channels)
            self.spatial_attention = SpatialAttention()

        self.downsample = None
        if stride != 1 or in_channels != out_channels:
            self.downsample = nn.SequentialCell([
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, has_bias=False),
                nn.BatchNorm2d(out_channels)
            ])

    def construct(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.use_attention:
            out = self.channel_attention(out)
            out = self.spatial_attention(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out = out + identity
        out = self.relu(out)

        return out


class SimpleCNN_Legacy(nn.Cell):
    """
    旧版本模型结构，用于加载旧的检查点
    分类器结构: 128 -> 128 -> 7
    """
    def __init__(self, num_classes=7):
        super(SimpleCNN_Legacy, self).__init__()

        # 初始卷积层
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, pad_mode='pad', padding=1, has_bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()

        # 残差块层 - 调整到输出 128 通道
        self.layer1 = self._make_layer(64, 64, 2, stride=1)
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        self.layer3 = self._make_layer(128, 128, 2, stride=2)  # 保持 128
        self.layer4 = self._make_layer(128, 128, 2, stride=2)  # 保持 128

        # 全局平均池化
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()

        # 旧版分类器: 128 -> 128 -> 7
        self.classifier = nn.SequentialCell([
            nn.Dense(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Dense(128, num_classes)
        ])

        # 权重初始化
        self._initialize_weights()

    def _make_layer(self, in_channels, out_channels, blocks, stride, use_attention=True):
        layers = []
        layers.append(ResidualBlock(in_channels, out_channels, stride, use_attention))
        for _ in range(1, blocks):
            layers.append(ResidualBlock(out_channels, out_channels, 1, use_attention))
        return nn.SequentialCell(layers)

    def _initialize_weights(self):
        for m in self.cells():
            if isinstance(m, nn.Conv2d):
                m.weight.set_data(init.initializer(init.HeUniform(), m.weight.shape, m.weight.dtype))
            elif isinstance(m, nn.Dense):
                m.weight.set_data(init.initializer(init.HeUniform(), m.weight.shape, m.weight.dtype))
                if m.bias is not None:
                    m.bias.set_data(init.initializer(init.Zero(), m.bias.shape, m.bias.dtype))

    def construct(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.global_pool(x)
        x = self.flatten(x)
        x = self.classifier(x)

        return x
