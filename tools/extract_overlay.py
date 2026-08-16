# -*- coding: utf-8 -*-
"""提取 overlay 组件与 R5p 组件的完整代码（副本1 @8707000-@8717000）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
out.append("===== 副本1 overlay+R5p 完整代码 (@8705000-@8718000) =====")
out.append(data[8705000:8718000])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_overlay_full.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
