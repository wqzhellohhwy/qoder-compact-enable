# -*- coding: utf-8 -*-
"""定位 node 错误的精确列号。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"
r = subprocess.run(["node", "--check", os.path.join(wd, "_t_pe_full.js")], capture_output=True, text=True)
lines = r.stderr.split("\n")
print("总行数:", len(lines))
for i, ln in enumerate(lines[:6]):
    print(f"[{i}] len={len(ln)} {ln[:100]!r}")
# 找 ^ 标记行
for i, ln in enumerate(lines):
    if "^" in ln:
        col = ln.index("^")
        print(f"^ 标记在第 {i} 行, 列 {col}")
        # 源码行
        src = lines[i - 1]
        print("源码上下文:", repr(src[max(0, col - 60): col + 60]))
        break
