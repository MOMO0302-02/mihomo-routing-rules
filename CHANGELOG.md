# Changelog

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
