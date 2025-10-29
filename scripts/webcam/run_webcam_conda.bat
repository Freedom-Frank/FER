@echo off
REM FER2013 实时摄像头表情识别 - Conda 版本
REM 自动激活 conda 环境并运行

echo ========================================
echo FER2013 实时摄像头表情识别
echo ========================================
echo.
echo 功能说明：
echo   - 实时检测人脸并识别表情
echo   - 按 'q' 键退出
echo   - 按 's' 键保存当前帧
echo.
echo 正在启动...
echo.

REM 尝试查找 Anaconda/Miniconda 安装位置
set CONDA_FOUND=0

REM 常见的 Anaconda 安装路径
if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    set ANACONDA_PATH=%USERPROFILE%\anaconda3
    set CONDA_FOUND=1
    goto :activate
)

if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    set ANACONDA_PATH=%USERPROFILE%\miniconda3
    set CONDA_FOUND=1
    goto :activate
)

if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
    set ANACONDA_PATH=C:\ProgramData\Anaconda3
    set CONDA_FOUND=1
    goto :activate
)

if exist "C:\Anaconda3\Scripts\activate.bat" (
    set ANACONDA_PATH=C:\Anaconda3
    set CONDA_FOUND=1
    goto :activate
)

REM 如果没找到 conda，尝试直接使用 python
if %CONDA_FOUND%==0 (
    echo [WARNING] 未找到 Anaconda/Miniconda 安装
    echo [INFO] 尝试直接使用 Python...
    echo.
    goto :direct_python
)

:activate
REM 激活 conda 环境
echo [INFO] 找到 Anaconda: %ANACONDA_PATH%
call "%ANACONDA_PATH%\Scripts\activate.bat" "%ANACONDA_PATH%"
if errorlevel 1 (
    echo [ERROR] Conda 初始化失败
    goto :direct_python
)

call conda activate fer
if errorlevel 1 (
    echo [WARNING] 激活 fer 环境失败，使用 base 环境
)

echo [INFO] Conda 环境已激活
echo.
goto :check_model

:direct_python
REM 直接使用 Python（不使用 conda）
echo [INFO] 直接使用系统 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未找到！
    echo.
    echo 请执行以下操作之一：
    echo   1. 打开 Anaconda Prompt 并运行：
    echo      cd /d E:\Users\Meng\Projects\VScodeProjects\FER
    echo      conda activate fer
    echo      python tools\demo_visualization.py --mode webcam --ckpt checkpoints_50epoch\best_model.ckpt
    echo.
    echo   2. 安装 Python: https://www.python.org/downloads/
    echo.
    echo   3. 查看详细文档: WINDOWS_SETUP.md
    pause
    exit /b 1
)

:check_model
REM 检查模型文件
if exist "checkpoints_50epoch\best_model.ckpt" (
    set CKPT_PATH=checkpoints_50epoch\best_model.ckpt
) else if exist "checkpoints\best_model.ckpt" (
    set CKPT_PATH=checkpoints\best_model.ckpt
) else if exist "checkpoints_50epoch\fer-50_449.ckpt" (
    set CKPT_PATH=checkpoints_50epoch\fer-50_449.ckpt
) else if exist "checkpoints\fer-5_449.ckpt" (
    set CKPT_PATH=checkpoints\fer-5_449.ckpt
) else (
    echo [ERROR] 未找到模型文件！
    echo 请确保以下文件存在：
    echo   - checkpoints_50epoch\best_model.ckpt
    echo   - checkpoints\best_model.ckpt
    pause
    exit /b 1
)

echo 使用模型: %CKPT_PATH%
echo.

REM 运行摄像头识别（CPU 模式）
echo [INFO] 启动摄像头识别...
echo.
python tools\demo_visualization.py --mode webcam --ckpt %CKPT_PATH% --device CPU

if errorlevel 1 (
    echo.
    echo [ERROR] 运行失败！
    echo.
    echo 可能的原因：
    echo   1. 摄像头未连接或被占用
    echo   2. 缺少依赖库
    echo   3. 模型文件损坏
    echo.
    echo 解决方法：
    echo   1. 测试摄像头: python test_camera.py
    echo   2. 测试模型: python test_model.py
    echo   3. 安装依赖: pip install opencv-python mindspore
    echo   4. 查看文档: WINDOWS_SETUP.md
)

pause
