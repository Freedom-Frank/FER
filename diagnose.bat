@echo off
REM 便捷诊断脚本 - 调用实际的测试脚本
REM 实际脚本位置: scripts/tests/diagnose.py

python scripts\tests\diagnose.py %*
