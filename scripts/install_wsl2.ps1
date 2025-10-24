# WSL2 安装脚本
# 请以管理员权限运行 PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WSL2 GPU 环境安装向导" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员运行
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "错误: 请以管理员权限运行此脚本!" -ForegroundColor Red
    Write-Host "右键点击 PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✓ 管理员权限确认" -ForegroundColor Green
Write-Host ""

# 步骤1: 检查WSL是否已安装
Write-Host "步骤1: 检查WSL状态..." -ForegroundColor Yellow
$wslStatus = wsl --status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ WSL已安装" -ForegroundColor Green
    wsl --list --verbose
} else {
    Write-Host "WSL未安装，开始安装..." -ForegroundColor Yellow

    # 启用WSL功能
    Write-Host "  启用 WSL 功能..." -ForegroundColor Cyan
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

    # 启用虚拟机平台
    Write-Host "  启用虚拟机平台..." -ForegroundColor Cyan
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    Write-Host ""
    Write-Host "✓ WSL功能已启用" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ 需要重启计算机以完成安装!" -ForegroundColor Yellow
    Write-Host ""
    $restart = Read-Host "是否现在重启? (Y/N)"

    if ($restart -eq "Y" -or $restart -eq "y") {
        Write-Host "正在重启..." -ForegroundColor Yellow
        shutdown /r /t 10
        exit
    } else {
        Write-Host "请手动重启计算机，然后重新运行此脚本继续安装。" -ForegroundColor Yellow
        pause
        exit
    }
}

Write-Host ""

# 步骤2: 设置WSL2为默认版本
Write-Host "步骤2: 设置WSL2为默认版本..." -ForegroundColor Yellow
wsl --set-default-version 2
Write-Host "✓ WSL2已设为默认版本" -ForegroundColor Green
Write-Host ""

# 步骤3: 检查Ubuntu是否已安装
Write-Host "步骤3: 检查Ubuntu安装状态..." -ForegroundColor Yellow
$ubuntuInstalled = wsl --list | Select-String "Ubuntu"

if ($ubuntuInstalled) {
    Write-Host "✓ Ubuntu已安装" -ForegroundColor Green
    wsl --list --verbose
} else {
    Write-Host "准备安装 Ubuntu 22.04..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "可用的发行版:" -ForegroundColor Cyan
    wsl --list --online
    Write-Host ""

    $install = Read-Host "是否安装 Ubuntu-22.04? (Y/N)"
    if ($install -eq "Y" -or $install -eq "y") {
        Write-Host "正在安装 Ubuntu 22.04..." -ForegroundColor Yellow
        wsl --install -d Ubuntu-22.04
        Write-Host ""
        Write-Host "✓ Ubuntu 22.04 安装完成!" -ForegroundColor Green
    } else {
        Write-Host "已取消安装" -ForegroundColor Yellow
        exit
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WSL2 基础安装完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "1. 启动 WSL2:" -ForegroundColor White
Write-Host "   wsl" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 验证GPU可用性 (在WSL2中运行):" -ForegroundColor White
Write-Host "   nvidia-smi" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. 运行自动配置脚本 (在WSL2中运行):" -ForegroundColor White
Write-Host "   cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER" -ForegroundColor Cyan
Write-Host "   bash wsl2_setup.sh" -ForegroundColor Cyan
Write-Host ""
Write-Host "详细配置指南: WSL2_GPU_SETUP.md" -ForegroundColor Yellow
Write-Host ""

pause
