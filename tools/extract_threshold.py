# -*- coding: utf-8 -*-
"""搜索 contextThreshold 与 compact conversation 相关上下文。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) contextThreshold 出现次数与上下文
ms = list(re.finditer(r"contextThreshold", data, re.IGNORECASE))
out.append(f"contextThreshold 出现次数: {len(ms)}")
for i, m in enumerate(ms):
    s = max(0, m.start() - 400)
    e = min(len(data), m.end() + 400)
    out.append(f"\n--- [{i}] @{m.start()} ---")
    out.append(data[s:e])

# 2) "conversation is still short" 上下文
out.append("\n" + "=" * 80)
ms = list(re.finditer(r"still short", data, re.IGNORECASE))
out.append(f"'still short' 出现次数: {len(ms)}")
for i, m in enumerate(ms):
    s = max(0, m.start() - 400)
    e = min(len(data), m.end() + 400)
    out.append(f"\n--- [{i}] @{m.start()} ---")
    out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_threshold_ctx.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
