# -*- coding: utf-8 -*-
"""提取 agents-window.desktop.main.js 中 usagePercent/compress 相关上下文片段。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

with open(F, "r", encoding="utf-8", errors="replace") as fp:
    data = fp.read()

# 1) usagePercent 全部上下文
out = []
out.append("=" * 80)
out.append("usagePercent contexts:")
for m in re.finditer(r"usagepercent", data, re.IGNORECASE):
    s = max(0, m.start() - 250)
    e = min(len(data), m.end() + 250)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_usage_percent_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
