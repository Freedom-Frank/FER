# 样例生成指南

本目录包含所有关于生成面部表情识别样例的文档。

## 📚 文档导航

### 快速开始
- **[快速入门](quickstart.md)** - 5分钟学会生成样例
- **[命令速查](commands.md)** - 所有可用命令

### 详细指南
- **[正确样例生成](correct-samples.md)** - 只生成预测正确的样例
- **[示例展示](examples.md)** - 样例格式和效果展示

### 故障排除
- **[故障排除指南](troubleshooting.md)** - 解决常见问题

## 🎯 快速开始

### 最简单的方式

```bash
# 处理已有图片
python tools/demo_visualization.py --mode image --ckpt checkpoints/best_model.ckpt --input test.jpg

# 从数据集生成样例
python tools/generate_correct_samples.py \
    --csv /mnt/e/Users/Meng/Datasets/FER2013/fer2013.csv \
    --ckpt checkpoints/best_model.ckpt \
    --num_samples 3
```

## 📊 样例类型对比

| 工具 | 用途 | 输出 | 推荐场景 |
|------|------|------|----------|
| `demo_visualization.py` | 处理已有图片 | 标注图 + 概率图 | 处理自己的图片 |
| `generate_correct_samples.py` | 生成正确样例 | 只包含预测正确的样例 | 项目展示、演示 |
| `generate_samples_simple.py` | 生成混合样例 | 包含正确和错误样例 | 性能分析、误差分析 |
| `generate_samples.py` | 完整报告 | 样例 + 对比表 + 统计 | 完整的性能报告 |

## 🔗 相关资源

### 工具脚本位置
所有工具脚本位于 `tools/` 目录：
- `tools/demo_visualization.py` - 可视化演示
- `tools/generate_correct_samples.py` - 正确样例生成
- `tools/generate_samples_simple.py` - 简化样例生成
- `tools/generate_samples.py` - 完整样例生成
- `tools/diagnose_correct_samples.py` - 诊断工具

### 其他文档
- [主文档](../../README.md)
- [可视化指南](../guides/visualization_guide.md)
- [入门指南](../getting-started/quickstart.md)

## 💡 常见问题

**Q: 无法生成正确样例怎么办？**
A: 查看 [故障排除指南](troubleshooting.md)

**Q: 如何选择合适的工具？**
A: 查看上面的"样例类型对比"表格

**Q: 样例文件保存在哪里？**
A: 默认保存在 `correct_samples/` 或 `samples_output/` 目录

## 🎨 样例格式

每个样例包含两部分：
- **左侧**：48x48 灰度人脸图像 + 真实表情标签
- **右侧**：7种表情的概率分布柱状图 + 预测结果

颜色编码：
- 🟢 绿色：预测正确
- 🔴 红色：预测错误

详见 [示例展示](examples.md)
