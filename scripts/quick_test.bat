@echo off
REM 快速测试脚本 - 2个epoch验证代码是否正常工作

SET PYTHON_ENV=E:\Users\Meng\Enviroments\conda_envs\fer\python.exe

echo ========================================
echo FER2013 Quick Test (2 epochs)
echo ========================================
echo.

%PYTHON_ENV% train.py --data_csv data/FER2013/fer2013.csv --device_target GPU --batch_size 32 --epochs 2 --augment --lr 0.001

echo.
echo Test completed!
pause
