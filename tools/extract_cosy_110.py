# -*- coding: utf-8 -*-
"""cosy 中 error.code 映射表与 prompt_enhance 日志上下文分析。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

strs = []
for m in re.finditer(rb"[\x20-\x7e]{6,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))
print("strings:", len(strs))

out = []

# 1) 所有 error.code.* 错误码映射
out.append("===== error.code 映射 =====")
for off, s in strs:
    if s.startswith("error.code."):
        out.append(f"  [{off}] {s[:250]}")

# 2) daily usage limit 上下文
out.append("\n===== daily usage limit 相邻 =====")
for i, (off, s) in enumerate(strs):
    if "daily usage limit" in s.lower() or "daily limit" in s.lower():
        out.append(f"\n--- [{off}] {s[:300]}")
        for j in range(max(0, i - 6), min(len(strs), i + 7)):
            out.append(f"  [{strs[j][0]}] {strs[j][1][:160]}")

# 3) [prompt_enhance] 完整日志
out.append("\n===== [prompt_enhance] 日志 =====")
for off, s in strs:
    if "[prompt_enhance]" in s:
        out.append(f"  [{off}] {s[:300]}")

# 4) EnhancePrompt 相关
out.append("\n===== EnhancePrompt / enhance 请求 =====")
for off, s in strs:
    if re.search(r"EnhancePrompt|enhancePrompt", s):
        out.append(f"  [{off}] {s[:250]}")

# 5) 本地 usage/计数存储线索
out.append("\n===== usage 计数相关 =====")
for off, s in strs:
    if re.search(r"(daily|today|date).*(usage|count|used)|(usage|count).*(daily|today)", s, re.IGNORECASE) and len(s) < 200:
        out.append(f"  [{off}] {s[:200]}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_110.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
