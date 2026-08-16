# -*- coding: utf-8 -*-
"""打印 _t_pe_run.js 的完整 node 错误。"""
import subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

r = subprocess.run(["node", r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_run.js"], capture_output=True, text=True)
err = r.stderr
# 错误格式：文件:行\n源码\n^^^\n消息
lines = err.split("\n")
for i, ln in enumerate(lines[:8]):
    print(f"[{i}] len={len(ln)}")
    if "^" in ln:
        col = ln.index("^")
        print(f"    列={col} 上下文={repr(lines[i-1][max(0,col-40):col+40])}")
    elif ln.strip() and "at " not in ln and "Node.js" not in ln:
        print(f"    消息: {ln[:150]}")
