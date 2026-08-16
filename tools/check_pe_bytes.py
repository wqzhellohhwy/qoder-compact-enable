# -*- coding: utf-8 -*-
"""精确检查副本 P-E 代码区域的真实字节（是否有裸换行）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_test_enhance_copy.js"
d = open(p, encoding="utf-8", errors="replace").read()

i = d.find("not sure")
seg = d[i : i + 120]
print("=== repr ===")
print(repr(seg))
print("=== 字节级 ===")
for ch in seg:
    if ch == "\n":
        print("<LF>", end="")
    elif ch == "\r":
        print("<CR>", end="")
    else:
        print(ch, end="")
print()
