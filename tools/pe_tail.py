# -*- coding: utf-8 -*-
"""打印 P-E 段尾部内容。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_full.js"
d = open(p, encoding="utf-8", errors="replace").read()
print("段长度:", len(d))
print("段尾 300 字符 repr:")
print(repr(d[-300:]))
