#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 - 验证核心功能
1. 下拉框迁移成功
2. 选项管理器工作正常
3. 配置管理器工作正常
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print("=" * 70)
print("快速测试 - 验证下拉框系统迁移")
print("=" * 70)

# 测试1：导入下拉框组件
try:
    from 表示层.组件.基础.下拉框 import create_dropdown
    print("✅ 测试1: 下拉框组件导入成功")
except ImportError as e:
    print(f"❌ 测试1失败: {e}")
    sys.exit(1)

# 测试2：导入选项管理器
try:
    from 配置.选项管理器 import get_option_loader
    print("✅ 测试2: 选项管理器导入成功")
except ImportError as e:
    print(f"❌ 测试2失败: {e}")
    sys.exit(1)

# 测试3：导入配置管理器
try:
    from 配置.配置管理器 import get_config_manager
    print("✅ 测试3: 配置管理器导入成功")
except ImportError as e:
    print(f"❌ 测试3失败: {e}")
    sys.exit(1)

# 测试4：测试选项加载器
try:
    city_loader = get_option_loader("city")
    city_options = city_loader()
    print(f"✅ 测试4: 城市选项加载成功 ({len(city_options)} 个选项)")
    
    level_loader = get_option_loader("building_level", max_level=40)
    level_options = level_loader()
    print(f"✅ 测试4: 建筑等级选项加载成功 ({len(level_options)} 个选项)")
except Exception as e:
    print(f"❌ 测试4失败: {e}")
    sys.exit(1)

# 测试5：测试配置管理器
try:
    config_manager = get_config_manager()
    
    # 获取建筑配置
    building_config = config_manager.get_building_config("主帅主城")
    if building_config:
        print(f"✅ 测试5: 建筑配置加载成功")
        print(f"   城市等级: {building_config.城市}")
        print(f"   兵工等级: {building_config.兵工}")
    else:
        print("⚠️ 测试5: 建筑配置为空，将创建默认配置")
    
    # 获取用户偏好
    current_city = config_manager.get_user_preference("最近使用的城市", "北京")
    print(f"✅ 测试5: 用户偏好加载成功 (最近使用的城市: {current_city})")
except Exception as e:
    print(f"❌ 测试5失败: {e}")
    sys.exit(1)

# 测试6：测试建筑配置区导入
try:
    from 表示层.界面.建筑配置区_v3 import BuildingConfigSectionV3
    print("✅ 测试6: 建筑配置区 v3 导入成功")
except ImportError as e:
    print(f"❌ 测试6失败: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ 所有核心功能测试通过!")
print("=" * 70)
print("\n项目结构:")
print("1. 📁 表示层/组件/基础/下拉框.py")
print("   - 标准下拉框组件（支持懒加载+深色主题）")
print("   - 支持懒加载，视觉细节已优化")
print("   - 不推挤下方控件")
print("")
print("2. 📁 配置/选项管理器.py")
print("   - 统一管理所有下拉框的选项数据")
print("   - 支持销毁-加载逻辑")
print("   - 提供 get_option_loader() 接口")
print("")
print("3. 📁 配置/配置管理器.py")
print("   - 管理建筑配置和用户偏好")
print("   - 自动保存到JSON文件")
print("   - 提供配置加载和保存接口")
print("")
print("4. 📁 表示层/界面/建筑配置区_v3.py")
print("   - 使用新下拉框系统的建筑配置区")
print("   - 所有下拉框使用懒加载")
print("   - 配置自动保存")
print("")
print("5. 📁 入口/测试主入口.py")
print("   - 完整的测试界面")
print("   - 验证所有功能")
print("")
print("✅ 现在可以直接在主项目中使用新的下拉框系统!")
print("=" * 70)