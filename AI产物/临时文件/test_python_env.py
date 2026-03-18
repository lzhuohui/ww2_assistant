import sys
import os

print("Python Environment Test")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")

# 尝试导入项目中的模块
try:
    import 前端
    print("Successfully imported 前端 module")
except ImportError as e:
    print(f"Failed to import 前端 module: {e}")

# 尝试导入依赖包
try:
    import flet
    print(f"Successfully imported flet version: {flet.__version__}")
except ImportError as e:
    print(f"Failed to import flet: {e}")

print("Test completed!")
