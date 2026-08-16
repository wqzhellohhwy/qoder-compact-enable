# -*- coding: utf-8 -*-
"""在 workbench.desktop.main.js 中搜索压缩相关关键词。"""
import re, os

F = r"C:\Program Files\Qoder\resources\app\out\vs\workbench\workbench.desktop.main.js"
print("size MB:", round(os.path.getsize(F) / 1024 / 1024, 1))
data = open(F, encoding="utf-8", errors="replace").read()

out = []
for kw in ["压缩", "compact", "summariz", "condens", "truncat", "contextLimit", "tokenLimit", "maxContext"]:
    n = len(re.findall(kw, data, re.IGNORECASE))
    out.append(f"{kw}: {n}")

# 中文压缩相关文案（\u538b\u7f29 = 压缩）
m_cn = re.findall(r".{0,60}\u538b\u7f29.{0,60}", data)
out.append(f"\n中文'压缩'出现: {len(m_cn)}")
for i, x in enumerate(m_cn[:10]):
    out.append(f"\n[{i}] {x}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_wb_scan.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
