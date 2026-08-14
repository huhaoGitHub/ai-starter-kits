# 项目级 AI 能力集 — 环境选择

本项目提供四种预设环境，覆盖不同开发场景。选择一种环境，将其文件复制到你的项目根目录即可生效。

## 环境一览

| 环境 | 适用场景 | 包含技能 | 复制命令 |
|------|---------|---------|---------|
| **basic** | 纯基础指令，无需领域技能加持 | 无 | `cp -rL basic/* /target/` |
| **fullstack** | 前后端通吃的全栈项目 | frontend + backend + api-design + testing | `cp -rL fullstack/* /target/` |
| **frontend** | 纯前端项目 | frontend + testing | `cp -rL frontend/* /target/` |
| **backend** | 纯后端项目 | backend + api-design + testing | `cp -rL backend/* /target/` |

## 快速开始

```bash
# 1. 选择环境（以 fullstack 为例）
cp -rL fullstack/* /path/to/your-project/

# 2. 编辑 AGENTS.md，填写项目技术栈信息
# 3. 开始使用 AI 能力
```

> `-L` 参数保证软链被展开为真实文件，目标项目得到独立副本，不依赖本项目。

## 复制后需自定义

1. 编辑 `AGENTS.md`，补充项目实际技术栈信息
2. 按需启用/禁用 `skills/` 中的技能文件
3. 根据项目需求调整指令细节