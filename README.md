# Qoder 对话压缩无条件启用工具

解除 Qoder 的"压缩当前对话"（Compact Chat）按钮的上下文使用率门槛，
**任意时刻（含新对话、低使用率）均可压缩当前对话**。纯客户端 UI 层修改，
单文件 3 处 patch，幂等可重跑，自动备份与回滚。

## 项目背景

Qoder 聊天界面提供"压缩当前对话"功能（总结历史对话并继续），
但压缩按钮在**上下文使用率低于 40%** 时被禁用，悬停提示"对话内容较短，暂无需压缩"。

经反混淆分析客户端 bundle（`agents-window.desktop.main.js`），
定位到该限制在 **3 个窗口副本**的 overlay 组件中（本地 chat 面板 / quest 输入面板 / agents 窗口）：

| 副本 | 原禁用条件 | 阈值常量 |
|---|---|---|
| 本地 chat 面板 | `c = s \|\| t < iDa` | `nDa=64`（提示条阈值）, `iDa=40`（压缩门槛） |
| quest 输入面板 | `c = s \|\| t < oyu` | `iyu=64`, `oyu=40` |
| agents/experts 窗口 | `c = s \|\| t < kHu` | `SHu=64`, `kHu=40` |

（`s`=对话生成中，`t`=上下文使用率百分比；阈值随 Qoder 版本可能变化，
`tools/` 目录下的分析脚本可重新定位。）

客户端 service 层（`compressContext`）与后端 RPC（`context/compact`）均无本地限制，
故 UI 层放开后即全链路可用。

## 核心功能

- **单文件 3 处 patch**（幂等：重复运行自动跳过，不会重复修改）
- 禁用条件 `s || t < 阈值` → `s`：仅"对话生成中"禁用，百分比不再是门槛
- 每次运行自动备份（`.bak_compact_时间戳`）+ 读回验证
- **完整回滚**：从最近备份一键恢复
- **路径自动探测**：无需任何本地路径配置

## 技术栈

- Python 3（标准库，无第三方依赖）
- Webpack 混淆 JS 逆向分析（单行 bundle、上下文定位）
- BAT 入口（管理员运行）

## 快速开始

前置：Windows + Qoder 桌面版（本工具针对 Windows 版 Qoder 开发）。

```bat
:: 1. 完全退出 Qoder（含系统托盘）
:: 2. 右键以管理员身份运行（需要写 Program Files）
patch_qoder_compact.bat

:: 3. 重启 Qoder
:: 4. 任意对话（哪怕只有 1 条消息）：
::    点击输入框旁上下文百分比图标 -> Compact Chat 按钮可点击
```

脚本输出 `[3/3] 读回验证通过` 即成功。

## 使用方法

### 路径探测与自定义

脚本按以下优先级自动定位 Qoder 客户端 bundle：

1. `--js <完整路径>` 命令行参数（测试/非标准安装时使用）
2. 环境变量 `QODER_INSTALL_DIR`（Qoder 安装根目录）
3. 常见安装位置（Program Files / Program Files (x86) / %LOCALAPPDATA%\Programs）

```bat
:: 指定路径运行
python patch_qoder_compact.py --js "D:\Apps\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

:: 或通过环境变量
set QODER_INSTALL_DIR=D:\Apps\Qoder
patch_qoder_compact.bat
```

### 验证

- 新开对话（使用率 < 40%），打开上下文面板：压缩按钮不再禁用
- 日志出现 `Starting context compression for session ...`（Qoder 日志目录 logs/）
- 备份存在：`agents-window.desktop.main.js.bak_compact_*`

### 回滚

```bat
rollback_qoder_compact.bat   :: 管理员运行，从最近 .bak_compact_* 备份恢复
```

### 维护

- **Qoder 升级会覆盖 patch**：升级后重新运行 `patch_qoder_compact.bat` 即可
- **版本不匹配**：脚本提示"未找到目标代码段"并写入 `_js_version.txt`，
  说明新版本代码结构已变化；可用 `tools/` 下的分析脚本重新定位
  （`search_compact.py` 搜关键词 → `extract_threshold.py` 提取上下文 → `verify_compact.py` 验证）

## 功能二：优化输入增强（promptEnhance）

### 项目背景

输入框旁的"优化输入"（Prompt Enhance）按钮存在两处本地限制与一处通道缺陷：
- **字数限制**：输入 <3 字符或 >1000 字符时按钮禁用（3 个窗口副本）
- **通道缺陷**：请求仅在 `SHOW_MODEL_SELECTOR` 特性开关开启时才附带自定义模型元数据
  （`_meta`）；实测 cosy 下发的特性配置不含 `showModelSelector` → 请求从不带 `_meta`
  → 增强请求走官方模型通道（消耗官方每日配额，错误码 110 "daily usage limit"），
  而非用户配置的自定义模型（BYOK）

### 实现

单文件 10 处 patch（3 副本 × 4 项，幂等）：
- P-A：禁用条件 `z = r || e.trim().length<3` → `z = r`（仅对话生成中禁用）
- P-B：禁用条件 `$ = e.length > 常量` → `$ = false`（解除 1000 字符上限）
- P-C：`if(Gi[Ui.SHOW_MODEL_SELECTOR]){...}` → 无条件调用 `resolvePromptModelMeta`，
  请求始终携带自定义模型 `_meta`（provider/model/api_key）
- P-D：`extra.customModel = {name: MODEL_KEY, value: model}`（普通聊天同款字段）
  —— 仅传 `_meta` 不够（实测仍报官方配额错误 113）；cosy 的
  `AskParams.extra.customModel`（ChatAskExtraParams）才是指定 BYOK 模型引用的通道，
  cosy 按 name 从本地 byok 配置解析 api_key 直连第三方 API

### 使用

```bat
:: 1. 完全退出 Qoder
:: 2. 右键以管理员身份运行
patch_qoder_enhance.bat

:: 3. 重启 Qoder -> 优化输入任意长度可点，请求走自定义模型
```

### 回滚

```bat
rollback_qoder_enhance.bat   :: 管理员运行，从最近 .bak_enhance_* 备份恢复
```

### 验证

- 1-2 字符 / 超 1000 字符的输入，优化输入按钮均可点击
- 日志出现 `resolvePromptModelMeta custom model resolved: provider=deepseek`
  且随后的增强请求不再返回 110（今日已达上限）
- 自定义模型平台（如 DeepSeek 开放平台）可见增强请求的 token 消耗

## 目录结构

```
compact/
├── patch_qoder_compact.py/.bat    # 压缩：解除 40% 门槛（3 副本，幂等，管理员）
├── rollback_qoder_compact.py/.bat # 压缩回滚
├── patch_qoder_enhance.py/.bat    # 优化输入：解除字数限制 + 强制自定义模型通道
├── rollback_qoder_enhance.py/.bat # 优化输入回滚
├── tools/                         # 逆向分析辅助脚本（可复用）
│   ├── search_compact.py          # 关键词统计定位
│   ├── extract_*.py               # 上下文/常量/组件提取
│   ├── scan_workbench.py          # 多 bundle 关键词扫描
│   └── verify_compact.py          # patch 结果读回验证
└── README.md
```

## 注意事项

- 本工具修改 Qoder 客户端文件（Program Files），仅适用于个人环境
- 所有修改自动备份，回滚脚本可从最近备份恢复
- 若 Qoder 更新了压缩逻辑（阈值/组件重构），patch 会失效——重新定位后更新脚本即可
- 不包含任何凭据信息；压缩请求由 Qoder 客户端发出，走用户已配置的模型通道
