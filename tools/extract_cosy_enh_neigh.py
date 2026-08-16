# -*- coding: utf-8 -*-
"""提取 EnhancePrompt 符号邻域的 cosy 函数符号（依赖模块线索）。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

strs = []
for m in re.finditer(rb"[\x20-\x7e]{6,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))

out = []

# EnhancePrompt 符号位置
for off, s in strs:
    if "EnhancePrompt" in s and "cosy/" in s:
        out.append(f"--- EnhancePrompt 符号 @{off}: {s}")
        # 打印该符号前后 60 个符号（函数符号，cosy/ 开头）
        for j in range(max(0, [x[0] for x in strs].index(off) - 1), min(len(strs), [x[0] for x in strs].index(off) + 2)):
            pass  # 简化：直接收集该偏移前后 200KB 内的 cosy 函数符号
        # 简化：统计偏移 67000000-67500000 内所有 cosy/ 函数符号
        break

out.append("\n===== 偏移 66.9M-67.6M 内 cosy 函数符号（EnhancePrompt 邻域） =====")
for off, s in strs:
    if 66900000 <= off <= 67600000 and s.startswith("cosy/") and "." in s:
        out.append(f"  [{off}] {s[:170]}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_enh_neigh.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
