@echo off
REM 生成 FER2013 样例展示的快速脚本

echo ============================================================
echo FER2013 样例生成脚本
echo ============================================================
echo.

REM 设置默认参数
set CSV_PATH=data\FER2013\fer2013.csv
set CKPT_PATH=checkpoints\best_model.ckpt
set OUTPUT_DIR=samples_output
set DEVICE=CPU
set NUM_SAMPLES=3

REM 检查数据集
if not exist "%CSV_PATH%" (
    echo [ERROR] 数据集文件不存在: %CSV_PATH%
    echo 请先下载 FER2013 数据集
    pause
    exit /b 1
)

REM 检查模型
if not exist "%CKPT_PATH%" (
    echo [WARNING] best_model.ckpt 不存在，尝试使用其他模型...
    if exist "checkpoints\fer-5_449.ckpt" (
        set CKPT_PATH=checkpoints\fer-5_449.ckpt
        echo [INFO] 使用模型: %CKPT_PATH%
    ) else (
        echo [ERROR] 未找到可用的模型文件
        echo 请先训练模型或下载预训练模型
        pause
        exit /b 1
    )
)

echo [INFO] 配置信息:
echo   数据集: %CSV_PATH%
echo   模型: %CKPT_PATH%
echo   输出目录: %OUTPUT_DIR%
echo   设备: %DEVICE%
echo   每种表情样例数: %NUM_SAMPLES%
echo.

REM 运行样例生成脚本
python generate_samples.py ^
    --csv "%CSV_PATH%" ^
    --ckpt "%CKPT_PATH%" ^
    --output "%OUTPUT_DIR%" ^
    --device %DEVICE% ^
    --num_samples %NUM_SAMPLES%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo 样例生成成功！
    echo ============================================================
    echo 查看结果:
    echo   详细样例: %OUTPUT_DIR%\^<emotion^>\sample_*.png
    echo   网格展示: %OUTPUT_DIR%\all_samples_grid.png
    echo   对比表: %OUTPUT_DIR%\emotion_comparison_sheet.png
    echo.
) else (
    echo.
    echo [ERROR] 样例生成失败
)

pause
