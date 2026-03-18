# -*- coding: utf-8 -*-
"""
模块名称：输入验证 | 层级：工具层
设计思路：
    提供输入格式验证功能，确保数据质量。
功能列表：
    1. 账号输入格式验证
    2. 验证结果返回
对外接口：
    - validate_account_input(input_text): 验证账号输入格式
    - get_subtitle_by_state(switch_enabled, input_text): 根据状态获取副标题
    - can_participate(switch_enabled, input_text): 判断是否可以参与挂机
"""

from typing import Tuple

# *** 用户指定变量 - AI不得修改 ***
# *********************************


def validate_account_input(input_text: str) -> Tuple[bool, str, str]:
    """
    验证账号输入格式
    
    格式要求: 名称/账号/密码
    
    参数:
        input_text: 输入文本
    
    返回:
        Tuple[bool, str, str]: (是否有效, 副标题文本, 提示类型)
        提示类型: "success" | "error" | "info"
    """
    if not input_text or not input_text.strip():
        return False, "请输入账号信息", "info"
    
    parts = input_text.split("/")
    if len(parts) != 3:
        return False, "格式错误：名称/账号/密码", "error"
    
    name, account, password = parts
    
    if not name.strip():
        return False, "名称不能为空", "error"
    if not account.strip():
        return False, "账号不能为空", "error"
    if not password.strip():
        return False, "密码不能为空", "error"
    
    return True, "参与挂机", "success"


def get_subtitle_by_state(switch_enabled: bool, input_text: str) -> str:
    """
    根据开关状态和输入内容获取副标题
    
    参数:
        switch_enabled: 开关是否打开
        input_text: 输入框内容
    
    返回:
        str: 副标题文本
    """
    if not switch_enabled:
        return "禁止挂机"
    
    is_valid, subtitle, _ = validate_account_input(input_text)
    return subtitle


def can_participate(switch_enabled: bool, input_text: str) -> bool:
    """
    判断是否可以参与挂机
    
    参数:
        switch_enabled: 开关是否打开
        input_text: 输入框内容
    
    返回:
        bool: 是否可以参与挂机
    """
    if not switch_enabled:
        return False
    
    is_valid, _, _ = validate_account_input(input_text)
    return is_valid





# *** 调试逻辑 ***
if __name__ == "__main__":
    test_cases = [
        ("测试用户/test_account/test_password", True),
        ("测试用户/test_account/", False),
        ("无效格式", False),
    ]
    for input_text, expected_valid in test_cases:
        is_valid, subtitle, tip_type = validate_account_input(input_text)
        status = "✓" if is_valid == expected_valid else "✗"
        print(f"{status} 输入: '{input_text}' -> 有效={is_valid}, 副标题='{subtitle}'")
