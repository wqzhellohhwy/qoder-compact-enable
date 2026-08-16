# -*- coding: utf-8 -*-
"""定位优化输入按钮禁用条件的所有副本（<3 字符 / >1000 字符）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) 所有副本的 z / $ 定义模式：e.length>XXX 与 trim().length<3
ms = list(re.finditer(r"e\.length>\w+,\[e\]\)", data))
out.append(f"e.length>XXX 禁用(>$): {len(ms)} 处")
for m in ms:
    s = max(0, m.start() - 200)
    e = min(len(data), m.end() + 120)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

ms2 = list(re.finditer(r"trim\(\)\.length<3", data))
out.append(f"\n\ntrim().length<3 禁用(z): {len(ms2)} 处")
for m in ms2:
    s = max(0, m.start() - 250)
    e = min(len(data), m.end() + 100)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# 2) z5p 常量定义
ms3 = list(re.finditer(r"\w{1,4}=\d{3,4},V\w{1,4}=t=>\{", data))
out.append(f"\n\n增强组件常量组: {len(ms3)} 处")
for m in ms3:
    s = max(0, m.start() - 60)
    e = min(len(data), m.end() + 60)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_v5p_all.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
