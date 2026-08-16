# -*- coding: utf-8 -*-
"""日志验证 promptEnhance 通道：resolvePromptModelMeta / prompt_enhance / byok / custom model resolved。"""
import re, os, glob

out = []
log_dirs = sorted(glob.glob(os.path.expandvars(r"%APPDATA%\Qoder\logs\*")), reverse=True)[:4]
pats = [r"resolvePromptModelMeta", r"custom model resolved", r"prompt_enhance", r"EnhancePrompt",
        r"byok", r"BYOK", r"CUSTOM_MODEL", r"customModel", r"modelConfig.*(?:custom|experts)",
        r"queryModels", r"SHOW_MODEL_SELECTOR"]
seen = set()
for ld in log_dirs:
    for fn in glob.glob(os.path.join(ld, "**", "*.log"), recursive=True):
        try:
            content = open(fn, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for pat in pats:
            for m in re.finditer(pat, content, re.IGNORECASE):
                s = max(0, m.start() - 150)
                e = min(len(content), m.end() + 200)
                seg = content[s:e].replace("\n", " ")
                key = pat + "|" + seg[:100]
                if key in seen:
                    continue
                seen.add(key)
                out.append(f"\n--- [{pat}] {os.path.basename(fn)} ---")
                out.append(seg)

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_chk_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done, lines:", len(out))
