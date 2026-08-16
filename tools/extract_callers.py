# -*- coding: utf-8 -*-
"""搜索 compressContext/compressChat 所有调用点 + 其他压缩入口。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# compressContext 调用点
ms = list(re.finditer(r"compressContext", data))
out.append(f"compressContext 出现: {len(ms)}")
for m in ms:
    s = max(0, m.start() - 150)
    e = min(len(data), m.end() + 150)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# compressChat / compact command
ms = list(re.finditer(r"compressChat", data))
out.append(f"\ncompressChat 出现: {len(ms)}")
for m in ms[:5]:
    s = max(0, m.start() - 150)
    e = min(len(data), m.end() + 150)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# 命令注册：包含 compact 的 command id（如 aicoding.chat.compact）
out.append("\n" + "=" * 80)
ms = list(re.finditer(r"[A-Za-z0-9_.-]*compact[A-Za-z0-9_.-]*", data))
from collections import Counter
c = Counter(m.group(0) for m in ms)
for w, n in c.most_common(30):
    out.append(f"{w}: {n}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_callers.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
