# ZCode 全局能力参考

当前 ZCode 运行环境的完整能力清单。供 AI 代理在生成代码、回答问题、调用工具时参考。

> 最后更新：2026-08-13

---

## 1. AI 提供商与模型

| 提供商 | 类型 | 模型 | 上下文 | 输出上限 | 推理 |
|--------|------|------|--------|---------|------|
| **DeepSeek 官方** | openai-compatible | `deepseek-v4-flash` | 1,000,000 | 384,000 | off/high/max（默认 max） |
| **云枢智联** | openai-compatible | `deepseek-v4-flash` | 1,000,000 | 384,000 | off/high/max（默认 max） |

**默认模型（CLI）：** `deepseek/deepseek-v4-flash`

**代理模型覆盖：** 通用代理和 Explore 代理均使用云枢智联的 `deepseek-v4-flash`，推理模式为 `max`。

---

## 2. MCP 服务器（工具）

### 2.1 Chrome DevTools

- **协议：** stdio (`npx -y chrome-devtools-mcp@latest`)
- **能力：** 浏览器自动化、页面导航、点击/输入/截图、性能追踪、Lighthouse 审计、网络请求检查、控制台日志、堆快照等
- **用途：** 前端测试、网页抓取、性能分析、UI 验证

### 2.2 Oracle 数据库（只读）

- **协议：** stdio（基于 `mcp-alchemy` + `oracledb`，Python 包装器）
- **连接：** `sc_base@192.168.1.76:1521/assets` (Oracle 19.29)
- **能力：** 只读查询（SELECT/WITH/EXPLAIN/DESCRIBE/SHOW），参数绑定防注入
- **限制：** 严格只读，禁止所有写入/修改/结构调整操作
- **用途：** 数据查询、SQL 优化、表结构分析

---

## 3. 技能

### 3.1 全局技能（`~/.zcode/skills/`）

| 技能 | 来源 | 版本 | 触发场景 |
|------|------|------|---------|
| **skillhub-preference** | SkillHub 社区 | 1.0.0 | 技能发现/安装/更新时优先使用 SkillHub，不可用时回退到 ClawHub |
| **github-fetch** | SkillHub 社区 (@user_eaab4ecf) | 1.0.0 | 给定 GitHub URL 时，用 curl 获取仓库内容并分析 |
| **unclecheng-reduce-ai-perception-v2** | SkillHub 社区 (@user_ab5ae6ee) | 1.0.5 | 中文/英文 AI 文本人性化，移除 AI 写作痕迹 |

### 3.2 工作区技能（`~/.zcode/workspace/default/skills/`）

| 技能 | 来源 | 版本 | 触发场景 |
|------|------|------|---------|
| **ponytail** | ClawHub (@dietrichgebert) | 4.8.4 | 懒人资深开发者模式：YAGNI、标准库优先、无额外抽象。支持 lite/full/ultra 强度 |

### 3.3 用户自定义技能

以下技能安装在 `~/.agents/skills/` 或由项目配置发现：

| 技能 | 用途 |
|------|------|
| **ai-readme-generator** | 生成 AI 可读的项目文档（AGENTS.md、Cursor rules 等） |
| **baoyu-design** | 创建设计稿（UI 原型、仪表盘、幻灯片等） |
| **caveman** | 超压缩通信模式，减少约 75% token 消耗 |
| **create-agent-skills** | 创建、编写、构建和优化 Agent Skills |
| **document-skills** (docx) | DOCX 文档创建、编辑、分析 |
| **document-skills** (pdf) | PDF 报告、海报、论文、提取等 |
| **document-skills** (pptx) | PPTX 检查和更新 |
| **excel-automation** | Excel 自动化处理 |
| **find-skills** | 帮助发现和安装 Agent Skills |
| **github-repo-search** | 搜索和筛选 GitHub 开源项目 |
| **hue** | 生成新的设计语言技能 |
| **huhao-writing-perspective** | 以 huhao 的风格撰写文档/方案/汇报 |
| **khazix-writer** | 公众号长文写作 |
| **ponytail** | 懒人资深开发者模式（本地版） |
| **release-skills** | 通用发布工作流（Node.js、Python、Rust 等） |
| **rule-skill-regression** | 约束规则与技能的回归和收敛 |
| **skill-creator** | 创建和编辑 SKILL.md |
| **vgo-front-skill** | VGO/V7 前端项目的 bug 定位和需求实现 |
| **zcode-guide** | ZCode 配置诊断（命令、钩子、MCP、插件、技能） |

