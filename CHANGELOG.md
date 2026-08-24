# Changelog

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
