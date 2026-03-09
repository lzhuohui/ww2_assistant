import os

rules_dir = r"c:\Users\chmm1\Documents\二战风云\.trae\rules"
files = sorted([f for f in os.listdir(rules_dir) if f.endswith('.md')])

print("=" * 80)
print("规则文件字符数统计")
print("=" * 80)

total_chars = 0
for filename in files:
    filepath = os.path.join(rules_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        char_count = len(content)
        total_chars += char_count
        status = "✅" if char_count <= 1000 else "❌"
        print(f"{status} {filename:30s} {char_count:5d} 字符")

print("=" * 80)
print(f"总计: {len(files)} 个文件, {total_chars} 字符")
print("=" * 80)
