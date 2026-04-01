# -*- coding: utf-8 -*-
import re

# 读取文件
with open('前端/配置/V2/界面配置.json', 'r', encoding='utf-8') as f:
    content = f.read()

# 将多行options改为一行格式
pattern = r'"options": \[\s+((?:"[^"]+",?\s+)+)\]'

def replace_options(match):
    options_text = match.group(1)
    options = re.findall(r'"([^"]+)"', options_text)
    return '"options": ["' + '", "'.join(options) + '"]'

new_content = re.sub(pattern, replace_options, content)

# 保存文件
with open('前端/配置/V2/界面配置.json', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('已将所有options改为一行格式')
