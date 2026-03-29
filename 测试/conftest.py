#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest配置文件

创建日期: 2026-03-08
作者: AI
版本: v1.0.0
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def project_root():
    """返回项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def mock_flet_page():
    """模拟Flet Page对象"""
    page = Mock()
    page.controls = []
    page.views = []
    page.add = Mock(side_effect=lambda x: page.controls.append(x))
    page.update = Mock()
    page.go = Mock()
    page.push_route = Mock()
    page.theme_mode = Mock()
    page.window_width = 800
    page.window_height = 600
    return page


@pytest.fixture(scope="function")
def mock_flet_control():
    """模拟Flet Control对象"""
    control = Mock()
    control.value = None
    control.text = None
    control.visible = True
    control.disabled = False
    control.update = Mock()
    return control


@pytest.fixture(scope="function")
def sample_config():
    """示例配置数据"""
    return {
        "游戏设置": {
            "游戏路径": "C:/Games/test/game.exe",
            "设备ID": "emulator-5554",
            "连接超时": 30,
            "重试次数": 3
        },
        "脚本设置": {
            "脚本延迟": 1.5,
            "自动运行": False,
            "运行模式": "手动",
            "最大运行时长": 12,
            "休息间隔": 300
        },
        "界面设置": {
            "主题": "浅色",
            "语言": "中文",
            "窗口宽度": 800,
            "窗口高度": 600
        }
    }


@pytest.fixture(scope="function")
def temp_directory(tmp_path):
    """临时目录"""
    return tmp_path


@pytest.fixture(scope="function")
def mock_adb():
    """模拟ADB对象"""
    adb = Mock()
    adb.tap = Mock(return_value=True)
    adb.swipe = Mock(return_value=True)
    adb.screenshot = Mock(return_value=b"fake_image_data")
    adb.connect = Mock(return_value=True)
    adb.disconnect = Mock(return_value=True)
    adb.is_connected = Mock(return_value=True)
    return adb


# 自定义标记
def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line("markers", "unit: 单元测试")
    config.addinivalue_line("markers", "integration: 集成测试")
    config.addinivalue_line("markers", "slow: 慢速测试")
    config.addinivalue_line("markers", "gui: GUI测试")
    config.addinivalue_line("markers", "api: API测试")


def pytest_collection_modifyitems(config, items):
    """修改测试项"""
    for item in items:
        # 自动添加标记
        if "test_" in item.nodeid and "gui" in item.nodeid.lower():
            item.add_marker(pytest.mark.gui)
        elif "test_" in item.nodeid and "api" in item.nodeid.lower():
            item.add_marker(pytest.mark.api)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告钩子"""
    outcome = yield
    report = outcome.get_result()
    
    # 记录测试执行时间
    if report.when == "call":
        setattr(item, "execution_time", call.duration)
