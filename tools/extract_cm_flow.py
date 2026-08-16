# -*- coding: utf-8 -*-
"""提取 ChatSessionService 聊天请求构建代码（customModel 传递方式）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 找 applyCustomModelRuntimeFallback 定义
m = re.search(r"applyCustomModelRuntimeFallback\([^)]*\)\{", data)
if m:
    out.append(f"===== applyCustomModelRuntimeFallback @{m.start()} =====")
    out.append(data[m.start():m.start()+2000])

# 找 customModel= 赋值处（普通聊天）
for m in list(re.finditer(r"customModel=this\.applyCustomModelRuntimeFallback", data)):
    s = max(0, m.start() - 800)
    e = min(len(data), m.end() + 300)
    out.append(f"\n===== customModel 赋值 @{m.start()} =====")
    out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cm_flow.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
