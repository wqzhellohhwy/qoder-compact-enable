# -*- coding: utf-8 -*-
"""搜索 compact 相关精确关键词。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

with open(F, "r", encoding="utf-8", errors="replace") as fp:
    data = fp.read()

out = []
patterns = [
    r"compact[A-Za-z]*",
    r"[Cc]ompact(?:ion|ing|ed)?\b",
]
# 统计各种 compact 驼峰组合
words = re.findall(r"compact[A-Za-z]*", data)
from collections import Counter
c = Counter(words)
for w, n in c.most_common(40):
    out.append(f"{w}: {n}")

# 搜索 "compact" 作为字符串常量（引号包裹）
out.append("\n" + "=" * 80)
out.append('引号内的 "compact" 上下文（前 10 个）:')
shown = 0
for m in re.finditer(r'["\'][^"\']*compact[^"\']*["\']', data, re.IGNORECASE):
    s = max(0, m.start() - 150)
    e = min(len(data), m.end() + 150)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 10:
        break
out.append(f"\n(仅显示前 {shown} 个)")

# 搜索 percent 相关逻辑: .percent >= X
out.append("\n" + "=" * 80)
out.append(".percent 相关上下文（前 20 个）:")
shown = 0
for m in re.finditer(r"\.percent\s*[<>=!]+\s*[0-9.]", data):
    s = max(0, m.start() - 150)
    e = min(len(data), m.end() + 150)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 20:
        break
out.append(f"\n(仅显示前 {shown} 个)")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_compact_words.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
