@echo off

echo =====================================
echo 自动接受Android许可证
echo =====================================

:: 自动接受所有许可证
echo y | "C:\flutter\flutter\bin\flutter.bat" doctor --android-licenses

echo =====================================
echo 许可证接受完成！
echo =====================================
echo 现在可以运行 'python build_apk_full.py' 来构建APK了！
echo =====================================
pause
