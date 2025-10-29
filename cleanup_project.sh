#!/bin/bash
# FER2013 项目自动清理脚本
# 执行前请先备份重要文件！

set -e  # 遇到错误就停止

echo "============================================================"
echo "FER2013 项目清理工具"
echo "============================================================"
echo ""
echo "此脚本将："
echo "  1. 整理文档到 docs/ 目录"
echo "  2. 移动脚本到 scripts/ 目录"
echo "  3. 备份重要模型文件"
echo "  4. 清理临时文件"
echo ""
echo "⚠️  警告：此操作会移动/删除文件"
echo "⚠️  建议先运行 'git status' 或手动备份"
echo ""
read -p "继续? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 1
fi

echo ""
echo "开始清理..."
echo ""

# ============================================================
# 1. 创建目录结构
# ============================================================
echo "[1/6] 创建新目录结构..."

mkdir -p docs/guides
mkdir -p docs/reference
mkdir -p docs/archive
mkdir -p models/working
mkdir -p models/archive
mkdir -p scripts/training
mkdir -p scripts/setup

echo "  ✓ 目录结构创建完成"

# ============================================================
# 2. 整理文档
# ============================================================
echo ""
echo "[2/6] 整理文档..."

# 移动指南类文档到 docs/guides/
[ -f "TRAINING_GUIDE_50_EPOCHS.md" ] && mv TRAINING_GUIDE_50_EPOCHS.md docs/guides/training_guide.md && echo "  ✓ 训练指南"
[ -f "MODEL_SAVE_FIX.md" ] && mv MODEL_SAVE_FIX.md docs/guides/model_save_fix.md && echo "  ✓ 模型修复说明"
[ -f "CHECKPOINT_EXPLANATION.md" ] && mv CHECKPOINT_EXPLANATION.md docs/guides/checkpoint_guide.md && echo "  ✓ Checkpoint指南"
[ -f "COMPLETE_WORKFLOW.md" ] && mv COMPLETE_WORKFLOW.md docs/guides/complete_workflow.md && echo "  ✓ 完整工作流程"

# 移动参考类文档到 docs/reference/
[ -f "QUICK_COMMANDS.txt" ] && mv QUICK_COMMANDS.txt docs/reference/quick_commands.txt && echo "  ✓ 快速命令"
[ -f "COMMANDS.txt" ] && mv COMMANDS.txt docs/reference/commands_old.txt && echo "  ✓ 旧命令（已标记）"

# 移动过时文档到 docs/archive/
[ -f "PROJECT_STRUCTURE.md" ] && mv PROJECT_STRUCTURE.md docs/archive/ && echo "  ✓ 归档：项目结构"
[ -f "PROJECT_CLEANUP_PLAN.md" ] && mv PROJECT_CLEANUP_PLAN.md docs/archive/ && echo "  ✓ 归档：清理计划"
[ -f "PROJECT_REORGANIZATION_COMPLETE.md" ] && mv PROJECT_REORGANIZATION_COMPLETE.md docs/archive/ && echo "  ✓ 归档：重组完成"
[ -f "CLEANUP_SUMMARY.md" ] && mv CLEANUP_SUMMARY.md docs/archive/ && echo "  ✓ 归档：清理总结"
[ -f "PROJECT_CLEANUP_REPORT.md" ] && mv PROJECT_CLEANUP_REPORT.md docs/archive/ && echo "  ✓ 归档：清理报告"

echo "  ✓ 文档整理完成"

# ============================================================
# 3. 整理脚本
# ============================================================
echo ""
echo "[3/6] 整理脚本..."

# 转换所有shell脚本为Unix格式（避免Windows换行符问题）
echo "  转换脚本行尾符..."
find scripts/ -name "*.sh" -type f -exec dos2unix {} \; 2>/dev/null || true

# 移动训练脚本
[ -f "train_50_epochs.sh" ] && mv train_50_epochs.sh scripts/training/ && echo "  ✓ 训练脚本 (Linux)"
[ -f "train_50_epochs.bat" ] && mv train_50_epochs.bat scripts/training/ && echo "  ✓ 训练脚本 (Windows)"
[ -f "train_gpu.sh" ] && mv train_gpu.sh scripts/training/train_gpu.sh && echo "  ✓ GPU训练脚本"

# 转换新移动的脚本
find scripts/training/ -name "*.sh" -type f -exec dos2unix {} \; 2>/dev/null || true

echo "  ✓ 脚本整理完成"

# ============================================================
# 4. 备份模型
# ============================================================
echo ""
echo "[4/6] 备份重要模型..."

# 备份可用的旧模型
if [ -f "checkpoints/fer-5_449.ckpt" ]; then
    cp checkpoints/fer-5_449.ckpt models/working/model_v1_old.ckpt
    echo "  ✓ 旧模型 (1.3MB): models/working/model_v1_old.ckpt"
fi

# 备份新训练的最佳模型（虽然很大）
if [ -f "checkpoints_50epoch/best_model.ckpt" ]; then
    cp checkpoints_50epoch/best_model.ckpt models/working/model_v2_new.ckpt
    SIZE=$(du -h "checkpoints_50epoch/best_model.ckpt" | cut -f1)
    echo "  ✓ 新模型 ($SIZE): models/working/model_v2_new.ckpt"
    echo "    ⚠️  注意：新模型文件很大 ($SIZE)"
fi

echo "  ✓ 模型备份完成"

# ============================================================
# 5. 清理Python缓存
# ============================================================
echo ""
echo "[5/6] 清理Python缓存..."

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "  ✓ Python缓存清理完成"

# ============================================================
# 6. 创建便捷链接
# ============================================================
echo ""
echo "[6/6] 创建便捷链接..."

# 在根目录创建快捷训练脚本的软链接
[ -f "scripts/training/train_gpu.sh" ] && ln -sf scripts/training/train_gpu.sh train.sh && echo "  ✓ train.sh -> scripts/training/train_gpu.sh"

echo "  ✓ 便捷链接创建完成"

# ============================================================
# 完成
# ============================================================
echo ""
echo "============================================================"
echo "清理完成！"
echo "============================================================"
echo ""
echo "📁 新的目录结构："
echo ""
echo "  docs/"
echo "    ├── guides/          - 使用指南"
echo "    ├── reference/       - 参考文档"
echo "    └── archive/         - 历史文档"
echo ""
echo "  models/"
echo "    └── working/         - 可用模型"
echo ""
echo "  scripts/"
echo "    ├── training/        - 训练脚本"
echo "    └── setup/           - 环境配置脚本"
echo ""
echo "📝 下一步："
echo ""
echo "  1. 验证模型："
echo "     python verify_model.py --ckpt models/working/model_v2_new.ckpt"
echo ""
echo "  2. 生成样例："
echo "     python tools/generate_correct_samples.py \\"
echo "       --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \\"
echo "       --ckpt models/working/model_v2_new.ckpt \\"
echo "       --device GPU --num_samples 3"
echo ""
echo "  3. 查看文档："
echo "     cat START_HERE.md"
echo ""
echo "⚠️  注意："
echo "  - 原始 checkpoints/ 目录保留未动"
echo "  - 如果一切正常，可以手动删除旧的 checkpoints/ 目录"
echo "  - 建议先测试模型再删除任何文件"
echo ""
