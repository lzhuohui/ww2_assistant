@echo off
chcp 65001 >nul
title Flet界面测试启动器

echo ===========================================
echo     Flet界面测试启动器
echo ===========================================
echo.
echo 请选择要运行的测试界面：
echo.
echo  [1] 基础界面测试 - 按钮、输入框、进度条
echo  [2] 配置界面测试 - 游戏辅助工具配置界面
echo  [3] 监控界面测试 - 实时监控面板
echo  [4] 运行全部测试（依次打开）
echo  [0] 退出
echo.
echo ===========================================
set /p choice="请输入选项 (0-4): "

if "%choice%"=="1" goto test1
if "%choice%"=="2" goto test2
if "%choice%"=="3" goto test3
if "%choice%"=="4" goto test_all
if "%choice%"=="0" goto exit
goto invalid

:test1
echo.
echo 正在启动基础界面测试...
cd /d "%~dp0"
"..\..\venv\Scripts\python.exe" test_flet界面实例.py
goto end

:test2
echo.
echo 正在启动配置界面测试...
cd /d "%~dp0"
"..\..\venv\Scripts\python.exe" test_配置界面实例.py
goto end

:test3
echo.
echo 正在启动监控界面测试...
cd /d "%~dp0"
"..\..\venv\Scripts\python.exe" test_监控界面实例.py
goto end

:test_all
echo.
echo 将依次运行所有测试界面...
echo 请关闭当前界面后继续下一个
echo.
echo [1/3] 启动基础界面测试...
"..\..\venv\Scripts\python.exe" test_flet界面实例.py
echo.
echo [2/3] 启动配置界面测试...
"..\..\venv\Scripts\python.exe" test_配置界面实例.py
echo.
echo [3/3] 启动监控界面测试...
"..\..\venv\Scripts\python.exe" test_监控界面实例.py
goto end

:invalid
echo.
echo 无效的选项，请重新运行脚本
goto end

:exit
echo.
echo 已退出

:end
echo.
echo 按任意键关闭窗口...
pause >nul
