# FER2013 项目结构说明

本文档详细说明项目的文件和目录结构。

## 📁 总体结构

```
FER/
├── README.md                      # 项目主文档
├── requirements.txt               # Python 依赖列表
├── COMMANDS.txt                   # 常用命令速查表
├── PROJECT_STRUCTURE.md           # 本文档
│
├── src/                          # 核心源代码
├── tools/                        # 工具脚本
├── scripts/                      # 自动化脚本
├── docs/                         # 文档目录
│
├── data/                         # 数据目录
├── checkpoints/                  # 模型检查点
├── output/                       # 输出结果
├── examples/                     # 示例代码
└── rank_0/                       # MindSpore 运行时输出
```

---

## 🔧 核心代码 (src/)

```
src/
├── train.py          # 训练脚本 - 训练面部表情识别模型
├── eval.py           # 评估脚本 - 在测试集上评估模型性能
├── inference.py      # 推理脚本 - 对单张图片进行表情预测
├── model.py          # 模型定义 - ResNet + 注意力机制
├── model_legacy.py   # 旧版模型 - 兼容旧的检查点文件
├── dataset.py        # 数据加载 - 数据增强、Mixup 等
└── visualize.py      # 可视化类 - FERVisualizer 实现
```

**核心功能**：
- `train.py` - 主训练入口，支持数据增强、Mixup、学习率调度等
- `eval.py` - 评估模型，输出精确率、召回率、F1-score 和混淆矩阵
- `inference.py` - 单图推理，自动检测模型版本
- `visualize.py` - 提供摄像头、图片、视频、批量处理功能

---

## 🛠️ 工具脚本 (tools/)

```
tools/
├── demo_visualization.py          # 可视化演示主程序
├── generate_correct_samples.py    # 生成预测正确的样例
├── generate_samples_simple.py     # 简化的样例生成
├── generate_samples.py            # 完整的样例生成（含对比表）
├── quick_samples.py               # 快速样例生成
├── diagnose_correct_samples.py    # 诊断工具（检查模型准确率）
│
└── legacy/                        # 废弃/临时脚本
    ├── diagnose_model.py         # 旧诊断脚本
    ├── fix_visualization.py      # 可视化修复脚本
    └── test_fix.py               # 测试修复脚本
```

**工具说明**：

### 可视化工具
- `demo_visualization.py` - 主可视化程序
  - 支持实时摄像头、图片、视频、批量处理
  - 使用方式：见 [可视化指南](docs/guides/visualization_guide.md)

### 样例生成工具
- `generate_correct_samples.py` - **推荐用于展示**
  - 只生成预测正确的样例
  - 自动过滤错误预测

- `generate_samples_simple.py` - 简化版
  - 生成混合样例（正确+错误）
  - 适合性能分析

- `generate_samples.py` - 完整版
  - 包含对比表和网格展示
  - 适合完整报告

### 诊断工具
- `diagnose_correct_samples.py` - 诊断模型性能
  - 测试每种表情的准确率
  - 预估生成样例需要的尝试次数

---

## 📜 自动化脚本 (scripts/)

```
scripts/
├── run_train.bat              # Windows 训练脚本
├── quick_test.bat             # 快速测试脚本
├── generate_samples.bat       # 样例生成脚本
├── wsl2_setup.sh              # WSL2 环境配置
├── test_visualization.sh      # 可视化测试
├── download_wsl_simple.ps1    # WSL 数据集下载
├── download_ubuntu.ps1        # Ubuntu 数据集下载
└── install_wsl2.ps1           # WSL2 安装脚本
```

**脚本用途**：
- `.bat` 文件 - Windows 批处理脚本
- `.sh` 文件 - Linux/WSL2 Shell 脚本
- `.ps1` 文件 - PowerShell 脚本

---

## 📚 文档目录 (docs/)

```
docs/
├── INDEX.md                   # 文档总索引（入口）
├── README.md                  # 文档说明
│
├── getting-started/           # 入门指南
│   ├── quickstart.md         # 快速开始
│   ├── setup.md              # 环境配置
│   └── overview.md           # 项目概览
│
├── guides/                    # 使用指南
│   ├── visualization_guide.md      # 可视化指南
│   ├── visualization_setup.md      # 可视化环境配置
│   ├── optimization.md             # 模型优化技术
│   └── model_compatibility.md      # 模型兼容性说明
│
├── samples/                   # 样例生成文档
│   ├── README.md             # 样例生成主文档
│   ├── quickstart.md         # 快速入门
│   ├── commands.md           # 命令速查
│   ├── examples.md           # 示例展示
│   ├── correct-samples.md    # 正确样例生成
│   └── troubleshooting.md    # 故障排除
│
├── troubleshooting/           # 故障排除
│   ├── README.md             # 故障排除总索引
│   └── general.md            # 通用问题
│
└── reference/                 # 参考文档
    └── changelog.md          # 版本历史
```

