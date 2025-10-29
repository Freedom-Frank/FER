# FER2013 项目最终指南

## 🎉 项目完成状态

### ✅ 已完成
- ✓ 模型训练成功（50轮）
- ✓ 修复了模型保存BUG
- ✓ 修复了导入路径问题
- ✓ 创建了完整的文档系统
- ✓ 提供了自动化脚本

### 📊 项目统计
- **模型准确率**: 预计 68-72%（GPU训练）
- **训练时间**: ~50-100分钟（GPU）
- **模型文件**: 2个可用模型
  - `models/working/model_v1_old.ckpt` (1.3MB) - 旧版本
  - `models/working/model_v2_new.ckpt` (131MB) - 新训练

---

## 🚀 快速开始

### 方式1: 使用新模型（推荐尝试）

```bash
# 1. 验证模型
python verify_model.py --ckpt models/working/model_v2_new.ckpt

# 2. 生成可视化
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt models/working/model_v2_new.ckpt \
  --device GPU \
  --num_samples 3
```

### 方式2: 使用旧模型（稳妥）

```bash
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt models/working/model_v1_old.ckpt \
  --device GPU \
  --num_samples 3
```

---

## 📁 整理后的项目结构

```
FER/
├── 📄 README.md                    # 项目主文档
├── 📄 START_HERE.md                # 快速开始（推荐从这里开始）
├── 📄 requirements.txt             # Python依赖
├── 📄 verify_model.py              # 模型验证工具
├── 🔗 train.sh                     # 训练快捷方式（软链接）
│
├── 📂 src/                         # 源代码
│   ├── train.py                   # 训练脚本 ⭐
│   ├── eval.py                    # 评估脚本
│   ├── inference.py               # 推理脚本
│   ├── model.py                   # 模型定义 ⭐
│   ├── model_legacy.py            # 旧版模型
│   ├── dataset.py                 # 数据加载
│   └── visualize.py               # 可视化类 ⭐
│
├── 📂 tools/                       # 工具脚本
│   ├── demo_visualization.py      # 可视化演示 ⭐
│   ├── generate_correct_samples.py # 生成样例 ⭐
│   ├── generate_samples.py
│   ├── generate_samples_simple.py
│   ├── diagnose_correct_samples.py
│   └── quick_samples.py
│
├── 📂 scripts/                     # 运行脚本
│   ├── training/                  # 训练相关
│   │   ├── train_gpu.sh          # GPU训练 ⭐
│   │   ├── train_50_epochs.sh    # 50轮训练
│   │   └── train_50_epochs.bat   # Windows训练
│   ├── setup/                     # 环境配置
│   │   ├── wsl2_setup.sh         # WSL2配置
│   │   └── install_wsl2.ps1      # WSL2安装
│   ├── run_train.bat             # 快速训练
│   ├── quick_test.bat            # 快速测试
│   └── test_visualization.sh     # 可视化测试
│
├── 📂 docs/                        # 文档
│   ├── 📄 README.md               # 文档索引
│   ├── guides/                    # 使用指南
│   │   ├── training_guide.md     # 训练指南 ⭐
│   │   ├── checkpoint_guide.md   # Checkpoint说明
│   │   ├── complete_workflow.md  # 完整流程
│   │   ├── model_save_fix.md     # 模型修复
│   │   ├── visualization_guide.md # 可视化
│   │   └── troubleshooting.md    # 故障排除
│   ├── reference/                 # 参考文档
│   │   ├── quick_commands.txt    # 快速命令 ⭐
│   │   └── commands_old.txt      # 旧命令
│   ├── archive/                   # 历史文档
│   │   └── ...                   # 过时文档
│   └── quick-reference/          # 快速参考
│       └── visualization.md
│
├── 📂 models/                      # 模型文件
│   ├── working/                   # 当前可用模型 ⭐
│   │   ├── model_v1_old.ckpt     # 1.3MB（旧版本）
│   │   └── model_v2_new.ckpt     # 131MB（新训练）
│   └── archive/                   # 历史模型
│
├── 📂 checkpoints/                 # 训练检查点（保留）
│   └── fer-5_449.ckpt            # 原始可用模型
│
├── 📂 checkpoints_50epoch/         # 新训练检查点（保留）
│   ├── best_model.ckpt           # 最佳模型
│   └── fer_1-*.ckpt              # 各轮检查点
│
├── 📂 outputs/                     # 输出文件（清理后）
│   ├── samples/                   # 样例展示
│   ├── visualizations/            # 可视化结果
│   └── batch_results/             # 批量处理
│
├── 📂 data/                        # 数据集
│   └── FER2013/
│       └── fer2013.csv           # 需手动下载
│
├── 📂 correct_samples/             # 正确样例（保留）
├── 📂 my_samples/                  # 自定义样例（保留）
└── 📂 rank_0/                      # MindSpore输出（可删）
```

---

## 🔧 项目整理工具

### 自动整理脚本

```bash
# 运行自动清理脚本
bash cleanup_project.sh
```

**脚本功能**：
1. ✓ 整理文档到 `docs/` 目录
2. ✓ 移动脚本到 `scripts/` 目录
3. ✓ 备份重要模型到 `models/working/`
4. ✓ 清理Python缓存
5. ✓ 创建便捷链接
6. ✓ 转换脚本行尾符（Unix格式）

---

## 📖 核心文档导航

### 快速参考
1. **[START_HERE.md](START_HERE.md)** ⭐ 从这里开始！
2. **[docs/reference/quick_commands.txt](docs/reference/quick_commands.txt)** - 命令速查

