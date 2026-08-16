# -*- coding: utf-8 -*-
"""修复 patch_qoder_enhance.py 的 P-E：改用 raw string 定义（\n 保持字面）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\patch_qoder_enhance.py"
data = open(P, encoding="utf-8").read()

# 当前 P-E NEW 行（从 "try{/* P-E start */" 到 "const K=await", 结尾）
start = data.find('        "try{/* P-E start */')
end = data.find('const K=await",', start)
if start < 0 or end < 0:
    print("P-E 行未找到")
    sys.exit(1)
end += len('const K=await",')

# raw string 版本（r"""...""" 内 \n \s \/ 全部保持字面）
new_line = (
    '        r"""try{/* P-E start */const G2=await R.resolvePromptModelMeta(c||"agent",o?.sessionType,d);'
    'const mMeta=G2?.CUSTOM_MODEL,mKey=G2?.MODEL_KEY;'
    'if(mKey&&mMeta?.parameters?.api_key){try{const apiKey=mMeta.parameters.api_key;'
    'const baseUrl=mMeta.provider==="deepseek"?"https://api.deepseek.com":(mMeta.base_url||"");'
    'if(baseUrl){const hr=await fetch(baseUrl.replace(/\\/+$/,"")+"/chat/completions",'
    '{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+apiKey},'
    'body:JSON.stringify({model:mMeta.model,messages:[{role:"system",'
    'content:"You are a professional prompt optimization assistant. Output only the optimized instruction wrapped in <enhanced-prompt> tags."},'
    '{role:"user",content:"Here is an instruction that I\'d like to give you, but it needs to be improved. '
    'Rewrite and enhance this instruction to make it clearer, more specific, less ambiguous, and correct any mistakes. '
    'Do not use any tools: reply immediately with your answer, even if you\'re not sure.'
    '\\n\\n<instruction>\\n"+e+"\\n</instruction>"}],stream:!1,temperature:.3}));'
    'const jd=await hr.json();const txt=jd?.choices?.[0]?.message?.content||"";'
    'const m2=txt.match(/<enhanced-prompt>([\\s\\S]*?)<\\/enhanced-prompt>/);'
    'const out=(m2?m2[1]:txt).trim();'
    'if(out&&U()){x.current=out;l?.current&&"setPromptEnhanceOperation"in l.current&&l.current.setPromptEnhanceOperation(e);'
    'n(out);g(!0);v(e);w([]);i();return}}catch(err){console.warn("[P-E] local enhance failed, fallback:",err)}}'
    '/* P-E end */const K=await""",'
)

data = data[:start] + new_line + data[end:]
with open(P, "w", encoding="utf-8", newline="\n") as f:
    f.write(data)
print("done")
