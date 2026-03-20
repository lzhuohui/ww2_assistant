@echo off

REM 激活虚拟环境
echo 激活虚拟环境...
call ..\..\venv\Scripts\activate.bat

REM 显示当前环境
echo 当前环境:
python --version
echo 虚拟环境已激活，请在该环境中运行项目

pause
