import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "windows11_v2"))

from 原子层.界面配置 import 界面配置

配置 = 界面配置()
print(f"bg_primary: {配置.获取颜色('bg_primary')}")
print(f"bg_secondary: {配置.获取颜色('bg_secondary')}")
print(f"bg_card: {配置.获取颜色('bg_card')}")
print(f"text_primary: {配置.获取颜色('text_primary')}")
print(f"border: {配置.获取颜色('border')}")
