@echo off
REM 快速启动实时摄像头表情识别
REM 使用方法：双击此文件或在命令行运行 run_webcam.bat

echo ========================================
echo FER2013 实时摄像头表情识别
echo ========================================
echo.
echo 功能说明：
echo   - 实时检测人脸并识别表情
echo   - 按 'q' 键退出
echo   - 按 's' 键保存当前帧
echo.
echo 正在启动摄像头...
echo.

REM 检查模型文件是否存在（按优先级顺序）
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
    echo 请先训练模型或确保以下文件存在：
    echo   - checkpoints_50epoch\best_model.ckpt
    echo   - checkpoints_50epoch\fer-50_449.ckpt
    echo   - checkpoints\best_model.ckpt
    echo   - checkpoints\fer-5_449.ckpt
    pause
    exit /b 1
)

echo 使用模型: %CKPT_PATH%
echo.

REM 运行摄像头识别（CPU模式）
python tools\demo_visualization.py --mode webcam --ckpt %CKPT_PATH% --device CPU

if errorlevel 1 (
    echo.
    echo [ERROR] 运行失败！可能的原因：
    echo   1. 摄像头未连接或被占用
    echo   2. 缺少依赖库（需要 opencv-python）
    echo   3. Python环境问题
    echo.
    echo 解决方法：
    echo   1. 确保摄像头已连接并正常工作
    echo   2. 运行: pip install opencv-python
    echo   3. 检查Python环境是否正确配置
)

pause
