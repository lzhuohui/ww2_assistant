# -*- coding: utf-8 -*-
"""文档代码示例检查器 | 检查文档中的代码示例是否符合规范 | 模块隔离原则"""
import re
import sys
from pathlib import Path

# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************

class DocCodeChecker:
    """文档代码示例检查器"""
    
    @staticmethod
    def check_file(file_path: str) -> dict:
        """检查文件中的代码示例
        
        Args:
            file_path: 要检查的文档路径
        
        Returns:
            dict: 检查结果
        """
        results = {
            "file": file_path,
            "total_blocks": 0,
            "issues": [],
            "passed": True
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取Python代码块
        code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
        results["total_blocks"] = len(code_blocks)
        
        for i, code in enumerate(code_blocks, 1):
            block_issues = DocCodeChecker._check_code_block(code, i)
            if block_issues:
                results["issues"].extend(block_issues)
                results["passed"] = False
        
        return results
    
    @staticmethod
    def _check_code_block(code: str, block_num: int) -> list:
        """检查单个代码块"""
        issues = []
        
        # 检查1：是否有文件头
        if not code.strip().startswith('# -*- coding: utf-8 -*-'):
            # 如果是示例代码片段，可以跳过此检查
            if 'class' in code or 'def' in code:
                if '# -*- coding: utf-8 -*-' not in code:
                    issues.append({
                        "block": block_num,
                        "type": "文件头",
                        "message": "缺少编码声明：# -*- coding: utf-8 -*-",
                        "severity": "warning"
                    })
        
        # 检查2：是否有用户变量区域
        if 'class' in code and '# *** 用户指定变量' not in code:
            issues.append({
                "block": block_num,
                "type": "用户变量",
                "message": "缺少用户指定变量区域",
                "severity": "error"
            })
        
        # 检查3：调试逻辑是否符合标准
        if '__main__' in code:
            if 'def main(page):' in code or 'page.title' in code:
                issues.append({
                    "block": block_num,
                    "type": "调试逻辑",
                    "message": "调试逻辑不符合标准：使用了自定义main函数或设置页面属性",
                    "severity": "error"
                })
            
            # 检查是否使用标准格式
            if 'ft.run(lambda page: page.add' not in code:
                issues.append({
                    "block": block_num,
                    "type": "调试逻辑",
                    "message": "调试逻辑应使用标准格式：ft.run(lambda page: page.add(...))",
                    "severity": "warning"
                })
        
        # 检查4：函数参数是否有默认值
        func_pattern = r'def\s+\w+\s*\(([^)]*)\)'
        func_matches = re.findall(func_pattern, code)
        for params in func_matches:
            if params.strip() and '=' not in params:
                # 排除self和cls参数
                param_list = [p.strip() for p in params.split(',')]
                for param in param_list:
                    if param not in ['self', 'cls'] and ':' not in param:
                        issues.append({
                            "block": block_num,
                            "type": "函数参数",
                            "message": f"参数缺少默认值和类型注解：{param}",
                            "severity": "warning"
                        })
        
        return issues
    
    @staticmethod
    def print_report(results: dict):
        """打印检查报告"""
        print(f"\n{'='*60}")
        print(f"文档代码示例检查报告")
        print(f"{'='*60}")
        print(f"检查文件：{results['file']}")
        print(f"代码块数量：{results['total_blocks']}")
        print(f"检查结果：{'✅ 通过' if results['passed'] else '❌ 未通过'}")
        
        if results['issues']:
            print(f"\n发现问题：{len(results['issues'])}个")
            print(f"{'-'*60}")
            
            for issue in results['issues']:
                severity_icon = "🔴" if issue['severity'] == 'error' else "🟡"
                print(f"{severity_icon} 代码块 #{issue['block']} - {issue['type']}")
                print(f"   问题：{issue['message']}")
                print()
        else:
            print("\n✅ 所有代码示例符合规范")
        
        print(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python doc-code-checker.py <文档路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    results = DocCodeChecker.check_file(file_path)
    DocCodeChecker.print_report(results)
    
    sys.exit(0 if results['passed'] else 1)
