# -*- coding: utf-8 -*-
"""cosy(Qoder.exe) 字符串分析：搜索 promptEnhance/quota/limit/URL/存储路径。"""
import re, os

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

out = []

# 提取可打印字符串（长度>=5）
print("extracting strings...")
with open(BIN, "rb") as f:
    blob = f.read()
print("size MB:", round(len(blob) / 1024 / 1024, 1))

strings = re.findall(rb"[\x20-\x7e]{5,}", blob)
str_list = [s.decode("ascii", errors="ignore") for s in strings]
print("strings count:", len(str_list))

# 关键词统计
keywords = {
    "promptEnhance": r"prompt[Ee]nhance",
    "enhance": r"[Ee]nhance",
    "quota": r"[Qq]uota",
    "limit": r"[Ll]imit",
    "daily": r"[Dd]aily",
    "count": r"[Cc]ount",
    "free": r"[Ff]ree",
    "http": r"https?://",
    "sqlite/db": r"\.(db|sqlite|sqlite3)",
    "cache": r"[Cc]ache",
}

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_str.txt", "w", encoding="utf-8") as f:
    for name, pat in keywords.items():
        hits = [s for s in str_list if re.search(pat, s)]
        f.write(f"\n{'='*20} {name}: {len(hits)} 条 {'='*20}\n")
        for h in hits[:40]:
            f.write("  " + h[:200] + "\n")
        if len(hits) > 40:
            f.write(f"  ... 共 {len(hits)} 条，仅显示前 40\n")
print("done")
