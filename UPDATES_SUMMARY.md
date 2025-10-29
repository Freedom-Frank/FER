# 更新总结 - 摄像头功能与模型路径配置

## 📅 更新日期
2025年1月29日

## 🎯 更新内容

### 1. 模型路径自动识别

所有启动脚本现在会按以下优先级自动查找模型：

1. ⭐ `checkpoints_50epoch/best_model.ckpt` - **优先使用**（131MB，50轮训练）
2. `checkpoints/best_model.ckpt` - 备用模型
3. `checkpoints_50epoch/fer-50_299.ckpt` - 其他50轮检查点
4. `checkpoints/fer-5_449.ckpt` - 早期检查点

### 2. 更新的文件

#### 启动脚本
- ✅ [run_webcam.bat](run_webcam.bat) - Windows启动脚本
- ✅ [run_webcam.sh](run_webcam.sh) - Linux/WSL启动脚本

**改进**：
- 自动检测 `checkpoints_50epoch` 目录
- 智能选择最佳模型
- 提供详细的错误提示

#### 文档更新
- ✅ [README.md](README.md) - 主文档
  - 添加了实时摄像头快速开始部分
  - 更新了项目结构，包含 `checkpoints_50epoch` 目录
  - 更新了模型路径示例

- ✅ [WEBCAM_QUICKREF.txt](WEBCAM_QUICKREF.txt) - 快速参考
  - 更新了命令示例，使用 `checkpoints_50epoch` 路径

- ✅ [MODEL_INFO.md](MODEL_INFO.md) - **新建**
  - 详细的模型文件说明
  - 模型性能对比
  - 使用建议

#### 测试工具
- ✅ [test_model.py](test_model.py) - **新建**
  - 自动查找最佳模型
  - 测试模型加载
  - 测试推理功能
  - 显示模型信息

### 3. 新功能

#### 一键启动（自动查找模型）

**Windows**:
```bash
# 双击或命令行运行
run_webcam.bat
```

**Linux/WSL**:
```bash
bash run_webcam.sh
```

脚本会自动：
1. 查找可用的模型文件
2. 优先使用 `checkpoints_50epoch/best_model.ckpt`
3. 自动检测GPU并选择合适的设备
4. 显示详细的运行信息

#### 模型测试工具

**自动测试**（自动查找模型）:
```bash
python test_model.py
```

**指定模型测试**:
```bash
python test_model.py --ckpt checkpoints_50epoch/best_model.ckpt
```

**GPU测试**:
```bash
python test_model.py --device GPU
```

功能：
- ✓ 验证模型文件存在性
- ✓ 显示文件大小
- ✓ 检测模型版本（新版/旧版）
- ✓ 测试模型加载
- ✓ 测试推理功能
- ✓ 显示测试输出

### 4. 目录结构

你的项目现在有两个模型目录：

```
FER/
├── checkpoints_50epoch/           ⭐ 推荐使用
│   ├── best_model.ckpt           (131MB) - 最佳模型
│   ├── final_model.ckpt          (44MB)  - 最终模型
│   └── fer-*.ckpt                - 各epoch检查点
│
└── checkpoints/                   备用
    ├── best_model.ckpt
    └── fer-*.ckpt
```

## 📖 使用指南

### 快速开始

1. **启动实时摄像头**（最简单）:
   ```bash
   # Windows
   run_webcam.bat

   # Linux/WSL
   bash run_webcam.sh
   ```

2. **测试模型**:
   ```bash
   python test_model.py
   ```

3. **测试摄像头**:
   ```bash
   python test_camera.py
   ```

### 手动指定模型

如果你想使用特定的模型：

```bash
# 使用50轮训练的最佳模型（推荐）
python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt

# 使用GPU加速
python tools/demo_visualization.py --mode webcam --ckpt checkpoints_50epoch/best_model.ckpt --device GPU

# 使用其他模型
python tools/demo_visualization.py --mode webcam --ckpt checkpoints/best_model.ckpt
```

### 处理图片

