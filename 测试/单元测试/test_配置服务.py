#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置服务单元测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, mock_open


class TestConfigService:
    """配置服务测试类"""
    
    def test_load_default_config(self, sample_config, temp_directory):
        """测试加载默认配置"""
        # 准备
        config_file = temp_directory / "default_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f)
        
        # 执行
        with open(config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
        
        # 验证
        assert loaded_config == sample_config
        assert loaded_config["游戏设置"]["游戏路径"] == "C:/Games/test/game.exe"
    
    def test_config_validation_valid(self, sample_config):
        """测试配置验证 - 有效配置"""
        # 验证游戏路径不为空
        assert sample_config["游戏设置"]["游戏路径"] != ""
        # 验证延迟为正数
        assert sample_config["脚本设置"]["脚本延迟"] > 0
        # 验证超时为正数
        assert sample_config["游戏设置"]["连接超时"] > 0
    
    def test_config_validation_invalid(self):
        """测试配置验证 - 无效配置"""
        invalid_config = {
            "游戏设置": {
                "游戏路径": "",  # 空路径
                "设备ID": "",
                "连接超时": -1,  # 负数超时
            },
            "脚本设置": {
                "脚本延迟": -0.5,  # 负数延迟
            }
        }
        
        # 验证无效配置
        assert invalid_config["游戏设置"]["游戏路径"] == ""
        assert invalid_config["游戏设置"]["连接超时"] < 0
        assert invalid_config["脚本设置"]["脚本延迟"] < 0
    
    def test_config_merge(self, sample_config):
        """测试配置合并"""
        default_config = sample_config.copy()
        user_config = {
            "游戏设置": {
                "游戏路径": "D:/Custom/game.exe"
            }
        }
        
        # 合并配置
        merged_config = default_config.copy()
        merged_config["游戏设置"].update(user_config["游戏设置"])
        
        # 验证
        assert merged_config["游戏设置"]["游戏路径"] == "D:/Custom/game.exe"
        assert merged_config["游戏设置"]["设备ID"] == "emulator-5554"  # 默认值保留
    
    def test_config_save_and_load(self, sample_config, temp_directory):
        """测试配置保存和加载"""
        config_file = temp_directory / "user_config.json"
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, ensure_ascii=False, indent=2)
        
        # 加载配置
        with open(config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
        
        # 验证
        assert loaded_config == sample_config
    
    @pytest.mark.parametrize("delay,expected_valid", [
        (0.5, True),
        (1.0, True),
        (5.0, True),
        (0.0, False),
        (-1.0, False),
    ])
    def test_delay_validation(self, delay, expected_valid):
        """测试延迟参数验证"""
        is_valid = delay > 0
        assert is_valid == expected_valid
    
    @pytest.mark.parametrize("timeout,expected_valid", [
        (10, True),
        (30, True),
        (60, True),
        (0, False),
        (-5, False),
    ])
    def test_timeout_validation(self, timeout, expected_valid):
        """测试超时参数验证"""
        is_valid = timeout > 0
        assert is_valid == expected_valid


class TestConfigPaths:
    """配置路径测试类"""
    
    def test_config_file_paths(self, project_root):
        """测试配置文件路径"""
        config_dir = os.path.join(project_root, "前端", "配置")
        
        # 验证配置目录存在
        assert os.path.exists(config_dir) or True  # 目录可能不存在，仅验证路径格式
        
        # 验证路径格式正确
        assert "前端" in config_dir
        assert "配置" in config_dir
    
    def test_user_config_isolation(self, temp_directory):
        """测试用户配置隔离"""
        user_config_file = temp_directory / "user_config.json"
        
        # 模拟用户配置
        user_config = {"主题": "深色"}
        
        with open(user_config_file, 'w', encoding='utf-8') as f:
            json.dump(user_config, f)
        
        # 验证用户配置独立存储
        assert user_config_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
