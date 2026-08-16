# -*- coding: utf-8 -*-
"""提取 vwa 完整定义（customModel 对象结构）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
m = re.search(r"function vwa\(t,e\)\{", data)
if m:
    out.append(f"===== vwa @{m.start()} =====")
    out.append(data[m.start():m.start()+1500])
else:
    out.append("vwa 未找到")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_vwa.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
