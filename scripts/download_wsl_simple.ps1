# 简化版WSL Ubuntu下载脚本 - 清华镜像

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Ubuntu 22.04 下载脚本" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 设置路径
$downloadPath = "E:\Downloads"
$targetFile = "$downloadPath\ubuntu-jammy.tar.gz"
$installPath = "E:\WSL\Ubuntu2204"

# 创建下载目录
if (-not (Test-Path $downloadPath)) {
    New-Item -ItemType Directory -Path $downloadPath -Force | Out-Null
}

Write-Host "下载源: 清华镜像" -ForegroundColor Green
Write-Host "保存位置: $targetFile" -ForegroundColor Yellow
Write-Host ""

# 下载URL
$url = "https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/wsl/jammy/current/ubuntu-jammy-wsl-amd64-wsl.rootfs.tar.gz"

# 检查文件是否存在
if (Test-Path $targetFile) {
    Write-Host "文件已存在，跳过下载" -ForegroundColor Yellow
} else {
    Write-Host "开始下载..." -ForegroundColor Cyan
    Write-Host "文件大小约: 500MB，请耐心等待" -ForegroundColor Yellow
    Write-Host ""

    try {
        Invoke-WebRequest -Uri $url -OutFile $targetFile -UseBasicParsing
        Write-Host ""
        Write-Host "下载完成!" -ForegroundColor Green
    }
    catch {
        Write-Host ""
        Write-Host "下载失败: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "请手动下载:" -ForegroundColor Yellow
        Write-Host $url -ForegroundColor Cyan
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "导入Ubuntu到WSL2" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 创建WSL安装目录
if (-not (Test-Path $installPath)) {
    New-Item -ItemType Directory -Path $installPath -Force | Out-Null
    Write-Host "创建安装目录: $installPath" -ForegroundColor Green
}

# 导入Ubuntu
Write-Host "正在导入Ubuntu..." -ForegroundColor Cyan
wsl --import Ubuntu-22.04 $installPath $targetFile

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Ubuntu导入成功!" -ForegroundColor Green

    # 设置WSL2
    Write-Host "设置为WSL2..." -ForegroundColor Cyan
    wsl --set-version Ubuntu-22.04 2
    wsl --set-default Ubuntu-22.04

    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "安装完成!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""

    # 验证
    wsl --list --verbose

    Write-Host ""
    Write-Host "下一步操作:" -ForegroundColor Yellow
    Write-Host "1. 启动WSL: wsl" -ForegroundColor White
    Write-Host "2. 创建用户 (在WSL中运行):" -ForegroundColor White
    Write-Host "   adduser <用户名>" -ForegroundColor Gray
    Write-Host "   usermod -aG sudo <用户名>" -ForegroundColor Gray
    Write-Host "3. 运行配置脚本:" -ForegroundColor White
    Write-Host "   cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER" -ForegroundColor Gray
    Write-Host "   bash wsl2_setup.sh" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "导入失败!" -ForegroundColor Red
}

Write-Host ""
pause
