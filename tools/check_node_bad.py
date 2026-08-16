# -*- coding: utf-8 -*-
"""验证 node --check 对裸换行字符串的行为 + 副本 P-E 片段。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"

# 1) 裸换行双引号字符串
bad = os.path.join(wd, "_t_bad.js")
with open(bad, "w", encoding="utf-8", newline="") as f:
    f.write('const x = "abc\ndef";\n')
r1 = subprocess.run(["node", "--check", bad], capture_output=True, text=True)
print("bad: exit=", r1.returncode, "| err:", r1.stderr.strip()[:120])

# 2) 正确转义
ok = os.path.join(wd, "_t_ok.js")
with open(ok, "w", encoding="utf-8", newline="") as f:
    f.write('const x = "abc\\ndef";\n')
r2 = subprocess.run(["node", "--check", ok], capture_output=True, text=True)
print("ok:  exit=", r2.returncode, "| err:", r2.stderr.strip()[:120])

# 3) 副本文件整体
copy = os.path.join(wd, "_test_enhance_copy.js")
r3 = subprocess.run(["node", "--check", copy], capture_output=True, text=True)
print("copy: exit=", r3.returncode, "| err:", r3.stderr.strip()[:200])

# 4) 从副本提取 P-E 片段（前后 100 字符）生成独立文件测试
data = open(copy, encoding="utf-8", errors="replace").read()
i = data.find("P-E start")
seg = data[max(0, i - 50): i + 1500]
seg_file = os.path.join(wd, "_t_seg.js")
with open(seg_file, "w", encoding="utf-8", newline="") as f:
    f.write("try{" + seg.split("try{", 1)[1] if "try{" in seg else seg)
r4 = subprocess.run(["node", "--check", seg_file], capture_output=True, text=True)
print("seg: exit=", r4.returncode, "| err:", r4.stderr.strip()[:300])
