# Changelog

## v2026.08.26.1GoogleAITK

### Fixes

- `ai_custom` 删除 `PROCESS-NAME,codex.exe` 与 `PROCESS-NAME,claude.exe` 两行（249 → 247）：**「大小写双写」的前提是错的**。mihomo 的进程名匹配走 `rules/common/process.go` 的 `strings.EqualFold(target, ps.pattern)`，**本就忽略大小写**（通配与正则分支同样带 `IgnoreCase`）。因此 `codex.exe` 相对 `Codex.exe` 永远不可能多匹配到任何东西，纯属死行。v2026.08.25.3 引入 Claude双写时所称的「沿用 Codex 双写先例」据此作废，`Codex.exe`/`Claude.exe` 单写即可覆盖全部大小写形态。
- `ai_api_direct_custom` 删除 `DOMAIN-SUFFIX,api.deepseek.com`（25 → 24，总量 929）：该条与 `ai_custom` 的 `DOMAIN-SUFFIX,deepseek.com` 冲突且**永远不生效** —— 在订阅工作台的推荐顺序里 AI 组排在直连组之前，先匹配者赢。使用方确认最终意图就是**DeepSeek 走 AI 代理组**，故删除这条表达相反意图的死行。
  ⚠️ 删除理由**不是**「上游 geosite 已收录」（该判据见 2026-08-25，仍然有效、未被动摇），而是**本库内部两条规则意图冲突、且已确认最终意图**。两者是不同的问题。

## v2026.08.25.3GoogleAITK

### Rules

- `ai_custom` 新增 `PROCESS-NAME,Claude.exe` 与 `PROCESS-NAME,claude.exe`（247 → 249，总量 932）：Claude Code CLI 与 Claude 桌面版的进程级兜底，沿用库内 `Codex.exe`/`codex.exe` 大小写双写先例。进程规则的价值是**在域名尚未被收录时就把该进程的全部流量兜进 AI 组**——本周两次 Datadog 遥测域漏网（browser-intake 族、logs 族）正是这类问题：域名会不断冒新，进程不会。实测本机 `claude.exe` 进程在跑而库内此前无任何 Claude 进程规则（ChatGPT/Codex/Adobe 均有）。

## v2026.08.25.2GoogleAITK

### Fixes

- `ai_custom` 新增 `DOMAIN-SUFFIX,datadoghq.com`（246 → 247，总量 930）：实时监控工具首跑 60 秒即抓到 `http-intake.logs.us5.datadoghq.com` 落兜底——Datadog 的**日志**上报族与已修的 browser-intake（浏览器遥测）是两条独立链路，且它是 `datadoghq.com` 的真子域，收主域后缀一条管住所有区域的 logs/rum 子域，与库内 `sentry.io` 全域收录先例一致。DoH 验活。`browser-intake` 关键词保留（负责 datadoghq.com 之外的兄弟注册域形态）。

### Tooling

- `watch_fallback.py` 支持 **Windows 命名管道自动发现**：Clash Party / Mihomo Party 不开 TCP 外部控制器、改用命名管道驱动内核，本工具现可直接发现并接入该管道（HTTP over named pipe，支持 chunked 解码），**零设置开箱即用**；TCP 控制器路径保留（`--controller`/`--secret`，`--no-pipe` 可禁用管道发现）。实测 60 秒采样即产出三类分级报告（未覆盖候选 / 已覆盖但配置未引用 / 兜底干净）。

## v2026.08.25.1GoogleAITK

### Fixes

- `tiktok_custom` 新增 `DOMAIN-KEYWORD,capcut`（45 → 46，总量 929）：修复上一版共性扫描确认的唯一真风险。CapCut 一族在库内已呈现三种兄弟域形态（`capcutapi.com`/`.us` 换尾、`capcutcdn-us.com` 区域中缀、`capcutstatic.com` 职能拆分），后缀匹配接不住未来新区域（如 `capcutcdn-eu.com`、`capcutapi-sg.com`）。采用品牌关键词与既有 `tiktok`/`douyin`/`adobe` 先例一致；矩阵验证现有域全部仍命中、假想新区域全部接住、无误伤。7 条显式后缀按惯例保留作文档与退路。`RULES.md` 关键词表已同步。

