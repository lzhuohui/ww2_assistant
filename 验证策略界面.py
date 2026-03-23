# -*- coding: utf-8 -*-
"""验证策略界面功能"""
from 前端.用户设置界面.界面模块.策略界面 import StrategyInterface, USER_CARD_NAMES
from 前端.用户设置界面.配置.卡片配置 import 卡片配置

print('策略界面卡片名称列表:', USER_CARD_NAMES)
print()

all_exist = True
for name in USER_CARD_NAMES:
    config = 卡片配置.get(name)
    if config:
        print(f'{name}: 配置存在')
        card_type = config.get('card_type')
        title = config.get('title')
        icon = config.get('icon')
        print(f'  - 类型: {card_type}')
        print(f'  - 标题: {title}')
        print(f'  - 图标: {icon}')
    else:
        print(f'{name}: 配置缺失!')
        all_exist = False

print()
if all_exist:
    print('验证结果: 所有卡片配置均存在，策略界面功能完整')
else:
    print('验证结果: 存在缺失的卡片配置')
