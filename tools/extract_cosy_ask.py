# -*- coding: utf-8 -*-
"""提取 cosy 中 AskParams/CustomModelExtra/custom_model 结构字段与上下文。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

strs = []
for m in re.finditer(rb"[\x20-\x7e]{6,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))
print("strings:", len(strs))

out = []

# 1) custom_model / customModel 的 json tag 及相邻字段
out.append("===== customModel 相关 json tag =====")
for i, (off, s) in enumerate(strs):
    if re.search(r"json:\"(custom_model|customModel)", s):
        out.append(f"\n--- [{off}] {s[:200]}")
        for j in range(max(0, i - 8), min(len(strs), i + 9)):
            out.append(f"  [{strs[j][0]}] {strs[j][1][:140]}")

# 2) AskParams 结构字段
out.append("\n===== AskParams 结构 =====")
for off, s in strs:
    if "AskParams" in s and len(s) < 200:
        out.append(f"  [{off}] {s}")

# 3) meta 相关字段（_meta 在 cosy 侧的解析）
out.append("\n===== meta/custom 处理 =====")
for off, s in strs:
    if re.search(r"json:\"(meta|customModelExtra|modelConfig|byok)", s, re.IGNORECASE) and len(s) < 200:
        out.append(f"  [{off}] {s}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_ask.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