```bash
# 单张图片
python tools/demo_visualization.py --mode image --ckpt checkpoints_50epoch/best_model.ckpt --input test.jpg

# 批量处理
python tools/demo_visualization.py --mode batch --ckpt checkpoints_50epoch/best_model.ckpt --input test_images/
```

### 评估模型

```bash
# 标准评估
python src/eval.py \
  --data_csv data/FER2013/fer2013.csv \
  --ckpt_path checkpoints_50epoch/best_model.ckpt \
  --device_target GPU

# CSV批量评估（无漏检）
python src/batch_eval_csv.py \
  --csv data/FER2013/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

## 🎨 功能亮点

### 1. 智能模型选择

启动脚本会智能选择最佳模型：
- ✓ 优先使用50轮训练的模型（更高准确率）
- ✓ 自动降级到备用模型
- ✓ 提供清晰的错误提示

### 2. 完整的测试工具

新增的测试工具帮助你：
- ✓ 验证模型是否可用
- ✓ 检查模型版本
- ✓ 测试推理功能
- ✓ 快速诊断问题

### 3. 详细的文档

新建的 [MODEL_INFO.md](MODEL_INFO.md) 包含：
- ✓ 模型目录结构说明
- ✓ 推荐使用的模型
- ✓ 模型性能对比
- ✓ 使用方法和示例
- ✓ 常见问题解答

## 📚 文档导航

### 摄像头功能
- [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md) - 完整使用指南
- [WEBCAM_QUICKREF.txt](WEBCAM_QUICKREF.txt) - 快速参考
- [WEBCAM_DEMO.txt](WEBCAM_DEMO.txt) - 界面演示
- [WEBCAM_IMPLEMENTATION_SUMMARY.md](WEBCAM_IMPLEMENTATION_SUMMARY.md) - 实现总结

### 模型相关
- [MODEL_INFO.md](MODEL_INFO.md) - 模型文件说明 ⭐ 新建
- [docs/model_compatibility.md](docs/model_compatibility.md) - 模型兼容性

### 主文档
- [README.md](README.md) - 项目主文档
- [START_HERE.md](START_HERE.md) - 5分钟快速上手
- [docs/README.md](docs/README.md) - 文档中心

## 🔧 测试清单

在使用之前，建议运行以下测试：

```bash
# 1. 测试模型加载
python test_model.py

# 2. 测试摄像头
python test_camera.py

# 3. 测试实时识别
run_webcam.bat  # Windows
bash run_webcam.sh  # Linux
```

## ⚠️ 注意事项

1. **模型优先级**:
   - 系统优先使用 `checkpoints_50epoch/best_model.ckpt`
   - 这个模型经过50轮训练，性能最好
   - 文件大小为 131MB

2. **GPU加速**:
   - 启动脚本在Linux/WSL上会自动检测GPU
   - Windows用户需要手动指定 `--device GPU`（如果有GPU）

3. **摄像头权限**:
   - Windows：确保程序有摄像头访问权限
   - Linux：可能需要用户组权限
   - WSL：需要配置USB摄像头直通

## 🎉 完成状态

- ✅ 摄像头功能文档化
- ✅ 启动脚本支持自动模型查找
- ✅ 添加模型测试工具
- ✅ 创建完整的使用文档
- ✅ 更新主README
- ✅ 创建快速参考卡片

## 🚀 下一步

现在你可以：

1. **立即使用**:
   ```bash
   run_webcam.bat  # Windows
   bash run_webcam.sh  # Linux
   ```

2. **测试模型**:
   ```bash
   python test_model.py
   ```

3. **查看文档**:
   - 摄像头使用: [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md)
   - 模型说明: [MODEL_INFO.md](MODEL_INFO.md)
   - 快速参考: [WEBCAM_QUICKREF.txt](WEBCAM_QUICKREF.txt)

## 📞 获取帮助

如果遇到问题：

1. 查看 [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md) 的常见问题部分
2. 运行 `python test_model.py` 诊断模型问题
3. 运行 `python test_camera.py` 诊断摄像头问题
4. 查看 [docs/troubleshooting.md](docs/troubleshooting.md)

祝使用愉快！ 🎉
