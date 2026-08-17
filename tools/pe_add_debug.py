# -*- coding: utf-8 -*-
"""P-E catch 加 L?.error 调试提示：更新 patch 脚本 + 真实文件。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

old = 'catch(err){console.warn("[P-E] local enhance failed, fallback:",err)}}'
new = 'catch(err){console.warn("[P-E] local enhance failed, fallback:",err);L?.error("[P-E] "+(err?.message||err))}}'

# 1) 更新 patch 脚本
P = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\patch_qoder_enhance.py"
d = open(P, encoding="utf-8").read()
print("脚本中旧片段出现:", d.count(old))
d2 = d.replace(old, new, 1)
open(P, "w", encoding="utf-8", newline="\n").write(d2)
print("脚本已更新")

# 2) 真实文件直接替换（3 处）
JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(JS, encoding="utf-8", errors="replace").read()
print("真实文件旧片段出现:", data.count(old))
data2 = data.replace(old, new)
open(JS, "w", encoding="utf-8", newline="").write(data2)
print("真实文件已更新")
