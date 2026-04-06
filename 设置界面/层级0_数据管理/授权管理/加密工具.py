# -*- coding: utf-8 -*-

"""
模块名称：加密工具.py
模块功能：授权系统加密解密工具

职责：
- AES加密/解密
- 数据签名/验证
- 密钥派生

不负责：
- 授权业务逻辑
"""

import hashlib
import base64
import os
from typing import Tuple, Optional

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False


class CryptoUtils:
    """
    加密工具类
    
    职责：
    - AES加密/解密
    - 数据签名/验证
    - 密钥派生
    """
    
    SECRET_KEY = b"WW2_Helper_2026_Secret_Key_32b!"
    IV_LENGTH = 16
    SALT_LENGTH = 8
    
    @classmethod
    def encrypt(cls, data: str, key: bytes = None) -> str:
        """
        加密数据
        
        参数:
            data: 原始数据
            key: 密钥（可选，默认使用内置密钥）
        
        返回:
            加密后的Base64字符串
        """
        if key is None:
            key = cls.SECRET_KEY
        
        if HAS_CRYPTOGRAPHY:
            return cls._encrypt_aes(data, key)
        else:
            return cls._encrypt_simple(data, key)
    
    @classmethod
    def decrypt(cls, encrypted_data: str, key: bytes = None) -> str:
        """
        解密数据
        
        参数:
            encrypted_data: 加密后的Base64字符串
            key: 密钥（可选，默认使用内置密钥）
        
        返回:
            解密后的原始数据
        """
        if key is None:
            key = cls.SECRET_KEY
        
        if HAS_CRYPTOGRAPHY:
            return cls._decrypt_aes(encrypted_data, key)
        else:
            return cls._decrypt_simple(encrypted_data, key)
    
    @classmethod
    def _encrypt_aes(cls, data: str, key: bytes) -> str:
        """AES加密"""
        iv = os.urandom(cls.IV_LENGTH)
        salt = os.urandom(cls.SALT_LENGTH)
        
        derived_key = cls._derive_key(key, salt)
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
        
        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        result = salt + iv + encrypted
        return base64.b64encode(result).decode('utf-8')
    
    @classmethod
    def _decrypt_aes(cls, encrypted_data: str, key: bytes) -> str:
        """AES解密"""
        raw_data = base64.b64decode(encrypted_data)
        
        salt = raw_data[:cls.SALT_LENGTH]
        iv = raw_data[cls.SALT_LENGTH:cls.SALT_LENGTH + cls.IV_LENGTH]
        encrypted = raw_data[cls.SALT_LENGTH + cls.IV_LENGTH:]
        
        derived_key = cls._derive_key(key, salt)
        
        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode('utf-8')
    
    @classmethod
    def _encrypt_simple(cls, data: str, key: bytes) -> str:
        """简单加密（无cryptography库时使用）"""
        salt = os.urandom(cls.SALT_LENGTH)
        derived_key = cls._derive_key(key, salt)
        
        key_stream = derived_key * ((len(data) // 16) + 1)
        
        encrypted = bytes([
            ord(data[i]) ^ key_stream[i % len(derived_key)]
            for i in range(len(data))
        ])
        
        result = salt + encrypted
        return base64.b64encode(result).decode('utf-8')
    
    @classmethod
    def _decrypt_simple(cls, encrypted_data: str, key: bytes) -> str:
        """简单解密（无cryptography库时使用）"""
        raw_data = base64.b64decode(encrypted_data)
        
        salt = raw_data[:cls.SALT_LENGTH]
        encrypted = raw_data[cls.SALT_LENGTH:]
        
        derived_key = cls._derive_key(key, salt)
        
        data = bytes([
            encrypted[i] ^ derived_key[i % len(derived_key)]
            for i in range(len(encrypted))
        ])
        
        return data.decode('utf-8')
    
    @classmethod
    def _derive_key(cls, key: bytes, salt: bytes) -> bytes:
        """派生密钥"""
        return hashlib.sha256(key + salt).digest()
    
    @classmethod
    def sign(cls, data: str) -> str:
        """
        生成数据签名
        
        参数:
            data: 原始数据
        
        返回:
            签名（MD5）
        """
        return hashlib.md5((data + cls.SECRET_KEY.decode()).encode()).hexdigest()
    
    @classmethod
    def verify_sign(cls, data: str, signature: str) -> bool:
        """
        验证数据签名
        
        参数:
            data: 原始数据
            signature: 签名
        
        返回:
            是否验证通过
        """
        expected = cls.sign(data)
        return expected == signature
    
    @classmethod
    def hash_data(cls, data: str) -> str:
        """
        哈希数据
        
        参数:
            data: 原始数据
        
        返回:
            哈希值（SHA256）
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    @classmethod
    def generate_random_key(cls, length: int = 32) -> str:
        """
        生成随机密钥
        
        参数:
            length: 密钥长度
        
        返回:
            随机密钥（十六进制）
        """
        return os.urandom(length).hex()


if __name__ == "__main__":
    print("测试加密工具...")
    
    test_data = "Hello, World! 你好，世界！"
    
    encrypted = CryptoUtils.encrypt(test_data)
    print(f"加密后: {encrypted}")
    
    decrypted = CryptoUtils.decrypt(encrypted)
    print(f"解密后: {decrypted}")
    
    assert test_data == decrypted, "加密解密测试失败"
    
    signature = CryptoUtils.sign(test_data)
    print(f"签名: {signature}")
    
    assert CryptoUtils.verify_sign(test_data, signature), "签名验证测试失败"
    
    print("测试通过!")
