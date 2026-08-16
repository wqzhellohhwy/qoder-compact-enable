# -*- coding: utf-8 -*-
"""相邻字符串分析：prompt_enhance / FreeQuota / TryFreeQuota 的代码区域关联。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

# 带偏移的字符串列表
strs = []
for m in re.finditer(rb"[\x20-\x7e]{6,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))
print("strings:", len(strs))

targets = {
    "prompt_enhance": r"prompt_enhance",
    "FreeQuota": r"FreeQuota",
    "TryFreeQuota": r"TryFreeQuota",
    "promptEnhance": r"promptEnhance",
    "agent.experts": r"agent\.experts\.communication",
}

out = []
for name, pat in targets.items():
    idxs = [i for i, (_, s) in enumerate(strs) if re.search(pat, s)]
    out.append(f"\n{'='*25} {name}: {len(idxs)} 处 {'='*25}")
    for i in idxs[:10]:
        off = strs[i][0]
        out.append(f"\n--- offset {off} ---")
        # 前后各 20 个字符串
        for j in range(max(0, i - 20), min(len(strs), i + 21)):
            marker = ">>" if j == i else "  "
            s = strs[j][1]
            if re.search(r"quota|limit|free|prompt|enhance|daily|count|110|115|error\.code", s, re.IGNORECASE) or j == i:
                out.append(f"  {marker} [{strs[j][0]}] {s[:160]}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_adj.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
