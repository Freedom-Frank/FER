# 项目结构整理方案

## 当前问题

根目录过于混乱，包含：
- 16 个 Markdown 文档
- 7 个 TXT 文件
- 5 个 Python 测试脚本
- 3 个 BAT 启动脚本
- 2 个 SH 脚本
- 一些临时文件和日志

## 整理方案

### 1. 文档分类整理

**保留在根目录**（最重要的入口文档）：
- `README.md` - 项目主文档
- `START_HERE.md` - 快速开始指南

**移动到 `docs/` 目录**：

#### docs/guides/ （使用指南）
- `WEBCAM_GUIDE.md` - 摄像头使用完整指南
- `QUICK_START_BATCH.md` - 批处理快速开始
- `QUICK_START_CSV_BATCH.md` - CSV批处理指南
- `NAVIGATION.md` - 文档导航

#### docs/setup/ （环境配置）
- `WINDOWS_SETUP.md` - Windows 配置指南
- `WSL_WEBCAM_SETUP.md` - WSL 摄像头配置

#### docs/troubleshooting/ （问题修复）
- `FIX_PIL_ERROR.md` - PIL 错误修复
- `OPENCV_FIX.md` - OpenCV 错误修复
- `QUICK_FIX_WSL_WEBCAM.md` - WSL 快速修复
- `QUICK_FIX_NOW.txt` - 快速修复命令

#### docs/reference/ （参考资料）
- `MODEL_INFO.md` - 模型信息
- `WEBCAM_IMPLEMENTATION_SUMMARY.md` - 实现细节
- `UPDATES_SUMMARY.md` - 更新摘要
- `DOCUMENTATION_COMPLETE.md` - 文档完成状态

#### docs/quickref/ （快速参考）
- `START_HERE.txt` - 纯文本快速开始
- `START_WEBCAM_WINDOWS.txt` - Windows 摄像头启动
- `WEBCAM_QUICKREF.txt` - 摄像头快速参考
- `WEBCAM_DEMO.txt` - 摄像头演示说明
- `READY_TO_RUN.md` - 准备运行指南
- `FINAL_STATUS.txt` - 最终状态报告

### 2. 脚本整理

**创建 `scripts/` 子目录**：

#### scripts/webcam/ （摄像头相关）
- `run_webcam.bat` - Windows 摄像头启动
- `run_webcam.sh` - Linux 摄像头启动
- `run_webcam_conda.bat` - Conda 环境自动启动

#### scripts/utils/ （工具脚本）
- `fix_and_run.bat` - 修复并启动
- `cleanup_project.sh` - 项目清理

#### scripts/tests/ （测试脚本）
- `test_camera.py` - 摄像头测试
- `test_model.py` - 模型测试
- `test_cascade.py` - Cascade 测试
- `diagnose.py` - 综合诊断
- `verify_model.py` - 模型验证

### 3. 临时文件清理

**删除以下文件**：
- `nul` - Windows 空文件
- `generate_output.log` - 旧日志文件
- `__pycache__/` - Python 缓存目录

### 4. 整理后的目录结构

```
FER/
├── README.md                    # 主文档
├── START_HERE.md               # 快速开始
├── requirements.txt            # 依赖
│
├── src/                        # 源代码
├── tools/                      # 工具脚本（原有）
│
├── scripts/                    # 启动和工具脚本
│   ├── webcam/                # 摄像头启动脚本
│   ├── utils/                 # 实用工具
│   └── tests/                 # 测试脚本
│
├── docs/                       # 文档
│   ├── guides/                # 使用指南
│   ├── setup/                 # 环境配置
│   ├── troubleshooting/       # 问题修复
│   ├── reference/             # 参考资料
│   ├── quickref/              # 快速参考
│   ├── model_compatibility.md # 已有文档
│   ├── setup.md               # 已有文档
│   └── ...                    # 其他已有文档
│
├── checkpoints/               # 模型检查点
├── checkpoints_50epoch/       # 50轮训练模型
├── output/                    # 输出结果
├── test_images/               # 测试图片
├── correct_samples/           # 正确样本
├── samples_output/            # 样例输出
├── examples/                  # 示例
└── rank_0/                    # 训练日志
```

### 5. 文档内容更新

整理后需要更新以下文档中的路径引用：
- `README.md` - 更新所有文档链接
- `START_HERE.md` - 更新脚本路径
- 所有包含相对路径的文档

### 6. 创建便捷访问

在根目录保留或创建：
- `START_HERE.md` - 指向所有重要资源的入口
- README.md 在开头添加"快速导航"部分

## 执行顺序

1. 创建新的子目录结构
2. 移动文档文件
3. 移动脚本文件
4. 删除临时文件
5. 更新 README.md 中的链接
6. 更新其他文档中的路径引用
7. 测试所有脚本是否正常工作

## 注意事项

- 所有移动操作使用 git mv 确保保留历史
- 移动后需要测试脚本的相对路径导入
- 更新所有文档内的超链接
- 保持 .gitignore 正确排除临时文件
