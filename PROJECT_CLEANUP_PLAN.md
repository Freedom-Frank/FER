# 项目整理计划

## 当前问题分析

### 冗余文档（需要合并）
1. **快速修复文档冗余**：
   - `QUICK_FIX.md` (5.2KB) - 新的样例生成快速修复
   - `QUICKFIX.md` (2.7KB) - 旧的可视化快速修复
   - **建议**：合并为统一的 `docs/QUICK_FIX_GUIDE.md`

2. **README 冗余**：
   - `README_VISUALIZATION_FIX.md` (5KB) - 可视化修复说明
   - 内容已整合到主 README
   - **建议**：删除

3. **样例生成文档冗余**：
   - `SAMPLES_README.md` (8.6KB) - 详细说明
   - `SAMPLES_QUICKSTART.md` (3KB) - 快速入门
   - `SAMPLES_EXAMPLES.md` (18.7KB) - 示例展示
   - `GENERATE_SAMPLES_COMMANDS.md` (9.2KB) - 命令速查
   - `CORRECT_SAMPLES_README.md` (9.9KB) - 正确样例说明
   - `TROUBLESHOOTING_SAMPLES.md` (10.4KB) - 故障排除
   - **建议**：整合为 `docs/samples/` 目录下的结构化文档

4. **命令参考冗余**：
   - `COPY_PASTE_COMMANDS.txt` - 命令速查
   - 各种 README 中的命令
   - **建议**：保留，作为快速参考

### 冗余脚本（需要合并/删除）
1. **诊断脚本**：
   - `diagnose_model.py` (5.4KB) - 旧的诊断脚本
   - `diagnose_correct_samples.py` (3.9KB) - 新的诊断脚本
   - **建议**：合并为 `tools/diagnose.py`

2. **修复脚本（临时）**：
   - `fix_visualization.py` (9.8KB) - 可视化修复脚本
   - `test_fix.py` (3KB) - 测试修复
   - **建议**：移到 `tools/legacy/` 或删除

3. **样例生成脚本**：
   - `generate_samples.py` (12.8KB) - 完整版
   - `generate_samples_simple.py` (9.3KB) - 简化版
   - `quick_samples.py` (5.6KB) - 快速版
   - `generate_correct_samples.py` (12KB) - 正确样例版
   - **建议**：保留前端统一脚本，其他作为模块

## 整理后的目标结构

```
FER/
├── README.md                          # 主文档（精简）
├── requirements.txt                   # 依赖
├── COMMANDS.txt                       # 命令速查（合并 COPY_PASTE_COMMANDS.txt）
│
├── src/                              # 核心代码
│   ├── train.py
│   ├── eval.py
│   ├── inference.py
│   ├── model.py
│   ├── model_legacy.py
│   ├── dataset.py
│   └── visualize.py
│
├── tools/                            # 工具脚本（新建）
│   ├── demo_visualization.py        # 可视化演示
│   ├── generate_samples.py          # 样例生成（统一入口）
│   ├── diagnose.py                  # 诊断工具（合并）
│   └── legacy/                      # 废弃脚本
│       ├── fix_visualization.py
│       ├── test_fix.py
│       └── diagnose_model.py
│
├── scripts/                          # 自动化脚本
│   ├── run_train.bat               # Windows 训练
│   ├── quick_test.bat              # 快速测试
│   ├── generate_samples.bat        # 样例生成
│   ├── wsl2_setup.sh               # WSL2 配置
│   └── ...
│
├── docs/                             # 文档目录（重组）
│   ├── README.md                    # 文档索引
│   ├── getting-started/             # 入门指南
│   │   ├── quickstart.md
│   │   ├── setup.md
│   │   └── commands.md             # 命令参考（合并）
│   ├── guides/                      # 使用指南
│   │   ├── training.md             # 训练指南
│   │   ├── visualization.md        # 可视化指南（合并）
│   │   ├── optimization.md
│   │   └── model_compatibility.md
│   ├── samples/                     # 样例生成（新建）
│   │   ├── README.md               # 主说明（合并多个）
│   │   ├── quickstart.md           # 快速入门
│   │   ├── examples.md             # 示例
│   │   ├── correct-samples.md      # 正确样例
│   │   └── troubleshooting.md      # 故障排除
│   ├── troubleshooting/             # 故障排除（新建）
│   │   ├── README.md               # 总索引
│   │   ├── general.md              # 通用问题
│   │   ├── training.md             # 训练问题
│   │   ├── visualization.md        # 可视化问题
│   │   └── samples.md              # 样例生成问题
│   └── reference/                   # 参考文档
│       ├── changelog.md
│       └── architecture.md
│
├── data/                             # 数据目录
├── checkpoints/                      # 模型检查点
├── output/                          # 输出目录
└── examples/                        # 示例代码
```

## 执行步骤

### 阶段 1：清理和归档
1. 删除明显冗余的文件
2. 将临时/修复脚本移到 legacy
3. 备份重要文件

### 阶段 2：创建新结构
1. 创建 `tools/` 目录
2. 创建 `docs/` 子目录结构
3. 移动和重命名文件

### 阶段 3：合并文档
1. 合并快速修复文档
2. 合并样例生成文档
3. 整合故障排除文档

### 阶段 4：更新引用
1. 更新主 README
2. 更新文档内链接
3. 更新脚本中的路径

### 阶段 5：验证和测试
1. 检查所有链接
2. 测试关键脚本
3. 更新 .gitignore

## 优先级

### 高优先级（立即执行）
- [x] 创建整理计划
- [ ] 创建新目录结构
- [ ] 移动脚本到 tools/
- [ ] 合并样例生成文档
- [ ] 更新主 README

### 中优先级
- [ ] 合并诊断脚本
- [ ] 整合故障排除文档
- [ ] 创建文档索引

### 低优先级
- [ ] 归档旧文件
- [ ] 优化脚本代码
- [ ] 添加更多示例
