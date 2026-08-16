# -*- coding: utf-8 -*-
"""对 P-E 段做括号配平分析（排除字符串/正则/注释）。"""
import sys, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_full.js", encoding="utf-8").read()

# 逐字符扫描，跳过字符串/正则/注释
i = 0
n = len(d)
stack = []
pairs = {")": "(", "}": "{", "]": "["}
line = 0
while i < n:
    c = d[i]
    if c == '"' or c == "'":
        quote = c
        i += 1
        while i < n:
            if d[i] == "\\":
                i += 2
                continue
            if d[i] == quote:
                break
            i += 1
    elif c == "/" and i + 1 < n and d[i + 1] == "/":
        i += 2
        while i < n and d[i] != "\n":
            i += 1
    elif c == "/" and i + 1 < n and d[i + 1] == "*":
        i += 2
        while i + 1 < n and not (d[i] == "*" and d[i + 1] == "/"):
            i += 1
        i += 2
    elif c == "/":
        # 正则近似（后跟字母/转义/括号）
        j = i + 1
        in_cls = False
        while j < n:
            if d[j] == "\\":
                j += 2
                continue
            if d[j] == "[":
                in_cls = True
            elif d[j] == "]":
                in_cls = False
            elif d[j] == "/" and not in_cls:
                break
            elif d[j] == "\n":
                break
            j += 1
        i = j + 1
    elif c in "({[":
        stack.append((c, i))
    elif c in ")}]":
        if not stack or stack[-1][0] != pairs[c]:
            print(f"不匹配: {c} @{i} (期望 {stack[-1][0] if stack else '空'} @{stack[-1][1] if stack else '-'})")
            sys.exit(1)
        stack.pop()
    i += 1

if stack:
    print(f"未闭合: {len(stack)} 个")
    for s, pos in stack[:10]:
        print(f"  {s} @{pos}: {repr(d[pos-40:pos+10])}")
else:
    print("括号配平 OK")
