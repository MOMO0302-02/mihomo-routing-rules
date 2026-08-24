# 规则索引

当前公开版本：`v2026.08.24.3GoogleAITK`，共 22 个分类、909 条 classical 规则。

配置中的策略名只是建议值，必须替换成你现有配置里真实存在的策略组。直连分类建议保持 `DIRECT`；其余分类可按自己的节点和地区需求映射。

| 分类 | Provider 名称 | 规则数 | 建议策略 | GitHub Raw | jsDelivr |
|---|---|---:|---|---|---|
| OpenAI 登录 | `openai_login_custom` | 29 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/openai_login_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/openai_login_custom.yaml) |
| 抖音直连 | `douyin_direct_custom` | 33 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/douyin_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/douyin_direct_custom.yaml) |
| 腾讯服务直连（含腾讯云，见下） | `tencent_docs_direct_custom` | 12 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/tencent_docs_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/tencent_docs_direct_custom.yaml) |
| YouTube | `youtube_custom` | 8 | `Streaming` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/youtube_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/youtube_custom.yaml) |
| Google Drive | `google_drive_custom` | 34 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/google_drive_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/google_drive_custom.yaml) |
| 指定 AI API 直连 | `ai_api_direct_custom` | 25 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_api_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_api_direct_custom.yaml) |
| AI API | `ai_api_custom` | 42 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_api_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_api_custom.yaml) |
| 综合 AI | `ai_custom` | 242 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_custom.yaml) |
| GitHub | `github_custom` | 15 | `GitHub` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/github_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/github_custom.yaml) |
| TikTok / CapCut | `tiktok_custom` | 45 | `TikTok` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/tiktok_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/tiktok_custom.yaml) |
| 加密货币 | `crypto_custom` | 68 | `Crypto` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/crypto_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/crypto_custom.yaml) |
| 支付 | `payment_custom` | 26 | `Payment` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/payment_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/payment_custom.yaml) |
| 流媒体 | `streaming_custom` | 39 | `Streaming` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/streaming_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/streaming_custom.yaml) |
| Microsoft Store | `microsoft_store_custom` | 22 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_store_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_store_custom.yaml) |
| Microsoft 更新 | `microsoft_update_custom` | 6 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_update_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_update_custom.yaml) |
| Microsoft 连通性检测 | `microsoft_connectivity_custom` | 2 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_connectivity_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_connectivity_custom.yaml) |
| Microsoft 服务 | `microsoft_custom` | 22 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_custom.yaml) |
| Adobe 下载直连 | `adobe_download_direct_custom` | 6 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/adobe_download_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/adobe_download_direct_custom.yaml) |
| Adobe | `adobe_custom` | 55 | `Adobe` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/adobe_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/adobe_custom.yaml) |
| 国内移动应用 | `mobile_cn_custom` | 99 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_cn_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_cn_custom.yaml) |
| 国内手游 | `mobile_cn_game_custom` | 16 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_cn_game_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_cn_game_custom.yaml) |
| 海外移动应用 | `mobile_overseas_custom` | 63 | `OtherProxy` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_overseas_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_overseas_custom.yaml) |

## 规则顺序

这些规则应放在 `GEOSITE`、`GEOIP`、`MATCH` 等兜底规则之前。仓库已在 [`examples/rules.yaml`](examples/rules.yaml) 提供建议顺序，在 [`examples/all-in-one.yaml`](examples/all-in-one.yaml) 提供可合并的完整片段。

同一域名若可能同时命中多组规则，Mihomo 按从上到下的第一条匹配结果执行，因此不要随意打乱直连、专项服务和通用服务之间的顺序。

`openai_login_custom` 是 `ai_custom` 的专项子集，两者存在有意重叠；需要为登录链单独指定地区或固定节点时，必须把 `openai_login_custom` 放在 `ai_custom` 前面。验证器会拒绝除此以外的意外跨分类重复。

`youtube_custom` 必须排在 `google_drive_custom` 前面：后者的 `DOMAIN-SUFFIX,googleapis.com` 会先行命中 `youtubei.googleapis.com`，导致 YouTube 客户端 API 落到 Google Drive 的策略组。

## 三处需要留意的范围

下面三项不是缺陷，但范围比分类名字看起来更大。按自己的需求决定是否保留，删掉对应行即可。

