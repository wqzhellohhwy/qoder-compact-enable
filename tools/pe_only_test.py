# -*- coding: utf-8 -*-
"""只测 P-E 自身（stub 环境运行）。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"
d = open(os.path.join(wd, "_test_enhance_copy.js"), encoding="utf-8", errors="replace").read()
i = d.find("try{/* P-E start */")
j = d.find("/* P-E end */const K=await", i)
pe = d[i:j] + "const K=await null;"

src = """
async function main(){
  const R = { resolvePromptModelMeta: async () => ({MODEL_KEY:"custom:model_x", CUSTOM_MODEL:{provider:"deepseek", model:"deepseek-chat", parameters:{api_key:"sk-test"}}}) };
  const c = "agent", o = { sessionType: "quest" }, e = "hello world";
  const U = () => true;
  const x = { current: "old" };
  const l = { current: {} };
  const n = (val) => { console.log("ENHANCED_OK:", val.slice(0, 40)); };
  let g = () => {}, v = () => {}, w = () => {}, i = () => {};
  global.fetch = async (url, opts) => {
    console.log("URL:", url);
    console.log("MODEL:", JSON.parse(opts.body).model);
    console.log("AUTH:", (opts.headers.Authorization || "").slice(0, 15) + "...");
    return { json: async () => ({ choices: [{ message: { content: "<enhanced-prompt>optimized text</enhanced-prompt>" } }] }) };
  };
  %PE%
  console.log("DONE");
}
main();
"""
src = src.replace("%PE%", pe)
tf = os.path.join(wd, "_t_pe_only.js")
with open(tf, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
r = subprocess.run(["node", tf], capture_output=True, text=True, timeout=60)
print("exit:", r.returncode)
print("STDOUT:", r.stdout[:300])
print("STDERR:", r.stderr[:500])
