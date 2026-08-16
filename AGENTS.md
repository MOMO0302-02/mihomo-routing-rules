---
项目: Mihomo Routing Rules
维护方: Codex
真相源: 本文件 + manifest.json + Git
最后校准: 2026-08-17
状态源: git
状态源路径: F:\AI\Github分流规则
---

# Mihomo Routing Rules 上手包

## 一句话

这是从订阅工作台脱敏导出的公开 Mihomo classical rule-provider 规则库，只包含分流规则，不包含代理节点、订阅地址或发布凭据。

## 当前状态

- 公开规则版本：`v2026.08.17.2GoogleAITK`（22 类、700 条）。2026-08-17 冗余审查后无损移除 79 条（53 条被同分类更宽后缀覆盖 + 26 条域名已失效），匹配行为不变，细节见 `CHANGELOG.md`。**与上游差异扩大，同步时需以本库为准整体回灌，不能逐条比对。**
- 2026-08-17 判据（不可据「主域不解析」删规则）：库内有 133 个域名主域无 A 记录，但全是 CDN 通配域（`ytimg.com`、`githubusercontent.com`、`akamai.net`、`mp.microsoft.com`、`msftconnecttest.com` 等），子域天天在用，`DOMAIN-SUFFIX` 匹配完全正常。判失效必须满足：**多个解析器均无记录 + 带对照组 + 代理亦不可达**，三者缺一不可。
- 2026-08-17 统计陷阱：查「被谁覆盖」时若对每条规则只记录**第一个**命中的覆盖者，会把同时被 `DOMAIN-KEYWORD` 和 `DOMAIN-SUFFIX` 覆盖的规则误分类。本次因此把零风险集合从 79 条误报成 49 条。统计覆盖关系必须枚举**全部**覆盖者再分类。
- 2026-08-17 待办（本次未动，已确认存在）：① `tencent_docs_direct_custom` 名为「腾讯文档直连」，实含 `qq.com`（整个 QQ）与 `myqcloud.com`/`qcloud.com`/`tencent-cloud.net`（整个腾讯云，承载大量第三方站点资源），公开库使用者按名字无法预期此范围；② `DOMAIN-KEYWORD,adobe` / `tiktok` / `douyin` 会命中任意含该词的无关域名；③ `ai_custom` 收了 22 组通用第三方 SaaS 全域（`sentry.io`、`segment.com`、`intercom.io`、`auth0.com`、`launchdarkly.com`、`challenges.cloudflare.com`、`browser-intake-datadoghq.com` 等），ChatGPT 登录链确需，但会连带把使用者所有网站的错误上报/分析/验证码流量送进 AI 组（`openai_login_custom` 反而用 `DOMAIN,o207216.ingest.sentry.io` 这类精确写法）。三项均需用户决策后再动。2026-08-17 逐字符审查后修两处：补 `cognition.com`（`ai_custom` 165），删 `google_drive_custom` 中被 `youtube_custom` 完全覆盖的 `DOMAIN,s.ytimg.com`（44），并把 `youtube_custom` 的推荐顺序提到 `google_drive_custom` 之前。**本版未同步上游，两侧现有 2 条差异**（公开库多 `cognition.com`、少 `s.ytimg.com`），上游同步时需一并处理。
- 2026-08-17 踩坑（跨分类遮蔽）：`validate_rules.py` **只查单文件内的语义冗余，查不到跨分类遮蔽**。`youtubei.googleapis.com` 从首个公开版本起就永远匹配不到——被推荐顺序中更靠前的 `google_drive_custom` 的 `DOMAIN-SUFFIX,googleapis.com` 吃掉，策略从 `Streaming` 变成 `AI`。**新增宽后缀规则（尤其 `*.googleapis.com` `*.google.com` 这类平台级域）必须结合 `examples/rules.yaml` 的顺序做一次全库遮蔽分析**，且注意两个分类可能双向覆盖，只调顺序会把冲突推到另一侧。判据：被更早分类覆盖且**策略不同**才是真问题，策略相同只是冗余。
- 2026-08-17：改推荐顺序会影响已复制过配置的使用者——他们不重新复制就拿不到修复。顺序变更必须在 `CHANGELOG.md` 里显式写明这一点。
- 2026-08-16 在 `ai_custom` 增加 68 条（96→164），细节见 `CHANGELOG.md`；同批已同步写回上游订阅工作台规则源，两侧逐条一致。**2026-08-16 经用户授权已发布**：commit `6a2245c` 推送 `main`，CI `Validate rules` 通过，`release` 无分叉快进到同一提交，tag `v2026.08.16.1GoogleAITK` 已推送；实测线上 release 的 `ai_custom.yaml` 与本地逐字节一致（164 条）。
- 2026-08-16：本次版本标记由本库先行铸造（规则先在本库和上游规则源落地，上游尚未重新生成），与「只在与上游内容等价后对齐」的常规顺序相反。上游下次生成时应确认它带出同一标记；若上游生成出别的序号，以上游为准回改本库。
- 版本标记只在与上游比对确认内容等价后对齐；条目有实际增删时必须同步 `manifest.json` 计数与 SHA-256、`RULES.md` 索引及 `CHANGELOG.md`。
- 2026-08-16 踩坑（`.google` 教训的推广）：域名迁移和产品被收购同样会让旧规则静默失效，且不会报错。实测发现 `notebooklm.google`→`notebook.google`、`lmarena.ai`→`arena.ai`、`hyperbolic.xyz`→`hyperbolic.ai`，以及 Windsurf 被 Cognition 收购后 `codeium.com`→`windsurf.com`→`devin.ai`。**只收 `api.*` 子域而不收主域**是同一类隐患（本次补了 14 家）。维护时应定期对已收录厂商做一次跳转探测，而不是只做「有没有新产品」的增量。
- 2026-08-16：国产 AI 站点收不收、进哪类，判据是**面向国内还是面向国际**，不是能否直连。实测 `deepseek.com` 直连可达（429 / 1.0s）但本库一直让它走 `ai_custom` 代理；反过来国内站直连快也不代表该收进 `ai_custom`。据此 `kimi.com`/`z.ai`/`qwen.ai`/`klingai.com`/`hailuoai.video` 等国际站进 `ai_custom`，而面向国内的 `hailuoai.com`（海螺国内站）与 `vidu.com`（`vidu.com`/`vidu.cn`/`vidu.studio` 全部 301 → `www.vidu.cn`，已无独立国际站）**刻意未收录**——本库没有网页类直连分类（只有 API 侧的 `ai_api_direct_custom`），收进 `ai_custom` 会把国内流量推上代理。要收必须新建直连分类。
- 2026-08-16 工具坑：本机 shell 设了 `HTTP_PROXY`/`HTTPS_PROXY=http://127.0.0.1:7890`，`curl` 不带 `-x` 也会走代理，直连探测会得出「直连和代理表现完全一致」的假结论。测直连必须加 `--noproxy '*'`，并且带对照组验证（`baidu.com` 应通、`google.com` 应超时）才算数。
- 规则文件、条目数和 SHA-256 以 `manifest.json` 为准。
- 使用方式以 `README.md`、`RULES.md` 与 `examples/all-in-one.yaml` 为准；示例是合并片段，不是完整订阅。
- `main` 是开发与文档分支，`release` 是通过验证后的稳定消费分支；公开配置地址只引用 `release`。
- GitHub 仓库：`MOMO0302-02/mihomo-routing-rules`。

## 怎么验证

```powershell
python tools\validate_rules.py
git diff --check
```

## 红线

- 禁止加入代理节点、UUID、密码、订阅地址、Cloudflare/GitHub 凭据或本机状态。
- `airport_site_custom` 与 `recmata_service_direct_custom` 属于私有工作台规则，不得发布。
- 修改规则后必须同步 `manifest.json` 中的计数与 SHA-256，并通过验证器。
- 公开发布、改可见性和删除仓库仍需用户明确授权。

## 跨工具任务接续（Beads）

项目使用本机 stealth 模式 `.beads`。新会话先运行：

```powershell
bd prime
bd ready
```

- `ai-ready/open`：AI 可直接执行的本地工作。
- `human/blocked`：需要用户选择或人工验收。
- `external-authorization/blocked`：公开发布、打 tag、推送或外部状态变更。
- `backlog/deferred`：以后再评估。
