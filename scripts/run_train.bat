@echo off
REM 训练脚本 - 使用GPU

SET PYTHON_ENV=E:\Users\Meng\Enviroments\conda_envs\fer\python.exe

echo ========================================
echo FER2013 Training Script
echo ========================================
echo.
echo Installing dependencies...
%PYTHON_ENV% -m pip install pandas opencv-python scikit-learn

echo.
echo Starting training...
echo.

REM 基础训练 (不使用数据增强)
REM %PYTHON_ENV% train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 64 --epochs 100 --lr 0.001

REM 使用数据增强的训练 (推荐)
%PYTHON_ENV% train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 64 --epochs 100 --lr 0.001 --augment --patience 15

echo.
echo Training completed!
pause
