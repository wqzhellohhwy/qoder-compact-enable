# -*- coding: utf-8 -*-
"""确认 cosy 中 quota/额度检查函数所属模块 + NoCreditError 上下文。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

strs = []
for m in re.finditer(rb"[\x20-\x7e]{6,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))
print("strings:", len(strs))

out = []

# 1) quota 相关函数符号（cosy/xxx.xxx 形式）
out.append("===== quota 函数符号 =====")
for off, s in strs:
    if re.search(r"^cosy/[\w/]+\.\w*(?:Quota|quota|Credit|credit|Usage|usage)\w*", s):
        out.append(f"  [{off}] {s[:180]}")

# 2) NoCreditError 上下文
out.append("\n===== NoCreditError 相邻 =====")
for i, (off, s) in enumerate(strs):
    if "NoCreditError" in s:
        out.append(f"\n--- [{off}] {s[:220]}")
        for j in range(max(0, i - 5), min(len(strs), i + 6)):
            out.append(f"  [{strs[j][0]}] {strs[j][1][:150]}")

# 3) computeQuotaState / QuotaInsufficient 相邻
out.append("\n===== computeQuotaState/QuotaInsufficient 相邻 =====")
for i, (off, s) in enumerate(strs):
    if s in ("computeQuotaState", "QuotaInsufficient", "markQuotaExceededBackoff", "quotaExceededRetryAt"):
        out.append(f"\n--- [{off}] {s}")
        for j in range(max(0, i - 8), min(len(strs), i + 9)):
            out.append(f"  [{strs[j][0]}] {strs[j][1][:150]}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_quota.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
