@echo off
REM 修复 PIL 错误并运行摄像头功能

echo ========================================
echo 修复 PIL/Pillow 兼容性问题
echo ========================================
echo.

echo [INFO] 正在修复 Pillow 版本问题...
echo.

REM 降级 Pillow 到兼容版本
pip install Pillow==9.5.0

if errorlevel 1 (
    echo [ERROR] Pillow 安装失败
    echo 请手动运行: pip install Pillow==9.5.0
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Pillow 已降级到 9.5.0
echo.

REM 测试 MindSpore 是否可以正常导入
echo [INFO] 测试 MindSpore...
python -c "import mindspore; print('[SUCCESS] MindSpore 加载成功')"

if errorlevel 1 (
    echo [ERROR] MindSpore 仍有问题
    echo 查看详细修复指南: FIX_PIL_ERROR.md
    pause
    exit /b 1
)

echo.
echo [INFO] 所有依赖正常！
echo.

REM 检查模型文件
if exist "checkpoints_50epoch\best_model.ckpt" (
    set CKPT_PATH=checkpoints_50epoch\best_model.ckpt
) else if exist "checkpoints\best_model.ckpt" (
    set CKPT_PATH=checkpoints\best_model.ckpt
) else (
    echo [ERROR] 未找到模型文件
    pause
    exit /b 1
)

echo 使用模型: %CKPT_PATH%
echo.

REM 询问是否立即运行摄像头
echo ========================================
echo 准备启动实时摄像头表情识别
echo ========================================
echo.
echo 按任意键启动，或按 Ctrl+C 取消...
pause >nul

echo.
echo [INFO] 启动摄像头...
echo.

REM 运行摄像头功能
python tools\demo_visualization.py --mode webcam --ckpt %CKPT_PATH% --device CPU

pause
