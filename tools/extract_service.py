# -*- coding: utf-8 -*-
"""提取 ContextThresholdService 类与 overlay 组件完整代码。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) service 类：从 @6718792 开始，找类定义起点和终点
# 找包含 sessionCompressionStates=new Map 的类声明
m = re.search(r"class \w+[^{]*\{[^{]*sessionCompressionStates=new Map", data)
if m:
    # 类名
    cls_start = m.start()
    cls_name_m = re.search(r"class (\w+)", data[cls_start:cls_start+200])
    out.append(f"service 类名: {cls_name_m.group(1)} @{cls_start}")
    # 找类结束：下一个 "};" 后面跟 __decorate 或 var 定义
    # 简化：取 40000 字符
    out.append(data[cls_start:cls_start+40000])

# 2) 找 _callCompressionAPI 完整定义
m2 = re.search(r"async _callCompressionAPI\([^)]*\)\{", data)
if m2:
    out.append("\n\n===== _callCompressionAPI @%d =====" % m2.start())
    out.append(data[m2.start():m2.start()+3000])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_service_ctx.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
