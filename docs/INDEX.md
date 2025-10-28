# FER2013 项目文档索引

欢迎使用 FER2013 面部表情识别项目文档。本索引帮助您快速找到所需信息。

## 🚀 快速导航

### 新手入门
1. **[快速开始](getting-started/quickstart.md)** - 5分钟快速上手
2. **[环境配置](getting-started/setup.md)** - 详细的安装和配置步骤
3. **[入门概览](getting-started/overview.md)** - 项目整体介绍

### 核心功能
- **[训练模型](../README.md#快速开始训练)** - 如何训练自己的模型
- **[评估模型](../README.md#评估脚本-srcevalpy)** - 在测试集上评估性能
- **[推理预测](../README.md#推理脚本-srcinferencepy)** - 对单张图片进行预测
- **[可视化功能](guides/visualization_guide.md)** - 实时摄像头、图片、视频处理

### 样例生成
- **[样例生成指南](samples/README.md)** - 完整的样例生成文档
- **[快速入门](samples/quickstart.md)** - 5分钟学会生成样例
- **[命令速查](samples/commands.md)** - 所有可用命令
- **[示例展示](samples/examples.md)** - 样例格式和效果

## 📚 文档结构

```
docs/
├── INDEX.md                      # 本文档（总索引）
├── getting-started/              # 入门指南
│   ├── quickstart.md            # 快速开始
│   ├── setup.md                 # 环境配置
│   └── overview.md              # 项目概览
├── guides/                       # 使用指南
│   ├── visualization_guide.md   # 可视化指南
│   ├── visualization_setup.md   # 可视化环境配置
│   ├── optimization.md          # 模型优化
│   └── model_compatibility.md   # 模型兼容性
├── samples/                      # 样例生成
│   ├── README.md                # 样例生成主文档
│   ├── quickstart.md            # 快速入门
│   ├── commands.md              # 命令速查
│   ├── examples.md              # 示例展示
│   ├── correct-samples.md       # 正确样例生成
│   └── troubleshooting.md       # 故障排除
├── troubleshooting/              # 故障排除
│   ├── README.md                # 故障排除总索引
│   └── general.md               # 通用问题
└── reference/                    # 参考文档
    └── changelog.md             # 版本历史
```

## 🎯 按任务查找

### 我想要...

#### 训练模型
1. [环境配置](getting-started/setup.md) - 配置环境
2. [快速开始](getting-started/quickstart.md#快速开始训练) - 开始训练
3. [模型优化](guides/optimization.md) - 提升准确率

#### 测试模型
1. [评估脚本](../README.md#评估脚本-srcevalpy) - 评估性能
2. [推理脚本](../README.md#推理脚本-srcinferencepy) - 单图预测

#### 生成样例展示
1. [样例快速入门](samples/quickstart.md) - 快速开始
2. [样例命令](samples/commands.md) - 复制粘贴命令
3. [正确样例](samples/correct-samples.md) - 只要正确的

#### 可视化功能
1. [可视化指南](guides/visualization_guide.md) - 完整功能说明
2. [环境配置](guides/visualization_setup.md) - 配置可视化环境
3. [演示脚本](../README.md#可视化演示脚本-demo_visualizationpy) - 使用方法

#### 解决问题
1. [故障排除总索引](troubleshooting/README.md) - 找到对应的问题
2. [通用问题](troubleshooting/general.md) - 常见问题
3. [样例故障排除](samples/troubleshooting.md) - 样例生成问题

## 📖 按角色查找

### 初学者
**推荐路径**：
1. [项目概览](getting-started/overview.md)
2. [快速开始](getting-started/quickstart.md)
3. [常见问题](../README.md#常见问题-faq)

### 开发者
**推荐路径**：
1. [环境配置](getting-started/setup.md)
2. [模型优化](guides/optimization.md)
3. [模型兼容性](guides/model_compatibility.md)

### 研究者
**推荐路径**：
1. [技术架构](../README.md#技术架构)
2. [模型优化](guides/optimization.md)
3. [性能指标](../README.md#性能指标)

### 项目展示者
**推荐路径**：
1. [样例快速入门](samples/quickstart.md)
2. [正确样例生成](samples/correct-samples.md)
3. [可视化功能](guides/visualization_guide.md)

## 🔧 工具和脚本

### 训练和评估
- `src/train.py` - 训练脚本
- `src/eval.py` - 评估脚本
- `src/inference.py` - 推理脚本

### 样例生成
- `tools/demo_visualization.py` - 可视化演示
- `tools/generate_correct_samples.py` - 正确样例生成
- `tools/generate_samples_simple.py` - 简化样例生成
- `tools/diagnose_correct_samples.py` - 诊断工具

### 辅助脚本
- `scripts/run_train.bat` - Windows 训练脚本
- `scripts/wsl2_setup.sh` - WSL2 自动配置
- `scripts/generate_samples.bat` - 样例生成脚本

详见：[项目结构](../README.md#项目结构)

## 📊 性能指标

| 版本 | 准确率 | 主要技术 |
|------|--------|----------|
| v1.0 | 66.91% | 基础 ResNet |
| v2.0 | 70.09% | + 注意力机制 + 数据增强 |
| v3.0 | 72-74% | + 超参数优化 |
| v4.0 | 74-77% | + Mixup 增强 |

详见：[性能指标](../README.md#性能指标)

## ❓ 常见问题快速链接

- [Windows 下如何使用 GPU？](../README.md#q-windows-下如何使用-gpu)
- [训练速度慢怎么办？](../README.md#q-训练速度慢怎么办)
- [如何提高准确率？](../README.md#q-如何提高准确率)
- [无法生成正确样例？](samples/troubleshooting.md)
- [可视化无法使用？](guides/visualization_setup.md)

## 🔗 外部资源

- [FER2013 数据集](https://www.kaggle.com/datasets/msambare/fer2013)
- [MindSpore 官方文档](https://www.mindspore.cn/)
- [项目 GitHub](https://github.com/your-repo)

## 📝 文档更新

最后更新：2025-01

查看完整更新历史：[版本历史](reference/changelog.md)

## 💡 使用建议

1. **新用户**：按顺序阅读"入门指南"
2. **遇到问题**：先查看"故障排除"
3. **深入学习**：阅读"使用指南"部分
4. **查找命令**：使用"命令速查"快速找到需要的命令

---

**提示**：使用 Ctrl+F (Windows) 或 Cmd+F (Mac) 在文档中搜索关键词
