# -*- coding: utf-8 -*-

"""
模块名称：授权管理器.py
模块功能：授权验证与管理

职责：
- 授权码验证
- 授权状态管理
- 试用期管理
- 设备绑定验证
- 换绑管理

不负责：
- UI显示
- 网络通信
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

from 设置界面.层级0_数据管理.授权管理.加密工具 import CryptoUtils
from 设置界面.层级0_数据管理.授权管理.设备识别 import DeviceIdentifier


class LicenseManager:
    """
    授权管理器
    
    职责：
    - 授权码验证
    - 授权状态管理
    - 试用期管理
    - 设备绑定验证
    - 换绑管理
    """
    
    _instance = None
    
    TRIAL_DAYS = 7
    MAX_CHANGE_COUNT = 3
    CHANGE_COOLDOWN_DAYS = 7
    GRACE_PERIOD_HOURS = 24
    
    LICENSE_FILE = ".license"
    TRIAL_FILE = ".trial"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._device_identifier = DeviceIdentifier()
        self._license_data: Dict = None
        self._trial_data: Dict = None
        
        self._load_license()
        self._load_trial()
    
    def verify_license(self) -> Dict[str, Any]:
        """
        验证授权状态
        
        返回:
            {
                "valid": True/False,
                "is_trial": True/False,
                "remaining_days": 30,
                "account_limit": 5,
                "device_matched": True/False,
                "message": "授权有效"
            }
        """
        if self._license_data:
            return self._verify_paid_license()
        else:
            return self._verify_trial_license()
    
    def _verify_paid_license(self) -> Dict[str, Any]:
        """验证付费授权"""
        current_device = self._device_identifier.get_device_id()
        bound_device = self._license_data.get("bound_device", "")
        
        if bound_device and bound_device != current_device:
            old_device_grace = self._license_data.get("old_device_grace_until")
            if old_device_grace:
                grace_time = datetime.fromisoformat(old_device_grace)
                if datetime.now() < grace_time:
                    pass
                else:
                    return {
                        "valid": False,
                        "is_trial": False,
                        "remaining_days": 0,
                        "account_limit": 0,
                        "device_matched": False,
                        "message": "设备不匹配，请使用绑定的设备或申请换绑"
                    }
            else:
                return {
                    "valid": False,
                    "is_trial": False,
                    "remaining_days": 0,
                    "account_limit": 0,
                    "device_matched": False,
                    "message": "设备不匹配，请使用绑定的设备或申请换绑"
                }
        
        expire_time = datetime.fromisoformat(self._license_data.get("expire_time", "2000-01-01"))
        remaining_days = (expire_time - datetime.now()).days
        
        if remaining_days <= 0:
            return {
                "valid": False,
                "is_trial": False,
                "remaining_days": 0,
                "account_limit": 0,
                "device_matched": True,
                "message": "授权已过期"
            }
        
        return {
            "valid": True,
            "is_trial": False,
            "remaining_days": remaining_days,
            "account_limit": self._license_data.get("account_limit", 1),
            "device_matched": True,
            "message": "授权有效"
        }
    
    def _verify_trial_license(self) -> Dict[str, Any]:
        """验证试用授权"""
        if not self._trial_data:
            self._init_trial()
        
        first_run = datetime.fromisoformat(self._trial_data.get("first_run", datetime.now().isoformat()))
        elapsed_days = (datetime.now() - first_run).days
        remaining_days = max(0, self.TRIAL_DAYS - elapsed_days)
        
        if remaining_days <= 0:
            return {
                "valid": False,
                "is_trial": True,
                "remaining_days": 0,
                "account_limit": 1,
                "device_matched": True,
                "message": "试用期已结束，请购买授权"
            }
        
        return {
            "valid": True,
            "is_trial": True,
            "remaining_days": remaining_days,
            "account_limit": 1,
            "device_matched": True,
            "message": f"试用期剩余{remaining_days}天"
        }
    
    def activate_license(self, license_code: str) -> Dict[str, Any]:
        """
        激活授权码
        
        参数:
            license_code: 授权码
        
        返回:
            {"success": True/False, "message": "激活成功"}
        """
        try:
            decoded = CryptoUtils.decrypt(license_code)
            license_info = json.loads(decoded)
        except Exception as e:
            return {"success": False, "message": f"授权码格式错误: {str(e)}"}
        
        if not self._verify_license_signature(license_info):
            return {"success": False, "message": "授权码签名验证失败"}
        
        current_device = self._device_identifier.get_device_id()
        now = datetime.now()
        expire_time = now + timedelta(days=license_info.get("days", 30))
        
        self._license_data = {
            "license_code": license_code,
            "account_limit": license_info.get("account_limit", 1),
            "days": license_info.get("days", 30),
            "bound_device": current_device,
            "activate_time": now.isoformat(),
            "expire_time": expire_time.isoformat(),
            "change_count": 0,
            "last_change_time": None,
            "old_device_grace_until": None,
        }
        
        self._save_license()
        
        return {"success": True, "message": "激活成功"}
    
    def request_device_change(self) -> Dict[str, Any]:
        """
        请求设备换绑
        
        返回:
            {"success": True/False, "message": "...", "remaining_changes": 2}
        """
        if not self._license_data:
            return {"success": False, "message": "无有效授权"}
        
        change_count = self._license_data.get("change_count", 0)
        if change_count >= self.MAX_CHANGE_COUNT:
            return {"success": False, "message": "换绑次数已用完"}
        
        last_change = self._license_data.get("last_change_time")
        if last_change:
            last_change_time = datetime.fromisoformat(last_change)
            days_since_change = (datetime.now() - last_change_time).days
            if days_since_change < self.CHANGE_COOLDOWN_DAYS:
                remaining_days = self.CHANGE_COOLDOWN_DAYS - days_since_change
                return {"success": False, "message": f"冷却期剩余{remaining_days}天"}
        
        old_device = self._license_data.get("bound_device", "")
        new_device = self._device_identifier.get_device_id()
        
        if old_device == new_device:
            return {"success": False, "message": "当前设备已绑定"}
        
        grace_until = datetime.now() + timedelta(hours=self.GRACE_PERIOD_HOURS)
        
        self._license_data["old_device"] = old_device
        self._license_data["bound_device"] = new_device
        self._license_data["change_count"] = change_count + 1
        self._license_data["last_change_time"] = datetime.now().isoformat()
        self._license_data["old_device_grace_until"] = grace_until.isoformat()
        
        self._save_license()
        
        return {
            "success": True,
            "message": "换绑成功",
            "remaining_changes": self.MAX_CHANGE_COUNT - change_count - 1
        }
    
    def get_license_info(self) -> Dict[str, Any]:
        """
        获取授权信息
        
        返回:
            授权信息字典
        """
        if self._license_data:
            return {
                "type": "paid",
                "account_limit": self._license_data.get("account_limit", 1),
                "activate_time": self._license_data.get("activate_time"),
                "expire_time": self._license_data.get("expire_time"),
                "change_count": self._license_data.get("change_count", 0),
                "bound_device": self._license_data.get("bound_device"),
            }
        elif self._trial_data:
            first_run = datetime.fromisoformat(self._trial_data.get("first_run", datetime.now().isoformat()))
            elapsed_days = (datetime.now() - first_run).days
            return {
                "type": "trial",
                "account_limit": 1,
                "first_run": self._trial_data.get("first_run"),
                "remaining_days": max(0, self.TRIAL_DAYS - elapsed_days),
            }
        else:
            return {"type": "none"}
    
    def can_enable_account(self, current_enabled: int) -> bool:
        """
        检查是否可以启用更多账号
        
        参数:
            current_enabled: 当前已启用的账号数
        
        返回:
            是否可以启用
        """
        status = self.verify_license()
        if not status["valid"]:
            return False
        
        return current_enabled < status["account_limit"]
    
    def _verify_license_signature(self, license_info: Dict) -> bool:
        """验证授权签名"""
        signature = license_info.pop("signature", None)
        if not signature:
            return False
        
        data = json.dumps(license_info, sort_keys=True)
        return CryptoUtils.verify_sign(data, signature)
    
    def _init_trial(self):
        """初始化试用期"""
        self._trial_data = {
            "first_run": datetime.now().isoformat(),
            "random_seed": os.urandom(16).hex(),
        }
        self._save_trial()
    
    def _load_license(self):
        """加载授权数据"""
        try:
            if os.path.exists(self.LICENSE_FILE):
                with open(self.LICENSE_FILE, 'r') as f:
                    encrypted = f.read()
                decrypted = CryptoUtils.decrypt(encrypted)
                self._license_data = json.loads(decrypted)
        except:
            self._license_data = None
    
    def _save_license(self):
        """保存授权数据"""
        try:
            data = json.dumps(self._license_data)
            encrypted = CryptoUtils.encrypt(data)
            with open(self.LICENSE_FILE, 'w') as f:
                f.write(encrypted)
        except:
            pass
    
    def _load_trial(self):
        """加载试用数据"""
        try:
            if os.path.exists(self.TRIAL_FILE):
                with open(self.TRIAL_FILE, 'r') as f:
                    encrypted = f.read()
                decrypted = CryptoUtils.decrypt(encrypted)
                self._trial_data = json.loads(decrypted)
        except:
            self._trial_data = None
    
    def _save_trial(self):
        """保存试用数据"""
        try:
            data = json.dumps(self._trial_data)
            encrypted = CryptoUtils.encrypt(data)
            with open(self.TRIAL_FILE, 'w') as f:
                f.write(encrypted)
        except:
            pass


if __name__ == "__main__":
    print("测试授权管理器...")
    
    manager = LicenseManager()
    
    status = manager.verify_license()
    print(f"授权状态: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    info = manager.get_license_info()
    print(f"授权信息: {json.dumps(info, indent=2, ensure_ascii=False)}")
    
    print("测试通过!")
