# -*- coding: utf-8 -*-
"""确认 ICustomModelService 注入名 / fetchBYOKConfig 方法 / provider base_url 字段。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) ICustomModelService 服务 id
for m in list(re.finditer(r"[A-Za-z_$]+=vn\(\"customModelService\"\)", data))[:3]:
    s = max(0, m.start() - 100)
    e = min(len(data), m.end() + 100)
    out.append(f"\n--- customModelService 注入名 @{m.start()} ---")
    out.append(data[s:e])

# 2) fetchBYOKConfig 定义
m = re.search(r"async fetchBYOKConfig\([^)]*\)\{", data)
if m:
    out.append(f"\n===== fetchBYOKConfig @{m.start()} =====")
    out.append(data[m.start():m.start()+800])

# 3) BYOK provider 的 base_url 字段（客户端）
for m in list(re.finditer(r"base_url", data))[:12]:
    s = max(0, m.start() - 120)
    e = min(len(data), m.end() + 120)
    out.append(f"\n--- base_url @{m.start()} ---")
    out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_svc.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
