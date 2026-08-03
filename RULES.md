# 规则索引

当前公开版本：`v2026.08.02.5GoogleAITK`，共 22 个分类、711 条 classical 规则。

配置中的策略名只是建议值，必须替换成你现有配置里真实存在的策略组。直连分类建议保持 `DIRECT`；其余分类可按自己的节点和地区需求映射。

| 分类 | Provider 名称 | 规则数 | 建议策略 | GitHub Raw | jsDelivr |
|---|---|---:|---|---|---|
| OpenAI 登录 | `openai_login_custom` | 30 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/openai_login_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/openai_login_custom.yaml) |
| 抖音直连 | `douyin_direct_custom` | 36 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/douyin_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/douyin_direct_custom.yaml) |
| 腾讯文档直连 | `tencent_docs_direct_custom` | 17 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/tencent_docs_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/tencent_docs_direct_custom.yaml) |
| Google Drive | `google_drive_custom` | 45 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/google_drive_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/google_drive_custom.yaml) |
| 指定 AI API 直连 | `ai_api_direct_custom` | 25 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_api_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_api_direct_custom.yaml) |
| AI API | `ai_api_custom` | 46 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_api_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_api_custom.yaml) |
| 综合 AI | `ai_custom` | 96 | `AI` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/ai_custom.yaml) |
| GitHub | `github_custom` | 12 | `GitHub` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/github_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/github_custom.yaml) |
| TikTok / CapCut | `tiktok_custom` | 46 | `TikTok` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/tiktok_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/tiktok_custom.yaml) |
| 加密货币 | `crypto_custom` | 38 | `Crypto` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/crypto_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/crypto_custom.yaml) |
| 支付 | `payment_custom` | 16 | `Payment` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/payment_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/payment_custom.yaml) |
| 流媒体 | `streaming_custom` | 18 | `Streaming` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/streaming_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/streaming_custom.yaml) |
| Microsoft Store | `microsoft_store_custom` | 27 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_store_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_store_custom.yaml) |
| Microsoft 更新 | `microsoft_update_custom` | 7 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_update_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_update_custom.yaml) |
| Microsoft 连通性检测 | `microsoft_connectivity_custom` | 2 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_connectivity_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_connectivity_custom.yaml) |
| Microsoft 服务 | `microsoft_custom` | 4 | `Microsoft` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/microsoft_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/microsoft_custom.yaml) |
| Adobe 下载直连 | `adobe_download_direct_custom` | 9 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/adobe_download_direct_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/adobe_download_direct_custom.yaml) |
| Adobe | `adobe_custom` | 81 | `Adobe` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/adobe_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/adobe_custom.yaml) |
| 国内移动应用 | `mobile_cn_custom` | 103 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_cn_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_cn_custom.yaml) |
| 国内手游 | `mobile_cn_game_custom` | 16 | `DIRECT` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_cn_game_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_cn_game_custom.yaml) |
| 海外移动应用 | `mobile_overseas_custom` | 28 | `OtherProxy` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/mobile_overseas_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/mobile_overseas_custom.yaml) |
| YouTube | `youtube_custom` | 9 | `Streaming` | [Raw](https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/youtube_custom.yaml) | [CDN](https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/youtube_custom.yaml) |

## 规则顺序

这些规则应放在 `GEOSITE`、`GEOIP`、`MATCH` 等兜底规则之前。仓库已在 [`examples/rules.yaml`](examples/rules.yaml) 提供建议顺序，在 [`examples/all-in-one.yaml`](examples/all-in-one.yaml) 提供可合并的完整片段。

同一域名若可能同时命中多组规则，Mihomo 按从上到下的第一条匹配结果执行，因此不要随意打乱直连、专项服务和通用服务之间的顺序。

`openai_login_custom` 是 `ai_custom` 的专项子集，两者存在有意重叠；需要为登录链单独指定地区或固定节点时，必须把 `openai_login_custom` 放在 `ai_custom` 前面。验证器会拒绝除此以外的意外跨分类重复。
