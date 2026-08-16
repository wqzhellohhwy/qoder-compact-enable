# -*- coding: utf-8 -*-
"""验证 compact patch 结果。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

OLDS = [
    "const c=(0,uin.useMemo)(()=>s||t<iDa,[t,s])",
    "const c=(0,ZBn.useMemo)(()=>s||t<oyu,[t,s])",
    "const c=(0,qqn.useMemo)(()=>s||t<kHu,[t,s])",
]
NEWS = [
    "const c=(0,uin.useMemo)(()=>s,[t,s])",
    "const c=(0,ZBn.useMemo)(()=>s,[t,s])",
    "const c=(0,qqn.useMemo)(()=>s,[t,s])",
]

out = []
for i, (o, n) in enumerate(zip(OLDS, NEWS), 1):
    out.append(f"副本{i}: OLD={data.count(o)} 次, NEW={data.count(n)} 次")

# 确认阈值常量定义仍在（不应改动）
for name in ["nDa=64,iDa=40", "iyu=64,oyu=40", "SHu=64,kHu=40"]:
    out.append(f"常量 {name}: {data.count(name)} 次")

# 确认整体无其他 t<iDa/t<oyu/t<kHu 残留（tooltip 里的条件表达式应还在，因为没改）
out.append(f"t<iDa 残留: {len(re.findall(r't<iDa', data))}")
out.append(f"t<oyu 残留: {len(re.findall(r't<oyu', data))}")
out.append(f"t<kHu 残留: {len(re.findall(r't<kHu', data))}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_verify_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
