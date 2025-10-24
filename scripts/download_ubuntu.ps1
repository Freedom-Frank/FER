# Ubuntu WSL 下载脚本 - 使用清华镜像加速
# 请以管理员权限运行 PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ubuntu 22.04 WSL 下载脚本（清华镜像）" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 设置下载路径
$downloadPath = "E:\Downloads"
$fileName = "Ubuntu2204.appx"
$fullPath = Join-Path $downloadPath $fileName

# 创建下载目录
if (-not (Test-Path $downloadPath)) {
    New-Item -ItemType Directory -Path $downloadPath -Force | Out-Null
    Write-Host "✓ 创建下载目录: $downloadPath" -ForegroundColor Green
}

Write-Host "下载目标: $fullPath" -ForegroundColor Yellow
Write-Host ""

# Ubuntu WSL AppX 下载链接（多个备用源）
$urls = @(
    @{
        Name = "清华镜像 - Ubuntu Cloud Images"
        Url = "https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/wsl/jammy/current/ubuntu-jammy-wsl-amd64-wsl.rootfs.tar.gz"
        File = "ubuntu-jammy.tar.gz"
    },
    @{
        Name = "微软官方"
        Url = "https://aka.ms/wslubuntu2204"
        File = "Ubuntu2204.appx"
    },
    @{
        Name = "微软直链"
        Url = "https://wslstorestorage.blob.core.windows.net/wslblob/Ubuntu_2204.0.10.0_x64.appx"
        File = "Ubuntu2204.appx"
    }
)

Write-Host "可用下载源：" -ForegroundColor Cyan
for ($i = 0; $i -lt $urls.Count; $i++) {
    Write-Host "  [$($i+1)] $($urls[$i].Name)" -ForegroundColor White
}
Write-Host ""

# 默认使用清华镜像
$selectedIndex = 0
Write-Host "使用下载源: $($urls[$selectedIndex].Name)" -ForegroundColor Green
$downloadUrl = $urls[$selectedIndex].Url
$targetFile = Join-Path $downloadPath $urls[$selectedIndex].File

Write-Host "下载地址: $downloadUrl" -ForegroundColor Yellow
Write-Host "保存位置: $targetFile" -ForegroundColor Yellow
Write-Host ""

# 检查文件是否已存在
if (Test-Path $targetFile) {
    $overwrite = Read-Host "文件已存在，是否重新下载? (Y/N)"
    if ($overwrite -ne "Y" -and $overwrite -ne "y") {
        Write-Host "使用现有文件: $targetFile" -ForegroundColor Green
        $downloadUrl = $null
    } else {
        Remove-Item $targetFile -Force
    }
}

# 下载文件
if ($downloadUrl) {
    Write-Host "开始下载..." -ForegroundColor Cyan
    Write-Host "提示: 下载可能需要几分钟，请耐心等待" -ForegroundColor Yellow
    Write-Host ""

    try {
        # 使用 Invoke-WebRequest 下载，显示进度
        $ProgressPreference = 'Continue'
        Invoke-WebRequest -Uri $downloadUrl -OutFile $targetFile -UseBasicParsing

        Write-Host ""
        Write-Host "✓ 下载完成!" -ForegroundColor Green
        Write-Host "文件大小: $((Get-Item $targetFile).Length / 1MB) MB" -ForegroundColor Cyan
    }
    catch {
        Write-Host ""
        Write-Host "✗ 下载失败: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "请尝试以下方法:" -ForegroundColor Yellow
        Write-Host "1. 检查网络连接" -ForegroundColor White
        Write-Host "2. 使用浏览器手动下载:" -ForegroundColor White
        Write-Host "   $downloadUrl" -ForegroundColor Cyan
        Write-Host "3. 保存到: $targetFile" -ForegroundColor White
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# 判断文件类型并安装
if ($targetFile -like "*.tar.gz") {
    Write-Host "检测到 tar.gz 格式，需要手动导入" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "导入步骤:" -ForegroundColor Cyan
    Write-Host "1. 创建安装目录:" -ForegroundColor White
    Write-Host "   mkdir E:\WSL\Ubuntu2204" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. 导入 Ubuntu:" -ForegroundColor White
    Write-Host "   wsl --import Ubuntu-22.04 E:\WSL\Ubuntu2204 $targetFile" -ForegroundColor Gray
    Write-Host ""

    $import = Read-Host "是否现在导入? (Y/N)"
    if ($import -eq "Y" -or $import -eq "y") {
        $installPath = "E:\WSL\Ubuntu2204"

        if (-not (Test-Path $installPath)) {
            New-Item -ItemType Directory -Path $installPath -Force | Out-Null
        }

        Write-Host "正在导入 Ubuntu..." -ForegroundColor Cyan
        wsl --import Ubuntu-22.04 $installPath $targetFile

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Ubuntu 导入成功!" -ForegroundColor Green

            # 设置默认用户
            Write-Host ""
            Write-Host "设置默认用户（可选）:" -ForegroundColor Yellow
            Write-Host "启动 Ubuntu 后运行以下命令创建用户:" -ForegroundColor White
            Write-Host "  useradd -m -s /bin/bash <用户名>" -ForegroundColor Gray
            Write-Host "  passwd <用户名>" -ForegroundColor Gray
            Write-Host "  usermod -aG sudo <用户名>" -ForegroundColor Gray
        }
    }
}
else {
    Write-Host "安装 Ubuntu AppX 包..." -ForegroundColor Cyan
    Write-Host ""

    try {
        Add-AppxPackage -Path $targetFile
        Write-Host "✓ Ubuntu 安装成功!" -ForegroundColor Green
        Write-Host ""
        Write-Host "下一步操作:" -ForegroundColor Yellow
        Write-Host "1. 在开始菜单搜索 'Ubuntu 22.04' 并启动" -ForegroundColor White
        Write-Host "2. 首次启动会要求创建用户名和密码" -ForegroundColor White
        Write-Host "3. 或者在 PowerShell 中运行: wsl" -ForegroundColor White
    }
    catch {
        Write-Host "✗ 安装失败: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "请手动安装:" -ForegroundColor Yellow
        Write-Host "1. 双击文件: $targetFile" -ForegroundColor White
        Write-Host "2. 或运行: Add-AppxPackage $targetFile" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 验证安装
Write-Host "验证 WSL 安装状态..." -ForegroundColor Cyan
wsl --list --verbose

Write-Host ""
Write-Host "配置完成后，运行以下命令继续:" -ForegroundColor Yellow
Write-Host "  wsl" -ForegroundColor Cyan
Write-Host "  cd /mnt/e/Users/Meng/Projects/VScodeProjects/FER" -ForegroundColor Cyan
Write-Host "  bash wsl2_setup.sh" -ForegroundColor Cyan
Write-Host ""

pause
