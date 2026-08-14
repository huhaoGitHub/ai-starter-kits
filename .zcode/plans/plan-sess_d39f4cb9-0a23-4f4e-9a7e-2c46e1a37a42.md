## 结构方案

```
project/
├── README.md                 # 四种环境总览，引导选择
├── _shared/                  # 共享 skill 源文件（软链目标）
│   ├── frontend.md
│   ├── backend.md
│   ├── api-design.md
│   └── testing.md
├── basic/                    # 普通环境 — 纯基础指令，无领域技能
│   ├── AGENTS.md
│   └── CLAUDE.md
├── fullstack/                # 全栈环境 — 前后端通吃（当前 project/ 内容移入）
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   └── skills/               # 软链 → _shared/ 全部 4 个
├── frontend/                 # 前端环境 — 专注前端
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   └── skills/               # 软链 → _shared/ frontend.md + testing.md
└── backend/                  # 后端环境 — 专注后端
    ├── AGENTS.md
    ├── CLAUDE.md
    └── skills/               # 软链 → _shared/ backend.md + api-design.md + testing.md
```

## 各环境差异

| 环境 | AGENTS.md 重点 | 技能 |
|------|---------------|------|
| basic | 通用约束 + 安全底线，无技术栈内容 | 无 |
| fullstack | 全栈技术栈占位 + 全部约束 | frontend + backend + api + testing |
| frontend | 前端技术栈（框架/构建/样式方案） | frontend + testing |
| backend | 后端技术栈（语言/框架/数据库） | backend + api-design + testing |

## 实施步骤

1. 新建 `project/_shared/`，将现有 skill 文件移入
2. 新建 `project/fullstack/`，移入现有 AGENTS.md / CLAUDE.md，创建 skills/ 软链
3. 新建 `project/basic/`、`project/frontend/`、`project/backend/`，各含 AGENTS.md + CLAUDE.md + skills/ 软链
4. 更新 `project/README.md` 为四种环境总览
5. 更新根 `README.md`

## 复制到项目根目录的用法

```bash
# 选择一种环境复制
cp -rL project/fullstack/* /target-project/   # -L 跟随软链，得到真实文件
```

**-L 保证软链被展开为真实文件，目标项目拿到的是独立副本，不依赖本项目。**