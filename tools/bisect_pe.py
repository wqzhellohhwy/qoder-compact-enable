# -*- coding: utf-8 -*-
"""二分定位第 17 行语法错误区间。"""
import subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_run.js", encoding="utf-8").read()
line = d.split("\n")[16]
print("行长度:", len(line))

def check(seg):
    src = "async function main(){" + seg + "\n}"
    tf = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_bin.js"
    with open(tf, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    r = subprocess.run(["node", "--check", tf], capture_output=True, text=True)
    return r.returncode == 0

print("整行 OK:", check(line))

# 二分：找出最小错误区间（前缀扩展法）
bad_start = None
for cut in range(0, len(line) + 1, 200):
    seg = line[:cut]
    if not check(seg):
        bad_start = cut
        break
print("首个失败前缀长度:", bad_start)

if bad_start:
    for cut in range(max(0, bad_start - 200), bad_start + 1):
        seg = line[:cut]
        if not check(seg):
            print("精确失败点:", cut)
            print("上下文:", repr(line[max(0, cut - 60): cut + 40]))
            break