## v2026.08.24.7GoogleAITK

### Fixes

- `ai_custom` 中 `DOMAIN-SUFFIX,browser-intake-datadoghq.com` 改为 `DOMAIN-KEYWORD,browser-intake`（总量保持 928）。Datadog 按区域拆分为**兄弟注册域**（`browser-intake-us5-datadoghq.com` / `us3` / `ap1` …），中缀多了区域标识，后缀匹配全部接不住；实测客户端上 `browser-intake-us5-datadoghq.com` 落到兜底 Match，未进 AI 组。关键词写法经矩阵验证：原域、`rum.` 子域、全部区域变体乃至 `.eu` 顶级域形态均命中，`example.com` 类无误伤。`RULES.md` 关键词表已同步（第七个使用关键词的分类）。
- `openai_login_custom` 的 `DOMAIN,rum.browser-intake-datadoghq.com` 为刻意精确写法，**保持不动**；其区域变体由 `ai_custom` 的关键词兜住（默认映射同为 AI 组）。

### Tooling

- 新增 `tools/watch_fallback.py`：连接客户端的外部控制接口实时采样连接表，聚合**落到兜底 Match 的主机**并对照本库判断是否已覆盖，输出收录候选清单——把「盯连接面板发现漏网域名」这件事自动化（本次 Datadog 缺口正是靠肉眼盯出来的）。需在客户端开启外部控制。

## v2026.08.24.6GoogleAITK

### Rules

