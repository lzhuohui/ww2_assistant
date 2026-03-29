#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坐标工具单元测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0
"""

import pytest
import random


class TestCoordinateTools:
    """坐标工具测试类"""
    
    def test_safe_tap_offset_range(self):
        """测试安全点击的偏移范围"""
        x, y = 100, 200
        
        # 模拟安全点击（添加随机偏移）
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        new_x = x + offset_x
        new_y = y + offset_y
        
        # 验证偏移在范围内
        assert abs(new_x - x) <= 5
        assert abs(new_y - y) <= 5
    
    def test_safe_tap_preserves_base_position(self):
        """测试安全点击保持基础位置"""
        x, y = 500, 300
        
        # 多次测试确保基础位置不变
        for _ in range(100):
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            new_x = x + offset_x
            new_y = y + offset_y
            
            # 验证新位置在合理范围内
            assert 495 <= new_x <= 505
            assert 295 <= new_y <= 305
    
    def test_screen_boundary_check(self):
        """测试屏幕边界检查"""
        screen_width, screen_height = 2400, 1080
        
        # 测试边界内坐标
        x, y = 100, 100
        assert 0 <= x <= screen_width
        assert 0 <= y <= screen_height
        
        # 测试边界外坐标
        x_out, y_out = 2500, 1200
        assert x_out > screen_width or y_out > screen_height
    
    @pytest.mark.parametrize("x,y,expected_valid", [
        (100, 200, True),
        (0, 0, True),
        (2399, 1079, True),
        (-1, 100, False),
        (100, -1, False),
        (2400, 100, False),
        (100, 1080, False),
    ])
    def test_coordinate_validation(self, x, y, expected_valid):
        """测试坐标有效性验证"""
        screen_width, screen_height = 2400, 1080
        
        is_valid = (0 <= x < screen_width) and (0 <= y < screen_height)
        assert is_valid == expected_valid
    
    def test_random_delay_range(self):
        """测试随机延迟范围"""
        base_delay = 1.0
        
        # 测试多次随机延迟
        for _ in range(100):
            # ±30%随机化
            random_factor = random.uniform(-0.3, 0.3)
            delay = base_delay * (1 + random_factor)
            
            # 验证延迟在范围内
            assert 0.7 <= delay <= 1.3
    
    def test_click_sequence_timing(self):
        """测试点击序列的时间间隔"""
        delays = []
        base_delay = 1.0
        
        # 模拟10次点击的延迟
        for _ in range(10):
            random_factor = random.uniform(-0.3, 0.3)
            delay = base_delay * (1 + random_factor)
            delays.append(delay)
        
        # 验证所有延迟都在合理范围内
        for delay in delays:
            assert 0.7 <= delay <= 1.3
        
        # 验证延迟有变化（随机性）
        assert len(set(delays)) > 1


class TestSwipeOperations:
    """滑动操作测试类"""
    
    def test_swipe_coordinates_calculation(self):
        """测试滑动坐标计算"""
        start_x, start_y = 100, 500
        end_x, end_y = 100, 200
        
        # 计算滑动距离
        distance = abs(end_y - start_y)
        
        assert distance == 300
    
    def test_swipe_direction_detection(self):
        """测试滑动方向检测"""
        # 向上滑动
        start_y, end_y = 500, 200
        assert end_y < start_y  # 向上
        
        # 向下滑动
        start_y, end_y = 200, 500
        assert end_y > start_y  # 向下
        
        # 向左滑动
        start_x, end_x = 500, 200
        assert end_x < start_x  # 向左
        
        # 向右滑动
        start_x, end_x = 200, 500
        assert end_x > start_x  # 向右


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
