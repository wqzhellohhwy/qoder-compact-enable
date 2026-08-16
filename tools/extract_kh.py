# -*- coding: utf-8 -*-
"""查找副本3 常量定义：kHu/SHu 及周边。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
for name in ["kHu", "SHu"]:
    ms = list(re.finditer(rf"(?<![A-Za-z0-9_]){name}\s*=\s*([0-9.e]+)", data))
    out.append(f"{name} 定义: {len(ms)} 个")
    for m in ms[:3]:
        s = max(0, m.start() - 250)
        e = min(len(data), m.end() + 250)
        out.append(f"\n--- @{m.start()} ---")
        out.append(data[s:e])
    # 也找 useMemo 中引用
    ms2 = list(re.finditer(rf"t<{name}", data))
    out.append(f"{name} 使用: {len(ms2)} 个")
    for m in ms2:
        out.append(f"  @{m.start()}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_kh_defs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
