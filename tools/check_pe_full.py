# -*- coding: utf-8 -*-
"""提取副本完整 P-E 段单独验证 node 语法。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"
copy = os.path.join(wd, "_test_enhance_copy.js")
data = open(copy, encoding="utf-8", errors="replace").read()

i = data.find("try{/* P-E start */")
# N 函数结束：依赖数组 },[e,h,d 前
j = data.find("},[e,h,d", i)
print("start:", i, "end:", j, "len:", j - i)
seg = data[i : j]
print("seg repr head:", repr(seg[:200]))

seg_file = os.path.join(wd, "_t_pe_full.js")
with open(seg_file, "w", encoding="utf-8", newline="") as f:
    f.write("async function __t(){ " + seg + " }")
r = subprocess.run(["node", "--check", seg_file], capture_output=True, text=True)
print("full P-E: exit=", r.returncode)
print("err:", r.stderr.strip()[:400])

# 单独验证 content 字段字符串
k = seg.find('content:"You are a professional')
seg2 = seg[k : k + 400]
print("\ncontent 字段 repr:", repr(seg2[:300]))
