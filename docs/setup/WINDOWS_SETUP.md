# Windows 环境快速配置指南

## 当前问题

你遇到的错误：
```
conda : 无法将"conda"项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

**原因**：PowerShell 中 conda 没有正确初始化。

## ✅ 快速解决方案

### 方案 1：使用 Anaconda Prompt（推荐 - 最简单）

1. **打开 Anaconda Prompt**
   - 按 `Win` 键
   - 搜索 "Anaconda Prompt"
   - 打开它

2. **进入项目目录**
   ```bash
   cd /d E:\Users\Meng\Projects\VScodeProjects\FER
   ```

3. **激活环境**
   ```bash
   conda activate fer
   ```

4. **运行摄像头功能**
   ```bash
   # 一键启动
   run_webcam.bat

   # 或手动运行
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
   ```

---

### 方案 2：在 PowerShell 中初始化 Conda

如果你想在 PowerShell 中使用 conda：

1. **查找 conda 安装路径**

   通常在：
   - `C:\Users\Meng\anaconda3`
   - `C:\Users\Meng\miniconda3`
   - `C:\ProgramData\Anaconda3`

2. **初始化 conda**

   在 PowerShell 中运行（替换为你的 Anaconda 路径）：

   ```powershell
   # 假设 Anaconda 安装在默认位置
   & "C:\Users\Meng\anaconda3\Scripts\conda.exe" init powershell
   ```

   或者尝试：
   ```powershell
   & "C:\Users\Meng\miniconda3\Scripts\conda.exe" init powershell
   ```

3. **重新打开 PowerShell**

4. **激活环境并运行**
   ```powershell
   conda activate fer
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
   ```

---

### 方案 3：直接使用 Python（无需 conda）

如果 Python 已经安装并在 PATH 中：

1. **检查 Python**
   ```powershell
   python --version
   ```

2. **检查依赖**
   ```powershell
   python -c "import cv2, mindspore; print('依赖已安装')"
   ```

   如果提示缺少模块，安装它们：
   ```powershell
   pip install opencv-python mindspore numpy matplotlib
   ```

3. **直接运行**
   ```powershell
   # 测试摄像头
   python test_camera.py

   # 运行实时识别
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
   ```

---

### 方案 4：使用完整的 Python 路径

如果你知道 conda 环境中 Python 的完整路径：

```powershell
# 使用完整路径（示例）
C:\Users\Meng\anaconda3\envs\fer\python.exe tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

查找 Python 路径：
```powershell
# 在 Anaconda Prompt 中运行
conda activate fer
where python
```

---

## 🎯 推荐流程

### 选项 A：使用 Anaconda Prompt（最简单）

```bash
# 1. 打开 Anaconda Prompt

# 2. 进入项目目录
cd /d E:\Users\Meng\Projects\VScodeProjects\FER

# 3. 激活环境
conda activate fer

# 4. 运行
run_webcam.bat
```

### 选项 B：修改启动脚本（自动激活环境）

创建一个新的启动脚本 `run_webcam_conda.bat`：

```batch
@echo off
REM 自动激活 conda 环境并运行摄像头功能

echo ========================================
echo FER2013 实时摄像头表情识别
echo ========================================
echo.

REM 设置 Anaconda 路径（根据你的安装位置修改）
set ANACONDA_PATH=C:\Users\Meng\anaconda3

REM 初始化 conda
call "%ANACONDA_PATH%\Scripts\activate.bat" "%ANACONDA_PATH%"

REM 激活 fer 环境
call conda activate fer

REM 检查模型文件
if exist "checkpoints_50epoch\best_model.ckpt" (
    set CKPT_PATH=checkpoints_50epoch\best_model.ckpt
) else if exist "checkpoints\best_model.ckpt" (
    set CKPT_PATH=checkpoints\best_model.ckpt
) else (
    echo [ERROR] 未找到模型文件！
    pause
    exit /b 1
)

echo 使用模型: %CKPT_PATH%
echo.

REM 运行摄像头识别
python tools\demo_visualization.py --mode webcam --ckpt %CKPT_PATH% --device CPU

pause
```

使用方法：
1. 修改脚本中的 `ANACONDA_PATH` 为你的 Anaconda 安装路径
2. 双击运行 `run_webcam_conda.bat`

---

## 🔍 查找 Conda 安装位置

### 方法 1：搜索文件

在文件资源管理器中搜索：
```
conda.exe
```

常见位置：
- `C:\Users\Meng\anaconda3\Scripts\conda.exe`
- `C:\Users\Meng\miniconda3\Scripts\conda.exe`
- `C:\ProgramData\Anaconda3\Scripts\conda.exe`

### 方法 2：查看环境变量

1. 按 `Win + R`
2. 输入 `sysdm.cpl`
3. 点击 "高级" → "环境变量"
4. 查看 PATH 中是否有 Anaconda 相关路径

---

## 📝 快速测试步骤

### 步骤 1：打开 Anaconda Prompt

搜索并打开 "Anaconda Prompt"

### 步骤 2：运行测试命令

```bash
# 进入项目目录
cd /d E:\Users\Meng\Projects\VScodeProjects\FER

# 激活环境
conda activate fer

# 测试 Python
python --version

# 测试依赖
python -c "import cv2, mindspore; print('OK')"

# 测试摄像头
python test_camera.py

# 运行实时识别
python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
```

---

## ⚠️ 常见问题

### Q1: 找不到 Anaconda Prompt

**解决**：
- 确认是否安装了 Anaconda/Miniconda
- 如果没有，从这里下载：https://www.anaconda.com/download
- 或使用普通 Python：从 python.org 下载

### Q2: conda activate 不工作

**解决**：
```bash
# 使用完整命令
conda activate fer

# 或使用
activate fer

# 或在 PowerShell 中
conda init powershell
```

### Q3: 缺少依赖包

**解决**：
```bash
conda activate fer
pip install opencv-python mindspore numpy matplotlib
```

---

## 🎉 成功标志

当你看到类似这样的输出，说明成功了：

```
============================================================
演示：实时摄像头表情识别
============================================================
按 'q' 退出，按 's' 保存当前帧

[INFO] Loading model from checkpoints_50epoch/best_model.ckpt
[INFO] Detected classifier shape: (256, 512)
[INFO] Loading current model (512 -> 256 -> 128 -> 7)
[INFO] Visualizer initialized. Output: output/webcam
[INFO] Starting webcam 0. Press 'q' to quit, 's' to save frame
```

然后会打开一个窗口显示摄像头画面和实时表情识别结果。

---

## 📞 需要帮助？

如果以上方法都不行：

1. **检查 Python 是否安装**：
   ```powershell
   python --version
   ```

2. **查看项目依赖**：
   ```powershell
   type requirements.txt
   ```

3. **查看详细文档**：
   - [WEBCAM_GUIDE.md](WEBCAM_GUIDE.md)
   - [QUICK_FIX_WSL_WEBCAM.md](QUICK_FIX_WSL_WEBCAM.md)

---

## 📋 总结

**最简单的方法**：

1. 打开 **Anaconda Prompt**（不是 PowerShell）
2. 运行：
   ```bash
   cd /d E:\Users\Meng\Projects\VScodeProjects\FER
   conda activate fer
   python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
   ```

就这么简单！🎉
