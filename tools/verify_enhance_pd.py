# -*- coding: utf-8 -*-
"""验证真实文件 P-D（extra.customModel）注入结果。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js", encoding="utf-8", errors="replace").read()

old_pd = "params:{sessionId:d,questionText:e,references:K,...G?{_meta:G}:{}}}})"
new_pd = "params:{sessionId:d,questionText:e,references:K,extra:G?.MODEL_KEY?{customModel:{name:G.MODEL_KEY,value:G.CUSTOM_MODEL?.model||G.MODEL_KEY}}:{},...G?{_meta:G}:{}}}})"
print("P-D OLD 残留:", d.count(old_pd))
print("P-D NEW 注入:", d.count(new_pd))
print("extra.customModel 总出现:", d.count("extra:G?.MODEL_KEY?{customModel:"))
