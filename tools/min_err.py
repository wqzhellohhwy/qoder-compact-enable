# -*- coding: utf-8 -*-
"""打印 _t_min.js 完整错误。"""
import subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

r = subprocess.run(["node", r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_min.js"], capture_output=True, text=True)
print("exit:", r.returncode)
print("=== STDERR 全文 ===")
print(r.stderr)
