#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复Gitee构建问题
"""

import webbrowser
import sys

def open_gitee_actions():
    """打开Gitee Actions页面"""
    urls = {
        "仓库主页": "https://gitee.com/lzhuohui/ww2_assistant",
        "流水线页面": "https://gitee.com/lzhuohui/ww2_assistant/pipelines",
        "Actions页面": "https://gitee.com/lzhuohui/ww2_assistant/actions",
        "设置页面": "https://gitee.com/lzhuohui/ww2_assistant/settings"
    }
    
    print("=" * 70)
    print("Gitee构建问题快速修复")
    print("=" * 70)
    
    print("\n✅ 已完成的修复:")
    print("1. 修复了有问题的合并提交")
    print("2. 创建了Gitee专用工作流")
    print("3. 推送到Gitee仓库")
    print("4. 修复了构建产物命名问题")
    
    print("\n🚀 立即操作:")
    print("请按顺序完成以下步骤:")
    
    print("\n步骤1: 开启Gitee流水线功能（如果未开启）")
    print("1. 访问: https://gitee.com/lzhuohui/ww2_assistant/settings")
    print("2. 找到'功能设置' -> '流水线'")
    print("3. 开启流水线功能")
    print("4. 点击保存")
    
    print("\n步骤2: 手动触发新工作流")
    print("1. 访问: https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    print("2. 找到'Build APK for Gitee'工作流")
    print("3. 点击'运行流水线'")
    print("4. 选择master分支")
    print("5. 点击'运行'")
    
    print("\n步骤3: 监控构建进度")
    print("1. 点击正在运行的流水线")
    print("2. 查看实时构建日志")
    print("3. 等待构建完成（15-30分钟）")
    
    print("\n步骤4: 下载APK")
    print("构建成功后，下载:")
    print("• WW2Assistant-APK - 包含APK的ZIP文件")
    print("• 或 APK-Files - 单独的APK文件")
    
    print("\n🔧 新工作流的特点:")
    print("• 明确的构建产物名称（不再是'备份'）")
    print("• 创建ww2-assistant-apk.zip文件")
    print("• 上传详细的构建日志")
    print("• 支持Gitee的流水线系统")
    
    # 询问是否打开网页
    print("\n是否要打开相关页面？ (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            print("\n正在打开页面...")
            webbrowser.open("https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    except:
        print("\n你可以手动访问: https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    
    print("\n" + "=" * 70)
    print("如果构建仍然失败:")
    print("1. 查看构建日志获取详细错误信息")
    print("2. 运行本地构建: python local_build_alternative.py")
    print("3. 或联系获取进一步帮助")
    print("=" * 70)
    
    return True

def main():
    """主函数"""
    open_gitee_actions()
    return 0

if __name__ == "__main__":
    sys.exit(main())