### 1. `tencent_docs_direct_custom` 覆盖整个腾讯生态

这个分类的名字是历史遗留，实际范围**远不止腾讯文档**：除 `docs` 相关域名外，还包含 `qq.com`（腾讯全部服务）、`myqcloud.com` / `qcloud.com` / `tencent-cloud.net`（腾讯云）以及 `gtimg.com` / `gtimg.cn` / `qpic.cn`（腾讯图床）。

其中腾讯云对象存储承载着**大量第三方网站**的静态资源，因此启用本分类等于把这些第三方资源一并设为直连。对国内网络这通常正是想要的效果；如果你的出口在境外，请自行评估。

Provider 名称保持 `tencent_docs_direct_custom` 不变——改名会让所有已引用它的配置失效。

### 2. 六个分类使用 `DOMAIN-KEYWORD`，按子串匹配

| 分类 | 关键词 |
|---|---|
| `adobe_custom` | `adobe` |
| `ai_api_custom` | `bedrock-runtime` |
| `crypto_custom` | `pokepay` |
| `douyin_direct_custom` | `douyin`、`aweme` |
| `tencent_docs_direct_custom` | `tencent-doc`、`doc.weixin` |
| `tiktok_custom` | `tik-tok`、`tiktok`、`byteoversea`、`byteintlapi` |

`DOMAIN-KEYWORD` 是**子串**匹配：`DOMAIN-KEYWORD,adobe` 会命中任何含 `adobe` 的域名，包括与 Adobe 无关的第三方域名。保留它们是因为这些服务的 CDN 域名数量多且经常变动，逐条穷举会漏；代价是匹配不够精确。对精确性要求高的场景，可以删掉关键词行，仅保留同分类内已列出的显式域名。

### 3. `ai_custom` 含 25 条通用第三方服务域名

这些不是 AI 厂商自己的域名，而是 AI 产品登录链路依赖的通用 SaaS，共 14 家：

| 用途 | 域名 |
|---|---|
| 身份认证 | `auth0.com`、`workos.com`、`workoscdn.com`、`workos.imgix.net` |
| 人机验证 | `arkoselabs.com`、`funcaptcha.com`、`challenges.cloudflare.com` |
| 功能开关 | `statsig.com`、`statsigapi.net`、`featuregates.org`、`featureassets.org`、`launchdarkly.com` |
| 监控与分析 | `sentry.io`、`browser-intake-datadoghq.com`、`segment.io`、`segment.com`、`segmentapis.com` |
| 客服与消息 | `intercom.io`、`intercomcdn.com`、`intercomassets.com`、`ct.sendgrid.net` |
| 其他 | `livekit.cloud`、`prodregistryv2.org`、`humb.apple.com`、`register.appattest.apple.com` |

**这些服务被成千上万个网站使用。** 启用 `ai_custom` 后，你访问任何网站时其错误上报、行为分析、验证码等流量都会一并进入 AI 策略组，而不只是 AI 网站的。

保留是因为缺了它们 ChatGPT 等产品的登录会卡住——这条链路上的验证码、功能开关和认证请求都必须与主站走同一出口。如果你只用 API 而不需要网页登录，可以删掉这 25 行。

作为对照，`openai_login_custom` 对同类服务采用了精确写法（如 `DOMAIN,o207216.ingest.sentry.io`），只覆盖 OpenAI 实际使用的那几个主机。

### 4. `github_custom` 含 `blob.core.windows.net`，范围是整个 Azure 对象存储

`github_custom` 里有一条 `DOMAIN-SUFFIX,blob.core.windows.net`。它原本是为 GitHub 的部分产物下载而收，但 `*.blob.core.windows.net` 是 **Azure 对象存储的通用域名**，被大量第三方网站用来托管文件——启用本分类等于把这些站点的文件下载一并送进 GitHub 策略组。

与第 3 条同类：不是匹配错误，但使用者无法从分类名预期这个范围。若你的 GitHub 用法不涉及需要该域名的产物下载，可以删掉这一行。

注意 `ai_custom` 里的 `openaiassets.blob.core.windows.net` 是更精确的写法，且 `ai_custom` 在推荐顺序中排在 `github_custom` 之前，因此 OpenAI 的资源不受这条影响。
