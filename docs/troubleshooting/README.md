# 故障排除总索引

本目录包含各种常见问题的解决方案。

## 📚 文档分类

### 通用问题
- **[通用故障排除](general.md)** - 环境、安装、配置等通用问题

### 训练相关
**常见问题**：
- 训练速度慢
- 准确率低
- 内存不足
- GPU 不可用

**查看**：主 README 的"常见问题"部分

### 可视化相关
**常见问题**：
- OpenCV 无法使用
- 摄像头无法打开
- 图像显示问题

**查看**：
- [可视化指南](../guides/visualization_guide.md)
- [可视化环境配置](../guides/visualization_setup.md)

### 样例生成相关
**常见问题**：
- 无法生成正确样例
- 生成失败
- 准确率太低

**查看**：
- [样例故障排除](../samples/troubleshooting.md)

## 🎯 快速定位问题

### 按错误类型

| 错误类型 | 可能原因 | 解决方案 |
|----------|----------|----------|
| ModuleNotFoundError | 依赖未安装 | `pip install -r requirements.txt` |
| CUDA out of memory | GPU内存不足 | 减小 batch_size |
| Model load failed | 模型文件损坏 | 重新下载或训练模型 |
| Dataset not found | 数据集路径错误 | 检查路径是否正确 |
| Low accuracy | 模型未训练好 | 增加训练轮数 |

### 按使用场景

**我想训练模型但...**
- 速度太慢 → 使用 GPU、增大 batch_size
- 准确率太低 → 启用数据增强、增加训练轮数
- 内存不足 → 减小 batch_size

**我想生成样例但...**
- 找不到正确样例 → [样例故障排除](../samples/troubleshooting.md)
- 图片无法显示 → 检查 OpenCV 安装
- 速度太慢 → 使用 GPU

**我想可视化结果但...**
- 摄像头打开失败 → 检查摄像头权限
- 图像显示异常 → [可视化指南](../guides/visualization_guide.md)

## 🔍 诊断工具

### 诊断样例生成问题
```bash
python tools/diagnose_correct_samples.py \
    --csv /path/to/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt
```

### 检查环境
```bash
# 检查 MindSpore
python -c "import mindspore; print(mindspore.__version__)"

# 检查 OpenCV
python -c "import cv2; print(cv2.__version__)"

# 检查 GPU
python -c "import mindspore as ms; ms.set_context(device_target='GPU'); print('GPU available')"
```

## 📞 获取帮助

1. **查看文档**：先查看对应的文档
2. **运行诊断**：使用诊断工具定位问题
3. **查看日志**：检查错误信息
4. **搜索文档**：在本项目文档中搜索关键词

## 🔗 相关链接

- [主文档](../../README.md)
- [快速开始](../getting-started/quickstart.md)
- [样例生成](../samples/README.md)
- [可视化指南](../guides/visualization_guide.md)
