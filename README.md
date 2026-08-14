# ai-starter-kits

ZCode / Claude Code AI 能力预设集，开箱即用。

## 目录结构

```
ai-starter-kits/
├── global/          # 全局级：安装到 Agent 全局目录，所有项目共享
│   ├── AGENTS.md    # 全局 AI 指令
│   └── skills/      # 通用技能集
└── project/         # 项目级：四种环境，按需选择复制到项目根目录
    ├── basic/       # 普通环境 — 纯基础指令
    ├── fullstack/   # 全栈环境 — 前端 + 后端 + API + 测试
    ├── frontend/    # 前端环境 — 前端 + 测试
    └── backend/     # 后端环境 — 后端 + API + 测试
```

## 使用方式

### 全局安装（通用能力）

```bash
# ZCode
cp global/AGENTS.md ~/.zcode/AGENTS.md
cp -r global/skills/ ~/.zcode/skills/

# Claude Code
cp global/AGENTS.md ~/.claude/CLAUDE.md
cp -r global/skills/ ~/.claude/skills/
```

### 项目安装（按需选择环境）

```bash
# 选择一种环境复制到项目根目录
cp -rL project/fullstack/* /path/to/your-project/
# 或
cp -rL project/frontend/* /path/to/your-project/
# 或
cp -rL project/backend/* /path/to/your-project/
# 或
cp -rL project/basic/* /path/to/your-project/
```

> `-L` 保证软链被展开为真实文件，目标项目得到独立副本。

## 能力清单

### 全局级

| 技能 | 说明 |
|------|------|
| fullstack-dev | 通用全栈开发规范与代码生成约束 |
| database-expert | 只读数据库查询与 SQL 优化能力 |

### 项目级

| 技能 | 适用环境 | 说明 |
|------|---------|------|
| frontend | fullstack / frontend | 前端开发规范与组件约束 |
| backend | fullstack / backend | 后端开发规范与 API 约束 |
| api-design | fullstack / backend | RESTful API 设计规范 |
| testing | fullstack / frontend / backend | 测试策略与规范 |

## 原则

- **Less is More** — 只放核心能力，不堆砌
- **开箱即用** — 复制即生效，无需额外配置
- **按需选择** — 四种环境覆盖不同开发场景
- **按需定制** — AGENTS.md 预留了技术栈占位，复制后填写即可

## License

MIT