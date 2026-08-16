# -*- coding: utf-8 -*-
"""查最新日志：promptEnhance 链路 + 113/配额错误。"""
import re, os, glob

out = []
log_dirs = sorted(glob.glob(os.path.expandvars(r"%APPDATA%\Qoder\logs\*")), reverse=True)[:2]
pats = [r"resolvePromptModelMeta", r"prompt_enhance", r"EnhancePrompt", r"enhance", r"statusCode",
        r"113", r"quota", r"Quota", r"limit", r"byok", r"custom model resolved", r"promptEnhance"]
seen = set()
for ld in log_dirs:
    out.append(f"\n########## 日志目录: {os.path.basename(ld)} ##########")
    for fn in glob.glob(os.path.join(ld, "**", "*.log"), recursive=True):
        try:
            content = open(fn, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        # 优先精确模式
        for pat in [r"prompt_enhance", r"EnhancePrompt", r"resolvePromptModelMeta", r"custom model resolved"]:
            for m in re.finditer(pat, content, re.IGNORECASE):
                s = max(0, m.start() - 200)
                e = min(len(content), m.end() + 300)
                seg = content[s:e].replace("\n", " ")
                key = pat + "|" + seg[:80]
                if key in seen:
                    continue
                seen.add(key)
                out.append(f"\n--- [{pat}] {os.path.basename(fn)} ---")
                out.append(seg)

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_chk2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done, lines:", len(out))