- 月检工作流首跑（[#1](https://github.com/MOMO0302-02/mihomo-routing-rules/issues/1)）在干净网络环境下抓到 2 个死域，双端 DoH 复核确认后移除：`desktop.chat.openai.com`（OpenAI 已弃用）与 `models.inference.ai.azure.com`（GitHub Models 旧端点）。后者属迁移而非消失，补收新端点 `models.github.ai`（DoH 验活）。总量 929 → 928。

### Automation

- `probe_migration.py` 支持已甄别名单 `tools/probe_known.txt`（按「来源域+目标可注册域」成对匹配）：8 组已人工判定为营销页跳转的条目不再触发月报；同一来源日后跳向新目标时因指纹不同仍会重新报告。实测全库探测 flagged 归零。

## v2026.08.24.5GoogleAITK

### Rules

- `ai_custom` 补收 3 条（246，总量 929）：`ppl-ai-file-upload.s3.amazonaws.com` 与 `pplx-res.cloudinary.com`（Perplexity 的文件上传桶与静态资源——主站早已收录而上传链路缺失，属「同链路必须同出口」缺口）、`clawhub.ai`（OpenClaw 技能市场，`openclaw.ai`/`claw.cloud` 均已在库）。三条均 DoH 验活。
- 官方名单中的 `comfyci.org` 经 DoH 判定 **NXDOMAIN（死域）**，不予收录——官方 geosite 同样会携带过期条目，引用前必须逐条验活。

### Automation

- 新增**每月自动体检**工作流（`monthly-health.yml`，每月 1 号）：在 GitHub 服务器上跑全库迁移探测 + DoH 死域检测 + 官方名单差距报告，发现需人工甄别的事项自动开 Issue；全干净则静默。
- `geosite_gap.py` 入库：拉取官方 MetaCubeX geosite 名单与本库比对，输出未覆盖条目。配套 `tools/geosite_rejected.txt`（已否决名单，22 条，含否决理由）——被人工甄别剔除的条目不再重复出现在月报中，移出该文件即恢复报告。当前对官方 `category-ai-!cn` 的差距为 **0**。

## v2026.08.24.4GoogleAITK

### New category

- 新增第 23 个分类 **`ntp_direct_custom`（时间同步直连，16 条）**：`ntp.org` 全生态、Windows/Apple/Android/Google/Cloudflare/NIST 的时间服务器、阿里/腾讯/国家授时中心的国内源。时间同步（NTP）走代理会静默失败或漂移，进而引发证书校验错误与登录异常；官方 geosite **没有** ntp 分类（实测 404），只能自建。16 条全部经 DoH 存活验证。
- 推荐顺序中 `ntp_direct_custom` 放在**最前**：`time.windows.com` 若排在 Microsoft 分类之后会被 `windows.com` 后缀先命中而走代理，时间同步属于必须最先直连放行的基础设施。

### Automation

- CI 新增 **真内核加载门禁**（`core-load` job）：每次推送自动下载官方 Mihomo（版本钉在 workflow 的 `MIHOMO_VERSION`）实际加载全部 23 个 provider，出错即红。此前这一金标准只能手动跑——`mihomo -t` 不解析 provider 内容，校验器也替代不了内核本身。
- 新增 **tag 推送自动建 GitHub Release**（`release.yml`）：Release 正文取自 `CHANGELOG.md` 对应版本节，杜绝「打了 tag 忘发 Release、首页 Latest 过期」的人为疏漏。
- 新增 **release 分支推送自动清 jsDelivr 缓存**（`purge-cdn.yml`）：此前新版本要等 CDN 缓存自然过期（最长 12 小时以上）才对 jsDelivr 用户生效，现在发布即生效。

### Tooling

- 三个此前每轮临时重写的体检脚本正式入库 `tools/`：`coretest.py`（真内核加载测试，CI 与本地共用）、`check_liveness.py`（DoH 测活，内置强制对照组，对照不过整批拒绝出结果）、`probe_migration.py`（全库跨站跳转探测 + 目标覆盖/策略一致性分析）。`changelog_section.py` 供 Release 工作流提取版本说明。

## v2026.08.24.3GoogleAITK

### Rules

- 与**官方维护的 `geosite:category-ai-!cn`**（mihomo 内核自带地理数据库，MetaCubeX 维护）做双向比对，取「结合方案」：官方名单 179 条里本库一条都没覆盖的有 85 条，逐条甄别后收 **61 条**，`ai_custom` 181 → 242，总量 848 → 909。
- 收录的主要是四类：
  - **已收厂商的另一个域名**：`perplexity.com`、`cohere.ai`、`elevenlabs.com`、`kimi.ai`、`moonshot.ai`、`copilot.com`、`clau.de`、`hf.co`、`hf.space`、`poecdn.net`、`manuscdn.com`、`cursor-cdn.com`、`codeiumdata.com`、`windsurf.build`——多数是 301 到已收主域的第一跳，此前跳转起点无规则命中。
  - **Google AI 的 `.com` 一侧**：`ai.studio`、`bard.google.com`、`jules.google.com`、`labs.google.com`、`notebook.google.com`、`opal.google.com`、`antigravity-unleash.goog`。本库此前只收了 `.google` gTLD 那一侧，是同一个失效模式的另一半。
  - **新产品**：`kiro.dev`、`coderabbit.ai`、`deepwiki.com`/`.org`、`jetbrains.ai` 与 `grazie.ai`/`grazie.aws.intellij.net`、`comfy.org`/`comfyregistry.org`、`crewai.com`、`duck.ai`、`grokipedia.com`、`h2o.ai`、`jasper.ai`、`lovart.ai`、`mozilla.ai`、`novelai.net`、`openart.ai`、`sider.ai`、`tripo3d.ai`、`anythingllm.com`、`clipdrop.co`、`diabrowser.com`、`openspec.dev`、`agentclientprotocol.com`。
  - **字节 Coze / Cici**：`coze.com`、`cici.com`、`ciciai.com`、`ciciaicdn.com`，以及 `dola.com`——实测 `cici.com` 与 `ciciai.com` 均已 301 至 `www.dola.com`，属品牌更名，新旧域一并收。
  - 另补 OpenAI / Anthropic 的资源域：`oaistatsig.com`、`openaicom.imgix.net`、`openaiassets.blob.core.windows.net`、`openai.com.cdn.cloudflare.net`、`production-openaicom-storage.azureedge.net`、`openaicom-api-*.z01.azurefd.net`、`servd-anthropic-website.b-cdn.net`。
- **官方名单里刻意不收的 24 条**：`envato.com` / `themeforest.net` / `envatousercontent.com`（素材交易市场，与 AI 无关）、`liveperson.net` / `lpsnmedia.net`（通用客服 SaaS，属本库既有的「通用第三方服务」谨慎范围）、`openai.qualtrics.com`（问卷）、`copilot-stg.com`（预发布环境）、`coderabbit.gallery.vsassets.io`（VS Code 市场 CDN，范围过宽），以及 `talkai.info`、`spicywriter.com`、`notegpt.io`、`oystermercury.top` 等镜像站与小众站。`comfyci.org` 剔除：无 NS 记录，域名已不存在。
- 反向差异也记录在案：**本库有、官方名单没有的 118 条**，主要是 ChatGPT 登录链路依赖的通用 SaaS（缺了登录会卡住）、按「面向国际」判据收的国产 AI 国际站（`kimi.com`、`z.ai`、`qwen.ai`），以及一批厂商主域。两份名单定位不同——官方回答「是不是 AI 网站」，本库还要回答「该走哪个出口」，因此**互为补充而非替代**。
- 一处官方与本库的**有意分歧**：官方把 `minimax.io` 归入 AI（走代理），本库放在 `ai_api_direct_custom`（直连），沿用既有决策不改。

### Documentation

- `RULES.md`「需要留意的范围」新增第 4 条：`github_custom` 里的 `DOMAIN-SUFFIX,blob.core.windows.net` 实际覆盖**整个 Azure 对象存储**，大量第三方网站用它托管文件。与既有第 3 条同类——不是匹配错误，但使用者无法从分类名预期该范围，已给出移除指引。

## v2026.08.24.2GoogleAITK

### Fixes

- 修 `v2026.08.24.1GoogleAITK` 的 `manifest.json`：其中 9 个规则文件的 SHA-256 是在 **CRLF 换行**的本地工作副本上算的，而 Git 按 `.gitattributes` 统一存成 LF，导致按 manifest 校验线上文件必然对不上（本地验证器通过、CI 报 9 条 `manifest SHA-256 mismatch`）。**规则内容本身没有任何问题**，受影响的只是校验值字段。本版已把全部文件归一为 LF 并重算。
- `validate_rules.py` 新增一道门禁：规则文件出现 CRLF 直接报错。这类问题在 Windows 上写文件时静默产生，本地和 CI 会给出相反结论——固化成门禁后本地就能拦下。已负对照验证（注入 CRLF 报错、还原后通过）。

### Rules

- 规则内容与 `v2026.08.24.1GoogleAITK` 完全一致：22 个分类、848 条。

## v2026.08.24.1GoogleAITK

### Rules

- 以**高星社区规则集**（blackmatrix7/ios_rule_script 的 33 个分类规则文件）为参照做覆盖率比对，补收 **75 条**（706 → 781），分类保持 22 个。比对方法：把参照集里的每个域名放进本库的完整匹配语义（后缀/精确/关键词）里判定「本库是否命中」，只看**一条都命中不到**的域名；对命中不到的再逐条甄别是否值得收录。
- 参照集的噪音远大于信号，**刻意不收**的大类已记录在案：Visa/Disney/YouTube 的上百个国别域名（`visa.com.br`、`disney.fr`、`youtube.co.uk` 等，全部 301 回主域，且本库收主域已够）、Disney 的乐园/招聘/演出等营销站、加密货币参照集里已倒闭的交易所（FTX、Bittrex、Bibox）与资讯站，以及 `identrust.com`、`onetrust.com`、`cookielaw.org`、`algolia.net` 这类被成千上万网站共用的通用第三方服务。
- **综合 AI +18**（163 → 181）：`qoder.com`（阿里国际版 AI 编程工具，`geosite:cn` 会把它误判为国内而直连）、`trae.ai` 与 `marscode.com`（字节 Trae，实测 `marscode.com` 已改版为 Trae 站点）、`deepmind.com`（301 → 已收录的 `deepmind.google`，第一跳此前无规则）、`generativeai.google` 与 `ai.google`（`.google` gTLD，前者 302 → 后者，两侧此前均无覆盖）、`ai.com`、`ollama.com`、`lmstudio.ai`、`wandb.ai`、`langchain.com`、`llamaindex.ai`、`blackforestlabs.ai` 与 `bfl.ai`（前者 301 → 后者）、`recraft.ai`、`assemblyai.com`、`deepgram.com`、`colab.research.google.com`。
- **加密货币 +29**（39 → 68）：交易所 `bitfinex.com`、`bitstamp.net`、`gemini.com`、`bithumb.com`、`upbit.com`、`backpack.exchange`、`hyperliquid.xyz`；钱包与硬件 `ledger.com`、`trezor.io`、`rabby.io`、`safe.global`、`exodus.com`；链上数据 `blockchain.com`、`bscscan.com`、`debank.com`、`defillama.com`、`dune.com`；公链与 DeFi `arbitrum.io`、`solana.com`、`aave.com`、`lido.fi`、`jup.ag`、`curve.fi` 与 `curve.finance`（前者 302 → 后者）、`1inch.io` 与 `1inch.com`（前者 301 → 后者）；NFT `opensea.io`、`blur.io`、`magiceden.io`。
- **流媒体 +14**（17 → 31）：Netflix `netflix.net`、`nflxsearch.net`、`nflximg.com`、`fast.com`；Disney+ `bamgrid.com`、`disneystreaming.com`、`dssedge.com`；Hulu `hulustream.com`、`huluim.com`；Prime Video `aiv-cdn.net`、`aiv-delivery.net`、`pv-cdn.net`；Spotify `spotifycdn.com`、`spotifycdn.net`。这 14 条里有 12 条主域不响应 HTTP——按本库既有判据（见 `v2026.08.17.2GoogleAITK`「不可据主域不解析判定失效」）改查 NS，全部托管在 AWS Route 53 / NS1 / Akamai 上，是正常的 CDN 通配域。
- **支付 +10**（16 → 26）：`visa.com`、`mastercard.com`、`americanexpress.com` 三大卡组织此前**完全没有覆盖**；另补 `revolut.com`、`skrill.com`、`squareup.com`、`adyen.com`、`paddle.com`、`lemonsqueezy.com`、`remitly.com`。
- **GitHub +2**（13 → 15）：`npmjs.com` 与 `npmjs.org`（npm 归 GitHub，`registry.npmjs.org` 是实际的包下载端点）。
- **TikTok +2**（43 → 45）：`ttwebview.com`、`sgpstatp.com`。同批参照集里的 `bytedapm.com` 与 `ipstatp.com` **刻意未收**——这两个是字节国内外共用的监控与图床基础设施，收进 TikTok 分类会把抖音/今日头条的流量一并推上代理，与 `douyin_direct_custom` 的直连意图冲突。
- 已收录的 `hbogo.com` / `hbonow.com` 候选被剔除：HBO Go 与 HBO Now 两个品牌均已并入 Max，域名仅剩跳转，功能链路上不再出现。
- 第二轮把参照比对扩到此前没动过的四个分类，再补 **67 条**（781 → 848）：
  - **微软 4 → 22**：原分类只有 Xbox 与 `live.com`、`msedge.net` 四条，**OneDrive / SharePoint / Office 全无覆盖**。补 `onedrive.com`、`1drv.com`、`1drv.ms`、`livefilestore.com`、`microsoftpersonalcontent.com`、`oneclient.sfx.ms`、`sharepoint.com`、`sharepointonline.com`、`office.com`、`office.net`、`office365.com`、`outlook.com`、`microsoftonline.com`、`msauth.net`、`msftauth.net`、`msidentity.com`、`aka.ms`，以及 **`cloud.microsoft`**——实测 `office.com` 已 302 至 `m365.cloud.microsoft`，这是微软新启用的统一应用域，此前无任何规则命中。`skype.com` 候选剔除：Skype 已并入 Teams，跳转目标 `teams.live.com` 本就被 `live.com` 覆盖。
  - **境外常用 28 → 63**：补 Reddit（4）、LinkedIn（2）、Pinterest（2）、Quora（2）、Snapchat（2）、Slack（2）、Notion（3，`notion.so` / `notion.site` 均 301 至新主域 `notion.com`）、Dropbox（2）、Zoom（2，`zoom.us` 301 至 `zoom.com`）、SoundCloud（2）、Stack Overflow（2）、Wikipedia / Wikimedia、Medium、Tumblr、Signal、Figma、Imgur、Vimeo、DuckDuckGo、LINE。
  - **流媒体 31 → 39**：Twitch（`twitch.tv`、`ttvnw.net`、`jtvnw.net`）、Crunchyroll、Paramount+、Peacock、DAZN、Apple TV+（`tv.apple.com`）。
  - **Adobe 49 → 55**：`creativecloud.com`、`creativesdk.com`、`echosign.com`、`adobesign.com`、`2o7.net`（NS 实为 `ns201.adobe.net`，与库内既有的 `demdex.net` / `omtrdc.net` 同属 Adobe 分析域）、`macromedia.com`。
- **国内直连类（`mobile_cn_custom` 等）本轮刻意未扩**：参照集的 ChinaMax 有数千条，而本库这几个分类是精挑的百余条；国内域名在绝大多数配置里本就由 `GEOSITE,cn` 或兜底直连接住，逐条堆进来只会让文件膨胀而不改变行为。

### Verification

- 全部 848 条经**官方核心 Mihomo Meta v1.19.30** 实际加载验证（22 个 file 类型 provider + 推荐顺序，`log-level: info`）：**0 错误 0 警告**。
- 同时做了**负对照**：向 `payment_custom` 注入一条 `NOT-A-RULE-TYPE,broken.example`，内核如实报 `parse classical rule ... error: unsupported rule type`，确认该验证确实能发现问题；随后已还原。

- 全部 75 条均经代理侧 HTTP 探测或 NS 记录双重确认存活；三道语义门禁（后缀盖后缀、关键词盖关键词、跨策略遮蔽）在补收后仍为 0 告警。

## v2026.08.17.4GoogleAITK

### Rules

- 对**全库存量域名**首次做迁移探测（662 个域名逐个发请求，此前只测过 8-16 新增的 68 条），发现 60 个跨站跳转；逐个甄别后**补收 10 条真实迁移/缺口**（696 → 706），其余为新旧域名均已收录的正常跳转或不应收录的官网营销跳转：
  - `vscode.dev`（GitHub：`github.dev` 的实际编辑器域）
  - `cdn-dynmedia-1.microsoft.com`、`microsoftstore.com`（Microsoft Store：图片 CDN 已从 akamaized.net 迁来；商店新域）
  - `windows.microsoft.com`（Microsoft 更新：`windows.com` 的跳转目标）
  - `intercom.com`、`runway.com`（AI：Intercom 与 Runway 均已把主域迁到 .com，此前只收了 `intercom.io` / `runwayml.com`）
  - `wallet.google.com`（支付：Google Pay 已并入 Google Wallet）
  - `phantom.com`、`reown.com`（加密货币：Phantom 钱包由 `.app` 迁至 `.com`；WalletConnect 的 Web3Modal 品牌重塑为 Reown）
  - `cloud.tencent.com`（腾讯直连：`qcloud.com` 的跳转目标，此前未覆盖会落 MATCH 走代理）
- 甄别中刻意不收的跳转目标：`vercel.com`（通用托管平台官网，收进 AI 属过宽）、`www.twilio.com`（Segment 母公司官网）、`www.microsoft.com` / `developers.google.com`（营销/文档页跳转，功能域名均已覆盖）。

### Validator

- `validate_rules.py` 新增三道语义门禁，把 2026-08-17 手工审查发现的三类问题固化进 CI：①同分类内 `DOMAIN-SUFFIX` 被更宽后缀覆盖；②同分类内 `DOMAIN-KEYWORD` 含另一关键词为子串；③**跨策略遮蔽**——规则被推荐顺序中更靠前、且建议策略不同的分类先行命中（即 `youtubei.googleapis.com` 那类永不生效的规则）。三道门禁均经负对照验证（注入违规规则确认报错、恢复后通过）。同策略遮蔽与分类内关键词盖域名仍属有意设计，不报错。
- 全部 706 条经官方核心 Mihomo Meta v1.19.29 实际加载验证，0 错误。

## v2026.08.17.3GoogleAITK

### Rule quality

- 移除 4 条被同分类另一个关键词完全覆盖的 `DOMAIN-KEYWORD`：`douyinpic` 与 `douyincdn` 已含于 `douyin`，`tiktokcdn` 与 `tiktokv` 已含于 `tiktok`（关键词按子串匹配）。700 → 696 条，分类保持 22 个，**匹配行为不变**。
- 上一版的覆盖分析只检查了「关键词覆盖域名」，未检查「关键词覆盖关键词」，因此漏掉这 4 条。

### Documentation

补上三处「范围比分类名字更大」的说明，`RULES.md` 新增「三处需要留意的范围」章节。三者都不是缺陷，但使用者无法从分类名预期其范围，此前没有任何文档提示。

- **`tencent_docs_direct_custom` 实际覆盖整个腾讯生态**：除腾讯文档外还含 `qq.com`（腾讯全部服务）、`myqcloud.com` / `qcloud.com` / `tencent-cloud.net`（腾讯云）与 `gtimg.com` / `gtimg.cn` / `qpic.cn`（腾讯图床）。腾讯云对象存储承载大量第三方网站的静态资源，启用本分类等于把这些资源一并设为直连。**Provider 名称刻意不改**——改名会让所有已引用它的配置失效；改的是文档标注与说明。
- **六个分类使用 `DOMAIN-KEYWORD`**，按子串匹配，会命中含该词的无关域名。现已在 `RULES.md` 列出全部 11 个关键词及其所属分类，并说明保留原因（这些服务的 CDN 域名多且常变，穷举会漏）与移除方式。
- **`ai_custom` 含 25 条通用第三方服务域名**（14 家：Auth0、WorkOS、Arkose、Cloudflare Turnstile、Statsig、LaunchDarkly、Sentry、Datadog、Segment、Intercom、SendGrid、LiveKit 等）。这些服务被成千上万个网站使用，启用 `ai_custom` 后访问任何网站时其错误上报、行为分析与验证码流量都会进入 AI 策略组。保留是因为缺了它们 ChatGPT 等产品的登录会卡住；文档已列出完整清单，只用 API 的使用者可自行删除这 25 行。
- 同时补充记录：`youtube_custom` 必须排在 `google_drive_custom` 之前的原因。

## v2026.08.17.2GoogleAITK

### Rule quality

- 全库冗余审查后**无损移除 79 条规则**，779 → 700 条，分类保持 22 个。**匹配行为完全不变**，已逐条验证。
- **53 条被同分类内更宽的 `DOMAIN-SUFFIX` 完全覆盖**：例如 30 条 `*.adobe.com` / `*.adobe.io` 子域被 `adobe.com` / `adobe.io` 覆盖、5 条 `*.mp.microsoft.com` 被 `mp.microsoft.com` 覆盖、4 条 `cos.ap-*.myqcloud.com` 被 `myqcloud.com` 覆盖、`events.openai.com` 与 `cdn.openai.com` 被 `openai.com` 覆盖等。等价性验证：对每条被删规则的主域与一个探针子域比对新旧归属，**归属变化 0 个**。
- **26 条域名已失效**：在 AliDNS、DNSPod、AliDNS 备用三个解析器上均无记录，经代理亦不可达，测试带对照组（`baidu.com` 正常解析、构造的假域名正常失败）。其中多条本就是写错或已改版的域名，且**正确域名早已在库内**——`bankcomm.com.cn`→`bankcomm.com`、`12123.gov.cn`→`122.gov.cn`、`12306img.cn`→`12306.cn`、`meituanimg.com`→`meituan.com`、`disneypluscdn.com`→`disneyplus.com`、`api.openrouter.ai`/`api.windsurf.com`/`api.luma.ai`→各自主域。另有 `login.openai.com`（OpenAI 已改用 `auth.openai.com`）、Google 已退役的 `clients0/7/8/9.google.com` 与 `lh0/1/7/8/9.google.com`。
- `api.openrouter.ai` 属规则本身写错：OpenRouter 的接口是 `openrouter.ai/api/v1`，从来没有 `api.` 子域。

### Not changed

- 保留 32 条被更早分类覆盖而不可达的规则：这些分类策略相同，当前无行为影响，但使用者若重新映射策略组即会生效，删除反而埋雷。
- 保留全部 `DOMAIN-KEYWORD` 及其覆盖的显式后缀。
- 133 个主域无 A 记录的域名**全部保留**：`ytimg.com`、`githubusercontent.com`、`akamai.net`、`mp.microsoft.com`、`msftconnecttest.com` 等属 CDN 通配域，主域本就不解析而子域在用，`DOMAIN-SUFFIX` 匹配正常。**不可据「主域不解析」判定规则失效。**

## v2026.08.17.1GoogleAITK

### Fixes

- 对全库做逐字符审查后修复两处问题。总量保持 779 条（+1 −1），分类仍 22 个。
- **补收 `cognition.com`**（`ai_custom` 164 → 165）：上一版新增的 `cognition.ai` 实测已 301 迁移至 `cognition.com`，而后者不被任何规则覆盖。属上一版遗漏——与该版专门修复的「域名迁移导致规则静默失效」是同一类问题。
- **`youtubei.googleapis.com` 此前永远匹配不到**，自首个公开版本 `v2026.07.28.1GoogleAITK` 起即存在：该规则在 `youtube_custom`（建议策略 `Streaming`），却被推荐顺序中更靠前的 `google_drive_custom` 的 `DOMAIN-SUFFIX,googleapis.com`（建议策略 `AI`）先行命中，导致 YouTube 客户端的 API 请求落到 AI 策略组，解锁类节点配置随之失效。
  - 两个分类存在双向覆盖，只调顺序会把冲突推到另一侧，因此一并处理：`google_drive_custom` 的 `DOMAIN,s.ytimg.com` 已被 `youtube_custom` 的 `DOMAIN-SUFFIX,ytimg.com` 完全覆盖，属跨文件冗余，予以移除（45 → 44）；同时在 `examples/rules.yaml` 与 `examples/all-in-one.yaml` 中把 `youtube_custom` 提到 `google_drive_custom` 之前。
  - 修复后全库跨策略遮蔽为 **0 条**。
  - **已按旧顺序把推荐规则复制进自己配置的使用者，需要重新复制一次才能拿到此修复。**
- 仍有 32 条规则被更早的分类覆盖而不可达，但策略相同（主要是 `ai_custom` 与 `openai_login_custom` 的有意重叠，见 `RULES.md`），无行为影响。

### Notes

- 验证器只检查单文件内的语义冗余，跨分类的遮蔽需要结合推荐顺序单独分析，`validate_rules.py` 不覆盖这一层。
- 本版仅在公开库落地，未同步上游规则源：两侧当前有 2 条差异（公开库多 `cognition.com`、少 `google_drive_custom` 的 `s.ytimg.com`）。

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
