# 构建进度检查脚本
Write-Host "=== APK构建进度检查 ==="
Write-Host "检查时间: $(Get-Date -Format 'HH:mm:ss')"
Write-Host "=========================="

# 检查build目录
if (Test-Path "build") {
    Write-Host "✅ build目录存在"
    
    # 计算目录大小
    $totalSize = 0
    $fileCount = 0
    Get-ChildItem -Path "build" -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $totalSize += $_.Length
        $fileCount++
    }
    
    Write-Host "   目录大小: $([math]::Round($totalSize/1MB, 2)) MB"
    Write-Host "   文件数量: $fileCount"
    
    # 检查关键目录
    Write-Host "`n📂 关键目录状态:"
    
    $checkPaths = @(
        @("build/.hash", "配置哈希"),
        @("build/site-packages", "Python依赖"),
        @("build/flutter", "Flutter项目"),
        @("build/flutter/android", "Android项目"),
        @("build/flutter/android/app", "Android应用"),
        @("build/flutter/android/app/build", "Android构建"),
        @("build/apk", "APK输出")
    )
    
    foreach ($pathInfo in $checkPaths) {
        $path = $pathInfo[0]
        $desc = $pathInfo[1]
        
        if (Test-Path $path) {
            if ((Get-Item $path).PSIsContainer) {
                $itemCount = (Get-ChildItem $path -ErrorAction SilentlyContinue).Count
                Write-Host "   ✅ $desc`: $itemCount个项目"
            } else {
                Write-Host "   ✅ $desc`: 文件存在"
            }
        } else {
            Write-Host "   ⏳ $desc`: 尚未创建"
        }
    }
    
    # 检查APK文件
    $apkFiles = Get-ChildItem -Path "build" -Recurse -Filter "*.apk" -ErrorAction SilentlyContinue
    if ($apkFiles) {
        Write-Host "`n🎉 找到APK文件:"
        $apkFiles | Select-Object -First 3 | ForEach-Object {
            $sizeMB = [math]::Round($_.Length/1MB, 2)
            Write-Host "   📱 $($_.Name) ($sizeMB MB) - $($_.Directory)"
        }
        if ($apkFiles.Count -gt 3) {
            Write-Host "   ... 还有$($apkFiles.Count - 3)个文件"
        }
    } else {
        Write-Host "`n⏳ 尚未生成APK文件"
        Write-Host "   构建仍在进行中..."
        
        # 估计进度
        if ($totalSize -lt 100MB) {
            Write-Host "   📊 进度: 初期阶段 (可能还需10-20分钟)"
        } elseif ($totalSize -lt 300MB) {
            Write-Host "   📊 进度: 中期阶段 (可能还需5-10分钟)"
        } else {
            Write-Host "   📊 进度: 后期阶段 (可能还需1-5分钟)"
        }
    }
    
} else {
    Write-Host "❌ build目录不存在"
    Write-Host "   构建可能尚未开始"
}

# 检查构建进程
Write-Host "`n🔍 构建进程状态:"
$buildProcesses = Get-Process | Where-Object {
    $_.ProcessName -match "python|flutter|java|gradle|dart" -and 
    $_.MainWindowTitle -notmatch "powershell|cmd|conhost"
} | Select-Object -First 5

if ($buildProcesses) {
    Write-Host "   ✅ 找到构建相关进程:"
    $buildProcesses | ForEach-Object {
        Write-Host "      • $($_.ProcessName) (PID: $($_.Id))"
    }
} else {
    Write-Host "   ⏳ 未找到构建进程 (可能已完成或在后台)"
}

Write-Host "`n=========================="
Write-Host "提示: 首次构建需要较长时间"
Write-Host "      - 下载Flutter和Android SDK"
Write-Host "      - 编译Flutter应用"
Write-Host "      - 打包Python依赖"
Write-Host "      - 通常需要15-30分钟"
Write-Host "=========================="