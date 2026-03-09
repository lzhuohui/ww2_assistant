# 前端配置目录

本目录存放前端项目的配置文件。

## 文件说明

### requirements.txt

Python依赖列表，包含项目运行所需的所有Python包。

**使用方法：**
```bash
# 安装依赖
pip install -r requirements.txt

# 更新依赖
pip freeze > requirements.txt
```

### activate_env.bat

虚拟环境激活脚本，用于快速激活项目的Python虚拟环境。

**使用方法：**
```bash
# 在项目根目录下执行
前端/配置/activate_env.bat
```

**脚本功能：**
1. 激活虚拟环境 (`venv\Scripts\activate.bat`)
2. 显示当前Python版本
3. 提示虚拟环境已激活

## 依赖列表

| 包名 | 版本 | 用途 |
|------|------|------|
| flet | 0.82.0 | Flet框架 |
| httpx | 0.28.1 | HTTP客户端 |
| msgpack | 1.1.2 | 消息序列化 |
| oauthlib | 3.3.1 | OAuth库 |
| repath | 0.9.0 | 路径处理 |
| anyio | 4.12.1 | 异步I/O |
| certifi | 2026.2.25 | SSL证书 |
| h11 | 0.16.0 | HTTP/1.1协议 |
| httpcore | 1.0.9 | HTTP核心库 |
| idna | 3.11 | 国际化域名 |
| six | 1.17.0 | Python 2/3兼容 |
| typing_extensions | 4.15.0 | 类型扩展 |

## 注意事项

1. 修改依赖后请及时更新`requirements.txt`
2. 激活虚拟环境后再运行前端应用
3. 确保所有依赖包版本兼容
