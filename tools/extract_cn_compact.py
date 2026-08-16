# -*- coding: utf-8 -*-
"""搜索 unicode 转义形式的压缩相关文案（\\u538b\\u7f29 = 压缩）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 压缩 = \u538b\u7f29
m = re.findall(r"\\u538b\\u7f29", data)
out.append(f"'压缩'(转义) 出现次数: {len(m)}")

# 上下文
shown = 0
for mm in re.finditer(r"\\u538b\\u7f29", data):
    s = max(0, mm.start() - 300)
    e = min(len(data), mm.end() + 300)
    out.append(f"\n--- @{mm.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 12:
        break
out.append(f"\n(仅显示前 {shown} 个)")

# 也搜 "summarize conversation" / "compact conversation" 等
out.append("\n" + "=" * 80)
for kw in ["conversation", "context", "history"]:
    for pat in [rf"compact[^,;]{{0,40}}{kw}", rf"{kw}[^,;]{{0,40}}compact"]:
        ms = re.findall(pat, data, re.IGNORECASE)
        if ms:
            out.append(f"\n{pat}: {len(ms)} 个, 例如: {ms[:3]}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cn_compact.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
