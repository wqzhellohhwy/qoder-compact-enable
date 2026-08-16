# -*- coding: utf-8 -*-
"""提取 promptEnhanceInstruction 全文 + cosy 模型通道（custom/api_key/base_url/openai/anthropic）证据。"""
import re

BIN = r"C:\Program Files\Qoder\resources\app\resources\bin\x86_64_windows\Qoder.exe"

with open(BIN, "rb") as f:
    blob = f.read()

strs = []
for m in re.finditer(rb"[\x20-\x7e]{8,}", blob):
    strs.append((m.start(), m.group().decode("ascii", errors="ignore")))
print("strings:", len(strs))

out = []

# 1) promptEnhanceInstruction 全文（找最长含 "improved" 或 "instruction" 的字符串）
out.append("===== promptEnhanceInstruction 模板 =====")
for off, s in strs:
    if s.startswith("Here is an instruction") or "improved. Rewrite and enhance" in s:
        out.append(f"[{off}] {s}")

# 2) 模型通道证据
out.append("\n===== 模型通道关键词 =====")
for kw in ["custom_model", "customModel", "api_key", "apiKey", "base_url", "baseUrl",
           "openai", "OpenAI", "anthropic", "dashscope", "deepseek", "byok", "BYOK"]:
    hits = [s for _, s in strs if kw.lower() in s.lower() and len(s) < 260]
    out.append(f"\n--- {kw}: {len(hits)} 条 ---")
    for h in hits[:12]:
        out.append(f"  [{h}]")

# 3) AskParams / PromptEnhanceResult 结构字段
out.append("\n===== PromptEnhance 结构 =====")
for off, s in strs:
    if re.search(r"PromptEnhance|EnhancedPrompt|AddedContext", s) and len(s) < 300:
        out.append(f"  [{off}] {s}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_asm.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
