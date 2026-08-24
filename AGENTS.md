---
项目: Mihomo Routing Rules
维护方: Codex
真相源: 本文件 + manifest.json + Git
最后校准: 2026-08-24
状态源: git
状态源路径: F:\AI\Github分流规则
---

# Mihomo Routing Rules 上手包

## 一句话

这是从订阅工作台脱敏导出的公开 Mihomo classical rule-provider 规则库，只包含分流规则，不包含代理节点、订阅地址或发布凭据。

## 当前状态

- 公开规则版本：`v2026.08.24.4GoogleAITK`（**23 类、925 条**）。2026-08-24 晚间四项升级：①新增 `ntp_direct_custom`（16 条，DoH 全验活；**必须排推荐顺序最前**，否则 `time.windows.com` 被 Microsoft 分类的 `windows.com` 后缀截走）；②CI 加 `core-load` job（真内核加载门禁，内核版本钉在 workflow `MIHOMO_VERSION`，内核发新版时手动升）；③tag 推送自动建 Release + release 分支推送自动清 jsDelivr 缓存（`release.yml` / `purge-cdn.yml`）；④体检脚本入库 `tools/`（`coretest.py` / `check_liveness.py` / `probe_migration.py` / `changelog_section.py`），以后不再每轮临时重写。注意：`coretest.py --binary` 在 Windows 要传**绝对路径**（CreateProcess 不认相对正斜杠路径）。
- 2026-08-24 晚间体检：对当日新增的 203 条做迁移+存活探测——25 个跨站跳转中 22 个目标已覆盖，3 个未覆盖目标（`aka.ms` 根跳转占位页、JetBrains 官网×2）均属营销/占位页按判据不收；50 个无响应域经 DoH 三重判定**全部存活**（均为主域无 A 的正常 CDN 形态）。909 条真内核加载 0 错误。**本轮零规则变更**，仅修文档。
- 2026-08-24 **测活方法被环境变化打破（重要）**：本机 Clash Party 开启了 fake-ip DNS 接管——即使用 `Resolve-DnsName -Server 223.5.5.5` 直查外部解析器，UDP 53 也被截走，任何域名（包括不存在的）都返回 `198.18.0.x` 段假 IP，8-17 的 DNS 测活方法**对照组已失效**。现行有效方法：**DoH**（`curl -x 代理 "https://dns.google/resolve?name=域名&type=A"`），按返回 JSON 的 `Status` 判定（0=存在、3=NXDOMAIN），Answer 有无区分「有 A 记录」与「主域无 A 的 CDN 形态」；对照组必须同跑（baidu.com 应 LIVE、构造假域名应 Status=3）。**任何测活结论前先看对照组，对照组不对全批作废。**
- 2026-08-24 与**官方 geosite 的定位关系已确定：互补，不是替代**。与内核自带的 `geosite:category-ai-!cn`（MetaCubeX 维护）双向比对：官方 179 条里本库未覆盖 85 条（收 61、剔 24），本库有而官方没有 118 条。判据差异在于**官方名单只回答「是不是 AI 网站」，本库还要回答「该走哪个出口」**——国内 API 直连 vs 网页代理、账号类必须钉固定出口 IP，这些官方名单表达不了。**实测官方 `geosite:cn`（11 万条）里含 `qoder.com`**，只靠官方名单会把它判成国内站直连。官方名单的正确用法是当**参照与补充源**：`temp/gap_vs_ref.py` 可直接换 `temp/geo_ai.list` 复跑。
- 2026-08-24 官方名单取自 `https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/<名>.list`（文本版，`+.` 前缀＝后缀匹配）；`geosite/ntp` 与 `geosite/stun` **不存在**（查过 404），需要这两类规则只能自己写域名；`geoip/telegram` 存在，是 Telegram 纯 IP 流量的唯一抓法。
- 2026-08-24 本库自身一处过宽规则已记入文档（未改行为）：`github_custom` 的 `DOMAIN-SUFFIX,blob.core.windows.net` 覆盖**整个 Azure 对象存储**，与既有的 `ai_custom` 通用 SaaS、腾讯分类同属「范围比分类名大」，`RULES.md` 已列为第 4 条并给出移除指引。
- 2026-08-24 踩坑（**换行符会让本地验证器与 CI 给出相反结论**）：在 Windows 上用 Python 的 `write_text` 改文件会把 LF 写成 CRLF，而 Git 按 `.gitattributes` 统一存成 LF——于是 `manifest.json` 里记的 SHA-256 是 CRLF 字节算的，本地验证器读同一份 CRLF 副本**照样通过**，推上去 CI 立刻报 9 条 `manifest SHA-256 mismatch`。规则内容无损，坏的只是校验值。教训：**改仓库文件一律以二进制写、显式用 LF**；`validate_rules.py` 已加 CRLF 门禁（负对照已验证），此后本地就能拦下。已发 `v2026.08.24.2GoogleAITK` 修正。
- 2026-08-24 第二轮参照比对覆盖了此前没动过的四个分类，再补 67 条。**最大的一处真空是微软**：原 `microsoft_custom` 只有 4 条（Xbox + `live.com` + `msedge.net`），OneDrive / SharePoint / Office 一条没有；并发现 `office.com` 已 302 至 **`cloud.microsoft`**（微软新启用的统一应用域），此前无任何规则命中。另有三处新迁移：`notion.so`/`notion.site`→`notion.com`、`zoom.us`→`zoom.com`、`skype.com`→`teams.live.com`（后者已被 `live.com` 覆盖，故 `skype.com` 未收）。
- 2026-08-24 内核验证已用**官方 Mihomo Meta v1.19.30** 重做：848 条 + 22 provider + 推荐顺序，0 错误 0 警告；并做了负对照（注入 `NOT-A-RULE-TYPE` 内核如实报 `parse classical rule ... error`）。内核程序下载后放在 `temp/coretest/`（temp 不入库），下次可直接复用；`temp/gap_vs_ref.py` 是本轮的参照比对脚本，`temp/ref/` 是参照集快照。
- 2026-08-24 刻意未扩国内直连类：参照集 ChinaMax 数千条，而本库这几类是精挑的百余条，国内域名在绝大多数配置里由 `GEOSITE,cn` 或兜底直连接住，堆进来只膨胀不改行为。
- 公开规则版本：`v2026.08.24.3GoogleAITK`（22 类、909 条）。2026-08-24 首次以**高星社区规则集**为参照做覆盖率比对（blackmatrix7/ios_rule_script 33 个分类文件），补收 75 条。方法沉淀：把参照集每个域名放进本库完整匹配语义里判定是否命中，只看一条都命中不到的；**参照集噪音远大于信号**——Visa/Disney/YouTube 各有上百个国别域名全部 301 回主域，Disney 参照集 172 条里 162 条本库未命中而绝大多数是乐园/招聘/演出营销站，加密货币参照集含 FTX/Bittrex 等已倒闭交易所。可直接照搬的比例不到一成，必须逐条甄别。
- 2026-08-24 本轮补收的三处**真空**（此前完全没有任何规则覆盖，不是冗余问题）：①支付分类没有 Visa/Mastercard/American Express 三大卡组织；②流媒体只收了各家主域，Netflix/Disney+/Hulu/Prime Video/Spotify 的 CDN 承载域全缺；③`npmjs.org`（npm 实际下载端点，归 GitHub）。这类真空靠「跳转探测」发现不了——跳转探测只能找出已收录域名的迁移，找不出**从未收录过**的域。两种方法互补，下次大版本前应各跑一遍。
- 2026-08-24 判据补充（分类归属看「谁在用」而不只看「谁拥有」）：`bytedapm.com`、`ipstatp.com` 虽在参照集的 TikTok 分类里，但属字节国内外共用的监控/图床基础设施，收进 `tiktok_custom` 会把抖音流量推上代理，与 `douyin_direct_custom` 直连意图冲突，**刻意未收**；同理 `hbogo.com`/`hbonow.com` 品牌已并入 Max、只剩跳转，不在功能链路上，也未收。
- 2026-08-24 同步方向已反转，**上游不再是规则来源**：订阅工作台 2026-08-24 完成「规则集化」，面板产物直接引用本库 `release` 分支的 22 个 rule-provider（`config/panel_rule_map.yaml` 里 `base_url` 走 jsdelivr，备用 raw.githubusercontent；实测客户端加载 706 条，与本库逐条一致）。工作台的 `custom_rules.yaml` 停留在 2026-08-16，比本库旧一整轮——它与本库的 84 条差异**全部**是本库 8-17 主动清掉的冗余/失效条目（24 条经三解析器判死的错拼域已在 `CHANGELOG.md` 列明），11 条反向差异是本库 8-17 新增的迁移域。**结论：此后不要再从 `custom_rules.yaml` 往本库回灌，那等于回退；该文件应视为归档。**
- 2026-08-24 顺带核对了 VPS 管控台（`F:\AI\VPS管控台`）那套 GEOSITE 通用规则里的 3 条「救回规则」是否已被本库覆盖：`tiktokrow-cdn.com` 被 `tiktok_custom` 的 `DOMAIN-KEYWORD,tiktok` 命中、`minimax.io` 已在 `ai_api_direct_custom`，两条无需动作；`qoder.com` 曾无规则覆盖——**2026-08-24 已随官方名单合并进入 `ai_custom`（第 165 行），此条待办作废**；当日晚间核查时曾因本条未及时更新差点重复添加，靠写入前的存在性断言拦下。教训：**待办完成后必须当场把 AGENTS.md 里的原始条目改成已完成态**，跨会话的过期待办会诱导重复操作。
- 2026-08-17 全项检查补查三维度：①全 Git 历史扫描——11 个提交均无私有规则文件、无代理 URI/订阅链接；②真实内核加载——官方 Mihomo Meta v1.19.29 加载全部 22 provider + 696 条 + 推荐顺序，0 错误（方法见「怎么验证」，`-t` 不够）；③GitHub Releases 页面曾过期（Latest 停在 `v2026.07.28.2GoogleAITK`），**2026-08-17 经用户全权授权已修复**：为 `v2026.08.17.3GoogleAITK` 创建了带累计变更说明的 Release 并标记 Latest（API 确认生效）。凭据方法：Git Credential Manager 存的推送凭据可经 `git credential fill` 取出用于 GitHub API（本次实测 rate_limit 200、创建 Release 201）；仅在用户明确授权公开动作时才可这样用。发版纪律：**打 tag 后应同时建 Release**，否则仓库首页的 Latest 会误导访客。尚未做过的检查：全库 ~650 个存量域名的跳转迁移探测（8-16 只测了新增 68 条）；仓库设置层（分支保护等）需账号权限。
- 公开规则版本：`v2026.08.17.4GoogleAITK`（22 类、706 条）。2026-08-17 全库 662 域名首次迁移探测，补收 10 条真实迁移（Intercom/Runway/Phantom 迁 .com、Google Pay→Wallet、Web3Modal→Reown、`cloud.tencent.com` 等）；`validate_rules.py` 固化三道语义门禁（后缀盖后缀、关键词盖关键词、跨策略遮蔽），CI 从此能抓住 8-17 手工发现的全部三类问题，负对照已验证。甄别纪律：**跳转目标是否收录，看它是功能域还是营销页**——官网/母公司/文档页跳转（vercel.com、twilio.com、www.microsoft.com）不收，功能链路上的新域（vscode.dev、wallet.google.com）必收。
- 2026-08-17 探测方法沉淀：全库迁移探测 = 每个 DOMAIN/DOMAIN-SUFFIX 目标发一次 HEAD（DIRECT 分类直连、其余走代理），只看**跨可注册域**的跳转（same-site 的 www./路径跳转是噪音）；再对跳转目标查「是否被任何规则覆盖 + 策略组是否一致」，两问都过才算健康。60 个跨站跳转里真问题只有 16 个、值得收的只有 10 个——多数跳转是新旧域名均已收录的正常态。建议每次大版本前跑一遍（脚本模式已记于本条，temp/ 不入库）。2026-08-17 冗余审查后无损移除 79 条（53 条被同分类更宽后缀覆盖 + 26 条域名已失效），匹配行为不变，细节见 `CHANGELOG.md`。**与上游差异扩大，同步时需以本库为准整体回灌，不能逐条比对。**
- 2026-08-17 判据（不可据「主域不解析」删规则）：库内有 133 个域名主域无 A 记录，但全是 CDN 通配域（`ytimg.com`、`githubusercontent.com`、`akamai.net`、`mp.microsoft.com`、`msftconnecttest.com` 等），子域天天在用，`DOMAIN-SUFFIX` 匹配完全正常。判失效必须满足：**多个解析器均无记录 + 带对照组 + 代理亦不可达**，三者缺一不可。
- 2026-08-17 统计陷阱：查「被谁覆盖」时若对每条规则只记录**第一个**命中的覆盖者，会把同时被 `DOMAIN-KEYWORD` 和 `DOMAIN-SUFFIX` 覆盖的规则误分类。本次因此把零风险集合从 79 条误报成 49 条。统计覆盖关系必须枚举**全部**覆盖者再分类。
- 2026-08-17 **上述三项待办已在 `v2026.08.17.3GoogleAITK` 处理完毕**：腾讯分类改文档标注而**不改 provider 名**（改名会让所有已引用的配置失效，这是硬约束）；关键词与第三方 SaaS 均保留功能、补齐文档并给出移除指引。判断依据：三者都不是匹配错误，删任何一项都会造成功能回退（腾讯云直连、CDN 域名覆盖、ChatGPT 登录链），而使用者的真正困难是「无法从分类名预期范围」——那是文档问题。同时移除 4 条被同分类另一关键词覆盖的冗余关键词（700→696）。
- 2026-08-17 分析盲区：覆盖检测要枚举**四种方向**——后缀盖域名、后缀盖后缀、关键词盖域名、**关键词盖关键词**。前三种此前都查了，第四种漏了，导致 `douyinpic`（含于 `douyin`）这类冗余留到下一版才发现。
- 2026-08-17 原待办（已处理，保留原始描述备查）：① `tencent_docs_direct_custom` 名为「腾讯文档直连」，实含 `qq.com`（整个 QQ）与 `myqcloud.com`/`qcloud.com`/`tencent-cloud.net`（整个腾讯云，承载大量第三方站点资源），公开库使用者按名字无法预期此范围；② `DOMAIN-KEYWORD,adobe` / `tiktok` / `douyin` 会命中任意含该词的无关域名；③ `ai_custom` 收了 22 组通用第三方 SaaS 全域（`sentry.io`、`segment.com`、`intercom.io`、`auth0.com`、`launchdarkly.com`、`challenges.cloudflare.com`、`browser-intake-datadoghq.com` 等），ChatGPT 登录链确需，但会连带把使用者所有网站的错误上报/分析/验证码流量送进 AI 组（`openai_login_custom` 反而用 `DOMAIN,o207216.ingest.sentry.io` 这类精确写法）。三项均需用户决策后再动。2026-08-17 逐字符审查后修两处：补 `cognition.com`（`ai_custom` 165），删 `google_drive_custom` 中被 `youtube_custom` 完全覆盖的 `DOMAIN,s.ytimg.com`（44），并把 `youtube_custom` 的推荐顺序提到 `google_drive_custom` 之前。**本版未同步上游，两侧现有 2 条差异**（公开库多 `cognition.com`、少 `s.ytimg.com`），上游同步时需一并处理。
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

2026-08-17 重要：**`mihomo -t` 不解析 rule-provider 的 payload 内容**——往规则文件里塞非法规则，`-t` 照样报 successful（负对照实测）。`-t` 只验证配置结构、provider 声明、策略组引用。要验证规则本身能被内核接受，必须实际启动内核让它加载 provider（file 类型、log-level info），看日志有无 `parse classical rule ... error`；测试端口用 17890 避开常用端口，结束后按 PID 清理（bash 的 kill 对 Windows 原生进程可能无效，用 `Stop-Process -Id`，绝不能按映像名杀——会误杀正在跑的客户端）。本库 696 条已用官方核心 Mihomo Meta v1.19.29 按此法验证，0 错误 0 警告。

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
