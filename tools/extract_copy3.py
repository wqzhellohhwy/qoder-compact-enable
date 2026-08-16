# -*- coding: utf-8 -*-
"""提取副本3（@40800000-@40830000）的压缩逻辑与常量。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 副本3 区域
seg = data[40770000:40830000]

# 找 overlay 组件禁用条件：useMemo(()=>s||t<XXX,
m = re.search(r"useMemo\)\(\(\)=>s\|\|t<(\w+),\[t,s\]\)", seg)
out.append(f"副本3 禁用条件: {m.group(0) if m else '未找到'}")
if m:
    out.append(f"阈值变量: {m.group(1)}")

# 找该区域所有 var 常量定义（类似 var aaa=64,bbb=40,...）
for mm in re.finditer(r"var (\w+)=(\d+),(\w+)=(\d+),(\w+)=([\d.e]+),(\w+)=([\d.e]+)", seg):
    out.append(f"常量组: {mm.group(0)}")

# 找函数结构
for name in ["percentage", "useMemo)(()=>s||"]:
    for mm in re.finditer(re.escape(name), seg):
        s = max(0, mm.start() - 100)
        e = min(len(seg), mm.end() + 150)
        out.append(f"\n--- {name} @seg{mm.start()} ---")
        out.append(seg[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_copy3.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