---

## 4. 自定义命令

| 命令 | 参数 | 说明 |
|------|------|------|
| `/ponytail` | `lite\|full\|ultra` | 懒人资深开发者模式，激活 ponytail 技能 |

---

## 5. 插件

| 插件 | 状态 |
|------|------|
| `carbone-skill@claude-plugins-official` | 已启用 |

---

## 6. 用户偏好与行为约束

### 6.1 交互模式

- **交互行为：** guide（引导模式）
- **语言：** 简体中文（`zh-CN`）
- **推理显示：** 开启
- **Todo 显示：** 开启
- **内存：** 已启用（自动持久化，按需召回）
- **仓库快照索引：** 已启用
- **即时搜索索引：** 已启用
- **任务自动归档：** 开启（超过 7 天）

### 6.2 行为底线（来自 `~/.zcode/AGENTS.md`）

- **数据库只读：** 仅允许 SELECT/WITH/EXPLAIN/DESCRIBE/SHOW，禁止一切写入/修改/删除（INSERT/UPDATE/DELETE/ALTER/CREATE/DROP 等），查询一律参数绑定
- **语言规则：** 全程简体中文；代码/命令/路径/API/报错保持原文
- **不猜测：** 不确定时明确说明，不把推断当作事实
- **计划/分析任务只读：** 不修改代码或文档
- **不修改无关文件：** 不擅自创建文档、commit、push、创建 PR

### 6.3 Less is More 原则

- **只留必要：** 删重复、删"可能有用"，判断标准是"现在是否需要"
- **单一工具：** 能用一样解决就不引入第二样
- **最小改动：** 只改相关文件，不碰无关代码；移除时连带清理依赖、配置、引用
- **配置回归：** 无效配置直接删，不保留死配置
- **收尾：** 改动后更新 lockfile，保证干净无残留
- **铁律：** 每次回答结束加上 **Less is More**

---

## 7. 微信机器人

| 配置项 | 值 |
|--------|-----|
| 提供商 | weixin |
| 状态 | 已启用（当前无活跃机器人状态） |
| 允许的工作区 | 所有（`*`） |
| 允许的命令 | status, new, workspace, model, mode, thoughtLevel, reply |
| 回复模式 | assistant_changes |

---

## 8. 桌面特性

| 特性 | 状态 |
|------|------|
| 桌面缩放级别 | -1（默认） |
| 硬件加速 | 已启用 |
| 自动下载更新 | 关闭 |
| 远程控制 | 已配置外部中继设备 |
| 后台保持唤醒 | 关闭 |

---

## 9. 近期项目工作区

| 项目 | 路径 |
|------|------|
| ai-starter-kits | `/Users/huhao/Documents/Dev/AI/ai-starter-kits` |
| VGO 前端包装 | `/Users/huhao/Documents/Dev/Frontend/SPEED-DEV-CENTER/assets/V7/vgo.front.assets.wrapper` |
| 智能大屏 | `/Users/huhao/Documents/Dev/Frontend/OTHERS/智能大屏项目/out.terminal.screen.admin` |
| SPEED-DEV-CENTER 后端 | `/Users/huhao/Documents/Dev/Backend/SPEED-DEV-CENTER/assets.wrapper` |
| zcode-mcp | `/Users/huhao/Documents/Dev/Frontend/AI/mcp/zcode-mcp` |
| 工作台个人管理 | `/Users/huhao/Documents/Dev/Frontend/SPEED-DEV-CENTER/admin/我的模版/workbench.personal.admin` |

---

## 10. 网络与安全

- **CA 证书：** 已配置 ZCode 网络 CA（`zcode-network-ca`），用于远程控制功能
- **凭证：** 加密存储（`credentials.json`），包含 Z.ai OAuth 令牌、JWT 令牌、远程控制密码哈希
- **提供商凭证：** DeepSeek 官方 API 密钥、云枢智联 API 密钥均已配置