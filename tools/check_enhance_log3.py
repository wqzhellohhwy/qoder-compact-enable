# -*- coding: utf-8 -*-
"""查最新 agent.log 中 resolvePromptModelMeta 记录（判断 P-E 生效次数）。"""
import re, os, glob, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out = []
log_dirs = sorted(glob.glob(os.path.expandvars(r"%APPDATA%\Qoder\logs\*")), reverse=True)[:2]
for ld in log_dirs:
    out.append(f"\n########## {os.path.basename(ld)} ##########")
    for fn in glob.glob(os.path.join(ld, "**", "agent.log"), recursive=True):
        try:
            content = open(fn, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        # 15:1x 之后的 resolvePromptModelMeta / promptEnhance 相关
        for pat in [r"resolvePromptModelMeta", r"promptEnhance", r"prompt/enhance", r"CHAT_PROMPT_ENHANCE"]:
            for m in re.finditer(pat, content):
                s = max(0, m.start() - 120)
                e = min(len(content), m.end() + 150)
                seg = content[s:e].replace("\n", " ")
                out.append(f"\n--- [{pat}] {os.path.basename(fn)} ---")
                out.append(seg)

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_chk3.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done, lines:", len(out))
