# -*- coding: utf-8 -*-
"""搜索压缩功能相关中文文案与 condens/summariz 上下文。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

with open(F, "r", encoding="utf-8", errors="replace") as fp:
    data = fp.read()

out = []

# 1) 中文"压缩"出现次数
n_cn = len(re.findall("压缩", data))
out.append(f"中文'压缩'出现次数: {n_cn}")
n_cn2 = len(re.findall("压缩对话", data))
out.append(f"中文'压缩对话'出现次数: {n_cn2}")

# 2) 中文"压缩"上下文片段（最多 15 个，每个前后 200 字符）
out.append("\n" + "=" * 80)
out.append("中文'压缩'上下文:")
shown = 0
for m in re.finditer("压缩", data):
    s = max(0, m.start() - 200)
    e = min(len(data), m.end() + 200)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 15:
        break
out.append(f"\n(仅显示前 {shown} 个)")

# 3) condens 上下文（最多 10 个）
out.append("\n" + "=" * 80)
out.append("condens 上下文:")
shown = 0
for m in re.finditer(r"condens", data, re.IGNORECASE):
    s = max(0, m.start() - 200)
    e = min(len(data), m.end() + 200)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 10:
        break
out.append(f"\n(仅显示前 {shown} 个)")

# 4) summarize 上下文（最多 10 个）
out.append("\n" + "=" * 80)
out.append("summariz 上下文:")
shown = 0
for m in re.finditer(r"summariz", data, re.IGNORECASE):
    s = max(0, m.start() - 200)
    e = min(len(data), m.end() + 200)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])
    shown += 1
    if shown >= 10:
        break
out.append(f"\n(仅显示前 {shown} 个)")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_compact_ctx.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
