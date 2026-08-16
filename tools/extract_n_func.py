# -*- coding: utf-8 -*-
"""提取 customModelRecord 结构（base_url/provider 字段）+ V5p N 函数完整代码。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) customModelRecord 结构：找 vwa 的输入 e 的字段（getApiKey/getResolvedByokTypeKey 附近）
for pat in [r"getResolvedByokTypeKey\([^)]*\)\{", r"getApiKey\([^)]*\)\{"]:
    m = re.search(pat, data)
    if m:
        out.append(f"===== {pat} @{m.start()} =====")
        out.append(data[m.start():m.start()+1200])
        out.append("")

# 2) customModelRecord 字段：搜 "base_url" 在 custom 相关上下文
for m in list(re.finditer(r"base_url", data))[:8]:
    s = max(0, m.start() - 200)
    e = min(len(data), m.end() + 200)
    out.append(f"\n--- base_url @{m.start()} ---")
    out.append(data[s:e])

# 3) V5p N 函数完整代码（第一副本，从 const N= 到 },[...]) 结束）
m = re.search(r"const N=\(0,wY\.useCallback\)\(async\(\)=>\{", data)
if m:
    # 找结束：匹配到 },\[[^\]]*\]) 且是 N 的依赖数组
    start = m.start()
    # 找 },[...]) 模式（N 函数结尾），从 start 后第一个 "},[" 开始回溯
    tail = data[start:start+8000]
    # N 函数结束于 `},[e,h,d,...]` —— 找 `},[e,h,d` 
    endm = re.search(r"\},\[e,h,d", tail)
    if endm:
        out.append(f"\n===== V5p N 函数 @{start} =====")
        out.append(tail[:endm.end()+400])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_n_func.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
