# Gitee Actions（流水线）开启指南

## 当前状态
✅ 仓库已成功推送到Gitee：`https://gitee.com/lzhuohui/ww2_assistant`
⚠️ Actions功能需要手动开启（返回404状态码）

## 开启步骤

### 步骤1：登录Gitee并访问仓库
1. 打开浏览器访问：**https://gitee.com/lzhuohui/ww2_assistant**
2. 使用你的账号登录（lzhuohui）

### 步骤2：开启流水线功能
1. 进入仓库后，点击右上角的 **"管理"** 按钮
2. 在左侧菜单中找到 **"功能设置"**
3. 找到 **"流水线"** 选项
4. 勾选 **"开启流水线功能"**
5. 点击保存

### 步骤3：配置流水线（可选）
Gitee流水线需要配置文件，我们已经准备好了：
- 配置文件位置：`.github/workflows/build-apk.yml`
- Gitee会自动识别这个文件

### 步骤4：手动触发构建
开启流水线功能后：
1. 点击顶部的 **"流水线"** 标签
2. 你会看到 **"Build APK"** 工作流
3. 点击 **"运行流水线"** 按钮
4. 选择分支（默认master）
5. 点击 **"运行"**

## 备选方案

### 方案A：使用GitHub Actions（如果网络允许）
如果你可以访问GitHub：
1. 将远程仓库改回GitHub：
   ```bash
   git remote set-url origin https://github.com/lzhuohui/ww2_assistant.git
   git push origin master
   ```
2. 访问：**https://github.com/lzhuohui/ww2_assistant/actions**

### 方案B：本地构建脚本
如果云端构建有问题，可以使用我们创建的本地测试脚本：
```bash
python github_build_test.py
```

## 常见问题

### Q1: Gitee流水线为什么是404？
A: Gitee的CI/CD功能默认是关闭的，需要手动开启。

### Q2: 开启后还是看不到流水线？
A: 需要等待几分钟，或者尝试重新推送代码：
```bash
git add .
git commit -m "开启流水线功能"
git push gitee master
```

### Q3: 流水线运行失败怎么办？
A: 检查以下可能的问题：
1. Flutter环境配置
2. Android SDK许可
3. 依赖包安装
4. 查看流水线日志获取具体错误信息

### Q4: 如何下载构建好的APK？
A: 流水线运行成功后：
1. 点击完成的工作流
2. 在 **"制品"** 或 **"Artifacts"** 部分
3. 下载 `ww2-assistant-apk.zip`

## 即时操作建议

1. **立即操作**：登录Gitee开启流水线功能
2. **备用方案**：如果Gitee不行，改回GitHub
3. **本地测试**：运行 `python github_build_test.py` 验证环境

## 联系我们
如果有任何问题，请查看流水线运行日志或联系技术支持。