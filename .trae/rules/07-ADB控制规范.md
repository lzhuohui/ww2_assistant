---
name: 07-ADB控制规范
description: 适用于ADB设备交互的专用规则
globs: ["core/adb/**/*.py", "**/adb_client.py"]
---

# ADB控制规范

## 封装要求
- 所有ADB命令封装在`AdbClient`类中
- 提供统一执行接口，包含错误处理

## 连接管理
- 必须包含连接状态管理
- 自动重连机制（最多3次，指数退避）
- 断线检测和恢复

```python
class AdbClient:
    def execute(self, cmd, retry=3):
        for i in range(retry):
            try:
                return subprocess.run(cmd, timeout=10, check=True)
            except (TimeoutExpired, CalledProcessError):
                if i == retry-1: raise
                time.sleep(2 ** i)
```

## 命令超时
- 所有命令设置超时（默认10秒）
- 截图等操作可适当延长
- 超时后重试或降级

## 资源释放
- 截图后及时释放内存
- 退出时断开连接
