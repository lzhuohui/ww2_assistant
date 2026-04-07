# 自动接受Android许可证的PowerShell脚本

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " 自动接受Android许可证 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green

# 设置Flutter路径
$flutterPath = "C:\flutter\flutter\bin\flutter.bat"

# 检查flutter.bat是否存在
if (-not (Test-Path $flutterPath)) {
    Write-Host "❌ Flutter可执行文件不存在: $flutterPath" -ForegroundColor Red
    exit 1
}

Write-Host "正在自动接受Android许可证..."
Write-Host "这可能需要几分钟时间..."

# 创建一个临时文件来存储输入
try {
    # 创建临时输入文件
    $inputFile = "$env:TEMP\license_input.txt"
    "y`ny`ny`ny`ny`ny`ny`n" | Out-File -FilePath $inputFile -Encoding ASCII
    
    # 运行flutter命令并重定向输入
    $process = Start-Process -FilePath $flutterPath -ArgumentList "doctor", "--android-licenses" -Wait -NoNewWindow -RedirectStandardInput $inputFile
    
    Write-Host "✅ 许可证接受完成！" -ForegroundColor Green
    
    # 清理临时文件
    Remove-Item $inputFile -Force -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "❌ 执行过程中出现错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " 操作完成 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "现在可以运行 'python build_apk_full.py' 来构建APK了！"
