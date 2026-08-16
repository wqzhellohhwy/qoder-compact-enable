# -*- coding: utf-8 -*-
"""查找压缩阈值常量定义：iDa/nDa/oyu/iyu/A5p/D5p。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
for name in ["iDa", "nDa", "oyu", "iyu", "A5p", "D5p", "Gdv", "Kdv"]:
    # 定义模式: name=数字 或 var name=... 或 name=数字,
    pats = [
        rf"(?:var|let|const)\s+{name}\s*=\s*([0-9.]+)",
        rf"(?<![A-Za-z0-9_]){name}\s*=\s*([0-9.]+)",
        rf"(?<![A-Za-z0-9_]){name}\s*=\s*([A-Za-z0-9_$]+)",
    ]
    found = False
    for p in pats:
        ms = list(re.finditer(p, data))
        if ms:
            found = True
            for m in ms[:5]:
                s = max(0, m.start() - 200)
                e = min(len(data), m.end() + 200)
                out.append(f"\n--- {name} @{m.start()} ({p[:40]}...) ---")
                out.append(data[s:e])
    if not found:
        out.append(f"\n{name}: 未找到定义")
    out.append("")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_const_defs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
