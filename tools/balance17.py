# -*- coding: utf-8 -*-
"""第 17 行括号配平（预替换正则）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\_t_pe_run.js", encoding="utf-8").read()
line = d.split("\n")[16]
line2 = (
    line.replace('/<enhanced-prompt>([\\s\\S]*?)<\\/enhanced-prompt>/', "REGEX1")
    .replace('/\\/+$/', "REGEX2")
)
print("替换后长度:", len(line2))

stack = []
pairs = {")": "(", "}": "{", "]": "["}
ok = True
for idx, ch in enumerate(line2):
    if ch in "({[":
        stack.append((ch, idx))
    elif ch in ")}]":
        if not stack or stack[-1][0] != pairs[ch]:
            print("不匹配", ch, "@", idx, "期望", stack[-1][0] if stack else "空")
            ok = False
            break
        stack.pop()
if ok:
    if stack:
        print("未闭合", len(stack), "个:")
        for s, pos in stack[:8]:
            print(" ", s, "@", pos, repr(line2[max(0, pos - 30): pos + 10]))
    else:
        print("第17行括号配平 OK")