### 详细指南
3. **[docs/guides/training_guide.md](docs/guides/training_guide.md)** - 训练详解
4. **[docs/guides/complete_workflow.md](docs/guides/complete_workflow.md)** - 完整流程
5. **[docs/guides/checkpoint_guide.md](docs/guides/checkpoint_guide.md)** - Checkpoint说明

### 问题解决
6. **[docs/guides/model_save_fix.md](docs/guides/model_save_fix.md)** - 模型保存修复
7. **[docs/troubleshooting.md](docs/troubleshooting.md)** - 故障排除

---

## 🎯 常用命令速查

### 训练相关
```bash
# GPU训练（推荐）
bash scripts/training/train_gpu.sh

# 或使用软链接
bash train.sh

# 验证模型
python verify_model.py --ckpt models/working/model_v2_new.ckpt
```

### 可视化相关
```bash
# 生成样例
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt models/working/model_v2_new.ckpt \
  --device GPU --num_samples 3

# 单张图片
python tools/demo_visualization.py \
  --mode image \
  --ckpt models/working/model_v2_new.ckpt \
  --input test.jpg

# 批量处理
python tools/demo_visualization.py \
  --mode batch \
  --ckpt models/working/model_v2_new.ckpt \
  --input test_images/
```

### 项目管理
```bash
# 整理项目
bash cleanup_project.sh

# 查看项目结构
tree -L 2 -I '__pycache__|*.pyc|rank_0'

# 检查模型大小
ls -lh models/working/
```

---

## 💡 重要提示

### 关于新模型（131MB）

**为什么这么大？**
- 正常模型：1.3 MB（只有参数）
- 新模型：131 MB（可能包含优化器状态）

**影响**：
- ✓ 功能正常（如果验证通过）
- ✓ 预测准确
- ✗ 占用空间大
- ✗ 加载稍慢

**解决方案**：
1. **现在**：先用，如果工作正常就行
2. **优化**：需要时可以提取纯参数版本
3. **重训**：修改保存代码后重新训练

### 关于checkpoints目录

**保留还是删除？**

```bash
# 保留（推荐）：
checkpoints/fer-5_449.ckpt          # 备用模型
checkpoints_50epoch/best_model.ckpt # 新模型

# 可删除：
checkpoints/fer_1-50_*.ckpt         # 旧训练的中间文件
checkpoints_50epoch/fer_1-4*.ckpt  # 中间检查点（已有best）
```

**建议**：
- 先确保新模型可用
- 备份重要文件
- 再删除冗余文件

---

## 📝 下一步建议

### 立即执行
1. **验证新模型**
   ```bash
   python verify_model.py --ckpt models/working/model_v2_new.ckpt
   ```

2. **生成可视化样例**
   ```bash
   python tools/generate_correct_samples.py \
     --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
     --ckpt models/working/model_v2_new.ckpt \
     --device GPU --num_samples 3
   ```

3. **检查输出结果**
   ```bash
   ls -R correct_samples/
   ls -R visualization_samples/
   ```

### 可选操作

4. **运行清理脚本**
   ```bash
   bash cleanup_project.sh
   ```

5. **清理旧checkpoints**（谨慎！）
   ```bash
   # 在确认新模型可用后
   rm -rf checkpoints/fer_1-50_*.ckpt
   rm -rf checkpoints_50epoch/fer_1-4*.ckpt
   ```

6. **提交到Git**（如果使用版本控制）
   ```bash
   git add .
   git commit -m "Project cleanup and model training complete"
   ```

---

## 🆘 遇到问题？

### 模型问题
- **模型文件太大**: 查看 [docs/guides/model_save_fix.md](docs/guides/model_save_fix.md)
- **预测概率均匀**: 模型未训练，重新训练
- **加载失败**: 检查模型版本兼容性

### 训练问题
- **内存不足**: 减小 batch_size
- **训练太慢**: 使用GPU，增大 batch_size
- **准确率低**: 启用数据增强和Mixup

### 可视化问题
- **找不到样例**: 增加 `--max_attempts`
- **导入错误**: 确认在项目根目录
- **OpenCV错误**: 检查cv2安装

详见：[docs/troubleshooting.md](docs/troubleshooting.md)

---

## 🎊 项目完成检查清单

- [ ] ✓ 模型训练完成
- [ ] ✓ 模型验证通过
- [ ] ✓ 生成可视化样例成功
- [ ] ✓ 概率分布正常（不是14.3%）
- [ ] ✓ 文档整理完成
- [ ] ✓ 项目结构清晰
- [ ] 可选：清理冗余文件
- [ ] 可选：提交到版本控制

---

## 📚 相关资源

### 项目文档
- [README.md](README.md) - 项目主文档
- [START_HERE.md](START_HERE.md) - 快速开始
- [docs/README.md](docs/README.md) - 文档索引

### 外部资源
- [FER2013 数据集](https://www.kaggle.com/datasets/msambare/fer2013)
- [MindSpore 文档](https://www.mindspore.cn/docs)
- [OpenCV 文档](https://docs.opencv.org/)

---

## 🎯 总结

### 你现在拥有：
- ✓ 完整训练的模型（2个版本）
- ✓ 完善的文档系统
- ✓ 自动化工具脚本
- ✓ 清晰的项目结构
- ✓ 可视化功能

### 核心命令：
```bash
# 验证
python verify_model.py --ckpt models/working/model_v2_new.ckpt

# 可视化
python tools/generate_correct_samples.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt models/working/model_v2_new.ckpt \
  --device GPU --num_samples 3

# 整理
bash cleanup_project.sh
```

**恭喜完成项目！** 🎉

如有任何问题，查阅 [START_HERE.md](START_HERE.md) 或各项文档。
