# -*- coding: utf-8 -*-

"""
模块名称：设备识别.py
模块功能：设备指纹生成与识别

职责：
- 获取设备标识信息
- 生成设备指纹
- 模拟器检测

不负责：
- 授权验证逻辑
"""

import hashlib
import os
import json
import time
from typing import Dict, Optional


class DeviceIdentifier:
    """
    设备识别类
    
    职责：
    - 获取设备标识信息
    - 生成设备指纹
    - 模拟器检测
    """
    
    _instance = None
    _device_info: Dict = None
    _random_seed: str = None
    
    SEED_FILE = ".device_seed"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._device_info is None:
            self._device_info = self._collect_device_info()
            self._random_seed = self._get_or_create_seed()
    
    def get_device_id(self) -> str:
        """
        获取设备指纹
        
        返回:
            设备指纹（32位十六进制）
        """
        components = [
            self._device_info.get("android_id", ""),
            self._device_info.get("model", ""),
            self._device_info.get("manufacturer", ""),
            self._device_info.get("brand", ""),
            self._device_info.get("sdk_version", ""),
            self._device_info.get("install_time", ""),
            self._random_seed,
        ]
        
        combined = "|".join(str(c) for c in components)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_device_info(self) -> Dict:
        """
        获取设备信息
        
        返回:
            设备信息字典
        """
        return self._device_info.copy()
    
    def is_emulator(self) -> bool:
        """
        检测是否为模拟器
        
        返回:
            是否为模拟器
        """
        info = self._device_info
        
        emulator_signs = [
            info.get("fingerprint", "").lower().find("generic") >= 0,
            info.get("fingerprint", "").lower().find("sdk") >= 0,
            info.get("model", "").lower().find("sdk") >= 0,
            info.get("model", "").lower().find("emulator") >= 0,
            info.get("manufacturer", "").lower() in ["genymotion", "unknown", "google"],
            info.get("hardware", "").lower() in ["goldfish", "ranchu", "vbox86"],
            info.get("product", "").lower().find("sdk") >= 0,
            info.get("board", "").lower() in ["goldfish", "ranchu"],
        ]
        
        return sum(emulator_signs) >= 2
    
    def _collect_device_info(self) -> Dict:
        """
        收集设备信息
        
        返回:
            设备信息字典
        """
        try:
            import android.os.Build as Build
            import android.provider.Settings as Settings
            import android.content.Context as Context
            
            context = Context.getApplicationContext()
            android_id = Settings.Secure.getString(
                context.getContentResolver(),
                Settings.Secure.ANDROID_ID
            )
            
            return {
                "android_id": android_id or "",
                "model": Build.MODEL or "",
                "manufacturer": Build.MANUFACTURER or "",
                "brand": Build.BRAND or "",
                "device": Build.DEVICE or "",
                "product": Build.PRODUCT or "",
                "board": Build.BOARD or "",
                "hardware": Build.HARDWARE or "",
                "fingerprint": Build.FINGERPRINT or "",
                "sdk_version": str(Build.VERSION.SDK_INT) if Build.VERSION.SDK_INT else "",
                "install_time": self._get_install_time(),
            }
        except ImportError:
            return self._collect_desktop_info()
    
    def _collect_desktop_info(self) -> Dict:
        """
        收集桌面环境信息（开发测试用）
        
        返回:
            模拟设备信息字典
        """
        import platform
        import uuid
        
        return {
            "android_id": str(uuid.getnode()),
            "model": platform.node(),
            "manufacturer": platform.system(),
            "brand": platform.system(),
            "device": platform.machine(),
            "product": "desktop",
            "board": "desktop",
            "hardware": platform.processor() or "unknown",
            "fingerprint": f"desktop/{platform.system()}/{platform.release()}",
            "sdk_version": "30",
            "install_time": self._get_install_time(),
        }
    
    def _get_install_time(self) -> str:
        """
        获取APK安装时间
        
        返回:
            安装时间字符串
        """
        try:
            install_time_file = ".install_time"
            if os.path.exists(install_time_file):
                with open(install_time_file, 'r') as f:
                    return f.read().strip()
            else:
                install_time = str(int(time.time()))
                with open(install_time_file, 'w') as f:
                    f.write(install_time)
                return install_time
        except:
            return str(int(time.time()))
    
    def _get_or_create_seed(self) -> str:
        """
        获取或创建随机种子
        
        返回:
            随机种子
        """
        try:
            if os.path.exists(self.SEED_FILE):
                with open(self.SEED_FILE, 'r') as f:
                    return f.read().strip()
            else:
                seed = os.urandom(16).hex()
                with open(self.SEED_FILE, 'w') as f:
                    f.write(seed)
                return seed
        except:
            return os.urandom(16).hex()
    
    def reset_seed(self):
        """重置随机种子（用于测试）"""
        self._random_seed = os.urandom(16).hex()
        try:
            with open(self.SEED_FILE, 'w') as f:
                f.write(self._random_seed)
        except:
            pass


if __name__ == "__main__":
    print("测试设备识别...")
    
    identifier = DeviceIdentifier()
    
    print(f"设备指纹: {identifier.get_device_id()}")
    print(f"设备信息: {json.dumps(identifier.get_device_info(), indent=2, ensure_ascii=False)}")
    print(f"是否模拟器: {identifier.is_emulator()}")
    
    print("测试通过!")
