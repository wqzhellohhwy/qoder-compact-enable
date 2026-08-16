# -*- coding: utf-8 -*-
"""打印副本中 P-E 完整代码（含 try 前缀和 finally 结尾）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_test_enhance_copy.js", encoding="utf-8").read()
i = d.find("try{/* P-E start */")
j = d.find("},[e,h,d", i) + 1
pe = d[i:j]
print("P-E 长度:", len(pe))
print(repr(pe))
