# -*- coding: utf-8 -*-
"""搜索次数/剩余相关文案 + 日志中的 promptEnhance 记录。"""
import re, os, glob

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 中文次数/剩余相关文案（unicode 转义）：
# 剩余=\u5269\u4f59 次数=\u6b21\u6570 今日=\u4eca\u65e5 已用=\u5df2\u7528 免费=\u514d\u8d39 额度=\u989d\u5ea6
for cn in ["\u5269\u4f59", "\u6b21\u6570", "\u4eca\u65e5", "\u514d\u8d39", "\u989d\u5ea6"]:
    pat = cn
    ms = list(re.finditer(pat, data))
    out.append(f"中文'{cn}' 出现: {len(ms)}")
    for m in ms[:6]:
        s = max(0, m.start() - 100)
        e = min(len(data), m.end() + 100)
        out.append(f"  --- @{m.start()} ---")
        out.append("  " + data[s:e])
    out.append("")

# 日志目录中 promptEnhance / enhance 相关
out.append("\n===== 日志扫描 =====")
log_dirs = sorted(glob.glob(os.path.expandvars(r"%APPDATA%\Qoder\logs\*")), reverse=True)[:2]
for ld in log_dirs:
    for fn in glob.glob(os.path.join(ld, "**", "*.log"), recursive=True):
        try:
            with open(fn, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue
        hits = []
        for pat in [r"promptEnhance", r"prompt enhance", r"enhance", r"PromoptEnhance", r"110|115"]:
            for m in re.finditer(pat, content, re.IGNORECASE):
                hits.append(m)
        if hits:
            out.append(f"\n--- {os.path.relpath(fn, ld)}: {len(hits)} hits ---")
            for m in hits[:4]:
                s = max(0, m.start() - 120)
                e = min(len(content), m.end() + 120)
                out.append("  " + content[s:e].replace("\n", " "))

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_quota.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
