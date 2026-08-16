# -*- coding: utf-8 -*-
"""检查副本 P-E 段的 \\n 字节状态。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_test_enhance_copy.js"
d = open(p, encoding="utf-8", errors="replace").read()

i = d.find("not sure")
seg = d[i - 20 : i + 160]
print("repr:", repr(seg))
print()
for ch in seg:
    if ch == "\n":
        print("<LF>", end="")
    elif ch == "\\":
        print("<BS>", end="")
    else:
        print(ch, end="")
print()
