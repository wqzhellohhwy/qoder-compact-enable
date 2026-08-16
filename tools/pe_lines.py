# -*- coding: utf-8 -*-
"""查看 _t_pe_run.js 的行结构与第 17 行内容。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_run.js", encoding="utf-8").read()
lines = d.split("\n")
print("总行数:", len(lines))
for i, ln in enumerate(lines[:20]):
    print(f"[{i}] len={len(ln)}: {repr(ln[:80])}")
