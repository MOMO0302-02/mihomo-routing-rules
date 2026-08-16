# Changelog

## v2026.08.16.1GoogleAITK

### Rules

- `ai_custom` 增加 68 条域名规则，由 96 条增至 164 条；分类保持 22 个，总量由 711 条增至 779 条。全部 68 条均经 DNS 解析与 HTTP 探测确认存活。
- **`.google` gTLD 补齐 6 条**：`gemini.google`、`aistudio.google`、`notebooklm.google`、`notebook.google`、`jules.google`、`opal.google`。与 `antigravity.google` 同一失效模式——`geosite:google` 不覆盖 `.google`，无规则命中就静默落到 `MATCH`。实测 `notebooklm.google` 已 302 跳转到新域名 `notebook.google`，`aistudio.google` 与 `gemini.google` 302 跳转到各自 `.com`；此前本库只收 `.com` 一侧，跳转的第一跳没有任何规则命中。
- **产品迁移补齐 4 条**：`windsurf.com`、`codeium.com`、`devin.ai`、`cognition.ai`。实测 `codeium.com` 301 → `windsurf.com` 308 → `devin.ai/desktop`（Cognition 收购 Windsurf）。此前本库只有 `api.windsurf.com` 与 `server.codeium.com` 两条子域，主域与迁移后的新域全部无规则命中。
- **厂商主域补齐 14 条**：`mistral.ai`、`cohere.com`、`stability.ai`、`fireworks.ai`、`novita.ai`、`cerebras.ai`、`sambanova.ai`、`deepinfra.com`、`ai21.com`、`reka.ai`、`writer.com`、`dify.ai`、`baseten.co`、`together.xyz`。这些厂商此前只收了 `api.*` 端点，官网与控制台（如 Le Chat、`console.mistral.ai`）落 `MATCH`。
- **新增 AI 产品 44 条**：`kimi.com`、`z.ai`、`qwen.ai`、`manus.im`、`genspark.ai`、`lmarena.ai`、`arena.ai`、`you.com`、`phind.com`、`abacus.ai`、`deepl.com`、`fal.ai`、`civitai.com`、`leonardo.ai`、`hume.ai`、`udio.com`、`klingai.com`、`hailuoai.video`、`pixverse.ai`、`higgsfield.ai`、`hedra.com`、`synthesia.io`、`descript.com`、`gamma.app`、`napkin.ai`、`lovable.dev`、`bolt.new`、`stackblitz.com`、`v0.app`、`replit.com`、`zed.dev`、`warp.dev`、`augmentcode.com`、`sourcegraph.com`、`tabnine.com`、`continue.dev`、`factory.ai`、`qodo.ai`、`modal.com`、`runpod.io`、`lambda.ai`、`hyperbolic.xyz`、`hyperbolic.ai`、`chutes.ai`。
- 其中两组域名迁移新旧并存：`lmarena.ai` 301 → `arena.ai`，`hyperbolic.xyz` 301 → `hyperbolic.ai`。
- 国内厂商的**国际站**（`kimi.com`、`z.ai`、`qwen.ai`、`klingai.com`、`hailuoai.video` 等）进 `ai_custom` 走代理，与 `deepseek.com` 在 `ai_custom`、`api.deepseek.com` 在 `ai_api_direct_custom` 的「网页域走代理、API 域走直连」分工一致。判据是**面向国内还是面向国际**，不是能否直连——`deepseek.com` 实测直连可达（429 / 1.0s）却照样走代理。
- **刻意未收录**面向国内的产品域 `hailuoai.com`（海螺国内站，国际站 `hailuoai.video` 已收）与 `vidu.com`：Vidu 的 `vidu.com` / `vidu.cn` / `vidu.studio` 三个域全部 301 → `www.vidu.cn`，已无独立国际站。本库没有网页类直连分类（只有 API 侧的 `ai_api_direct_custom`），收进 `ai_custom` 会把国内流量推上代理；要收必须新建直连分类。
- `minimax.io` 未动：整个后缀已在 `ai_api_direct_custom` 走直连，属既有决策而非缺口。

### Sync

- 同批 68 条已同步写回上游订阅工作台的规则源，两侧 `ai_custom` 逐条一致（按本库去冗余约定归一化后差异 0 条）。

## v2026.08.02.5GoogleAITK

### Maintenance

- 仅对齐版本标记到上游订阅工作台 `v2026.08.02.5GoogleAITK`，**规则内容自 `v2026.07.29.1GoogleAITK` 起未发生任何变化**：22 个分类、711 条规则逐条相同。
- 上游在此期间的改动集中在 sing-box DNS 父级策略继承、DNS 精简与节点集合，均不属于本库发布范围（本库只发布分流规则）。
- 已双向比对上游规则源确认同步：需新增 0 条、需移除 0 条；上游多出的 102 条 `DOMAIN` 仍是被同组 `DOMAIN-SUFFIX` 完全覆盖的冗余，按本库既有去冗余约定不收录。

## v2026.07.29.1GoogleAITK

### Rules

- `ai_custom` 增加 `DOMAIN-SUFFIX,antigravity.google`，覆盖 Google Antigravity 的授权与产品域名；分类保持 22 个，规则由 710 条增至 711 条。
- 该域名此前无任何规则命中，会落到用户配置的兜底策略，与同一登录链路上的 `*.googleapis.com` 分处不同策略组。`.google` gTLD 不被 `geosite:google` 覆盖，同类域名需逐条显式加入。

## v2026.07.28.2GoogleAITK

### Rule quality

- 无损移除 102 条已被同组 `DOMAIN-SUFFIX` 完全覆盖的 `DOMAIN` 规则。
- 公开分类保持 22 个，规则由 812 条精简为 710 条，实际匹配范围不变。
- 验证器新增同类语义冗余门禁，防止重复写法回流。

### Distribution

- 增加稳定 `release` 消费分支，`main` 保留为开发与文档分支。
- 所有示例切换到 `release` 地址。
- 增加 22 类规则索引、GitHub Raw 与 jsDelivr 双下载地址。
- 增加贡献、隐私和发布流程说明。
- 扩展验证器，锁定稳定地址、规则索引和示例完整性。

## v2026.07.28.1GoogleAITK

### Public rule set

- 首次公开 22 个通用分类，共 812 条 Mihomo classical 规则。
- 排除机场站点、本地专用服务、订阅、节点和凭据。