**文档导航**：
- **新手** → 从 `docs/INDEX.md` 开始
- **问题** → 查看 `docs/troubleshooting/`
- **样例** → 查看 `docs/samples/`

---

## 📊 数据和输出

### 数据目录 (data/)
```
data/
└── FER2013/
    └── fer2013.csv           # FER2013 数据集（需手动下载）
```

### 模型检查点 (checkpoints/)
```
checkpoints/
├── best_model.ckpt           # 最佳模型
├── fer-5_449.ckpt            # 特定 epoch 的检查点
└── ...                       # 其他检查点
```

### 输出目录 (output/)
```
output/
├── images/                   # 图片处理结果
├── videos/                   # 视频处理结果
├── webcam/                   # 摄像头截图
└── batch/                    # 批量处理结果
```

### 样例输出
```
correct_samples/              # 正确样例输出（generate_correct_samples.py）
samples_output/               # 混合样例输出（generate_samples*.py）
```

---

## 🗂️ 其他重要文件

### 根目录文件

| 文件 | 说明 |
|------|------|
| `README.md` | 项目主文档，包含快速开始、使用说明等 |
| `requirements.txt` | Python 依赖列表 |
| `COMMANDS.txt` | 常用命令速查表（复制粘贴即用） |
| `PROJECT_STRUCTURE.md` | 本文档（项目结构说明） |
| `.gitignore` | Git 忽略文件配置 |

### 配置文件
- `.gitignore` - Git 忽略规则
- `requirements.txt` - Python 依赖

---

## 🎯 快速查找

### 我想...

#### 训练模型
- **代码**：`src/train.py`
- **文档**：`docs/getting-started/quickstart.md`
- **脚本**：`scripts/run_train.bat`

#### 评估模型
- **代码**：`src/eval.py`
- **文档**：`README.md#评估脚本`

#### 生成样例
- **代码**：`tools/generate_correct_samples.py`
- **文档**：`docs/samples/README.md`
- **命令**：`COMMANDS.txt`

#### 可视化结果
- **代码**：`tools/demo_visualization.py`
- **文档**：`docs/guides/visualization_guide.md`

#### 解决问题
- **文档**：`docs/troubleshooting/README.md`
- **诊断**：`tools/diagnose_correct_samples.py`

---

## 📝 文件命名规范

### Python 脚本
- `*.py` - Python 源代码
- 核心功能 → `src/`
- 工具脚本 → `tools/`
- 废弃脚本 → `tools/legacy/`

### 文档
- `*.md` - Markdown 文档
- 大写文档 → 项目根目录（如 `README.md`）
- 小写文档 → `docs/` 子目录

### 脚本
- `*.bat` - Windows 批处理
- `*.sh` - Linux/WSL2 Shell
- `*.ps1` - PowerShell

---

## 🔄 推荐工作流

### 1. 新用户入门
```
README.md → docs/INDEX.md → docs/getting-started/quickstart.md
```

### 2. 训练模型
```
src/train.py → src/eval.py → checkpoints/best_model.ckpt
```

### 3. 生成样例
```
tools/diagnose_correct_samples.py → tools/generate_correct_samples.py
→ correct_samples/
```

### 4. 可视化
```
tools/demo_visualization.py → output/
```

---

## 💡 维护建议

### 添加新功能
1. 核心功能 → `src/`
2. 工具脚本 → `tools/`
3. 文档 → `docs/` 对应子目录

### 清理原则
- 临时文件 → `tools/legacy/`
- 废弃文档 → 移除或归档
- 输出文件 → 添加到 `.gitignore`

### 文档更新
- 修改代码 → 同步更新文档
- 新增功能 → 添加到 `docs/INDEX.md`
- 版本更新 → 更新 `docs/reference/changelog.md`

---

## 🔗 相关文档

- [主文档](README.md)
- [文档索引](docs/INDEX.md)
- [命令速查](COMMANDS.txt)
- [入门指南](docs/getting-started/quickstart.md)

---

**最后更新**：2025-01
**维护者**：项目团队
