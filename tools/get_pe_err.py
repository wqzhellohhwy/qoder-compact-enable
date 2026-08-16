# -*- coding: utf-8 -*-
"""获取 P-E 段 node 检查的完整错误。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"
r = subprocess.run(["node", "--check", os.path.join(wd, "_t_pe_full.js")], capture_output=True, text=True)
print("exit:", r.returncode)
print("STDERR:", r.stderr[-600:])
