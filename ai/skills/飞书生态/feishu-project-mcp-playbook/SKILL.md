---
name: feishu-project-mcp-playbook
description: Use when working with Feishu Project MCP to create, update, query, or transition work items in any space that has recurring business fields; pair MCP with a locally maintained business context file so the agent can reuse field mappings, defaults, role mappings, and cached candidate values instead of rediscovering them every time.
---

# 飞书 Project MCP 工单管理方法论

## 适用场景

- 用户准备在 Claude Code、Codex CLI、Cursor、VSCode Copilot 等 AI 工具里接入飞书项目 MCP
- 在飞书项目里创建、更新、查询、评论、排期、流转工单
- 某个空间存在固定的业务字段、角色、默认值、自定义枚举、关联项等配置
- 希望先命中本地业务上下文缓存，再决定是否实时调用 MCP 查字段和候选值
- 希望把“字段映射 + 确认规则 + 缓存候选值”沉淀成可维护资产，而不是每次从零摸索

## 前置依赖

这个 skill 不是独立工作的，它必须搭配 `feishu-project` MCP Server 使用。

开始任何工单创建、更新、查询、流转动作之前，先检查两件事：

1. 飞书项目侧是否已经启用 MCP，并完成授权。
2. 当前 AI 工具是否已经正确连接飞书项目 MCP。

如果 `feishu-project` MCP 没安装、没配置、没连接成功，先暂停工单操作，改为引导用户完成连接。具体做法见 `references/mcp-connection-setup.md`。

## 核心思想

不要把 Feishu Project MCP 当成“每次都要把空间重新探索一遍”的工具。

更高效的做法是维护一份或多份本地业务上下文文件，记录：

- 空间标识与业务别名
- 常用工作项类型
- 字段 key 与业务含义
- 角色 key 与常用负责人
- 默认建议值
- 必问字段与确认规则
- 最近一次 live query 得到的枚举、关联项、用户缓存

这样 agent 在大多数场景下可以先命中本地上下文，再只对缺口做实时查询。

## 首次接入

1. 先确认飞书项目 MCP 已连接；如果没有，先读 `references/mcp-connection-setup.md`。
2. 再读 `references/business-context-template.md`。
3. 以模板为骨架，在 `references/` 下新增你自己的业务上下文文件，推荐命名：
   - `references/<space-simple-name>-context.md`
   - `references/<business-alias>-context.md`
4. 把该空间的项目标识、工作项类型、字段映射、角色映射、默认值、缓存候选值填进去。
5. 后续每次 live query 拿到新值后，只补对应区块，不要重写整份文件。

如果当前 skill 下已经存在空间专属上下文文件，优先读取空间精确命中的文件；没有时再把模板当结构参考，并用 MCP 实时补齐。

## 精简工作流

1. 先确认当前会话里 `feishu-project` MCP 可用；不可用时先做连接引导。
2. 解析用户意图：空间、业务别名、工作项类型、动作。
3. 找到对应的业务上下文文件；如果没有，就按模板结构边查边补。
4. 创建类动作先调用 `get_workitem_field_meta`，拿 schema 必填字段。
5. 把三类字段合并成待写清单：
   - schema 必填
   - 业务流程必填
   - 本轮准备写入的字段
6. 对动态字段先查本地上下文缓存；只有缓存缺失、用户要最新、或缓存不可信时才 live query。
7. 把“用户原话明确给出的值”和“本地默认值/缓存建议值”分开处理。
8. 所有待写字段里，只要不是用户明确给出或明确确认的，都先问清楚。
9. 全部确认后再调用 `create_workitem`、`update_field`、`update_node`、`transition_node`。
10. 本轮如果通过 live query 找到了新候选值，用 `apply_patch` 回写本地业务上下文文件。

## 核心工具速查

| 场景 | 工具 | 关键入参 |
|------|------|----------|
| 创建工单 | `create_workitem` | `project_key`, `work_item_type`, `fields` |
| 更新字段 | `update_field` | `work_item_id`, `fields` |
| 更新角色 | `update_field` | `work_item_id`, `role_operate` |
| 查工单详情 | `get_workitem_brief` | `work_item_id` |
| 查节点流详情 | `get_node_detail` | `project_key`, `work_item_id` |
| 查流转必填项 | `get_transition_required` | `project_key`, `work_item_id`, `state_key` |
| 更新节点排期/估分/负责人 | `update_node` | `project_key`, `work_item_id`, `node_id` |
| 完成或回滚节点 | `transition_node` | `project_key`, `work_item_id`, `node_id`, `action` |
| 查创建必填字段 | `get_workitem_field_meta` | `project_key`, `work_item_type` |
| 查字段配置 | `list_workitem_field_config` | `project_key`, `work_item_type`, `page_num` |
| 查角色配置 | `list_workitem_role_config` | `project_key`, `work_item_type`, `page_num` |
| 搜索用户 | `search_user_info` | `user_keys` |
| 查关联项候选值 | `search_by_mql` | `project_key`, `mql` |

## 业务上下文文件该存什么

业务上下文文件不是纯文档，而是 agent 的本地操作记忆。至少要覆盖这些区块：

- 适用范围：`project_key`、`simple_name`、默认工作项类型
- 业务别名：用户口语和空间/项目的映射
- 默认建议值：用户没显式给时可以拿来确认的预填值
- 确认规则：哪些字段必须问，哪些字段默认留空
- 字段注册表：字段 key、字段类型、怎么取值、何时必问
- 角色缓存：角色名到 `role_key`
- 枚举缓存：选项名到 `option_id`
- 关联项缓存：名称到工作项 ID
- 用户缓存：常见负责人到 `user_key`

细节结构直接看 `references/business-context-template.md`。

## 动态值解析顺序

1. 用户本轮明确给值
2. 本地业务上下文里的默认建议值
3. 本地业务上下文里的缓存候选值
4. MCP live query

使用原则：

- 用户明确给值，优先级最高
- 默认建议值只能用于确认，不能静默落库
- 缓存候选值优先于实时查询，但缓存命中失败时必须回退 live query
- 用户一旦说“查最新”“没有我要的”“把完整列表列出来”，就直接实时查询

## 确认规则

### 总规则

1. 任何准备写入的字段，只要用户没明确给值或明确确认，就视为未确认。
2. 本地业务上下文里的默认值和缓存都只是建议，不是自动写入许可。
3. 如果缺多个字段，优先一次性列出，减少来回确认。
4. 可选链接字段、附件字段、备注字段，如果用户没提，通常默认留空，不单独追问。
5. 角色字段要按角色分别确认，不要把“负责人=某某”自动拆成多个角色。

### 建议长期固化在业务上下文里的必问项

- 目标迭代或发布时间
- 主负责人
- 协作负责人
- 所属组件
- 优先级或严重程度
- 关联父项或关联项目

## 字段类型到取值方式

| 字段类型 | 先做什么 | 怎么拿值 |
|----------|----------|----------|
| `select` / `radio` / `multi-select` | 先看本地缓存 | 从枚举配置里取 `option_id` |
| `template` | 先看本地缓存 | 从模板枚举里取模板 ID |
| `user` / `multi-user` | 不看字段枚举 | `search_user_info` 拿 `user_key` |
| 角色字段 | 先看本地角色缓存 | `list_workitem_role_config` 拿 `role_key`，`search_user_info` 拿 `user_key` |
| 关联工作项字段 | 先看本地关联项缓存 | 不够时用 `list_workitem_field_config` + `search_by_mql` |
| 文本 / Markdown / 链接 / 数字 / 日期 | 一般无需候选值 | 直接按字段类型传值 |

## 节点流转工作流

适用于 `get_workitem_brief` 显示为节点流的工单。

1. 先用 `get_workitem_brief` 看当前状态和模式。
2. 再用 `get_node_detail` 找 `status = doing` 的当前节点，记下 `node_key`。
3. 调 `get_transition_required(mode=unfinished)` 检查流转前还缺哪些字段。
4. 如果返回里出现“下一节点必填”，优先补下一节点要求的排期、估分、负责人，不要只盯当前节点。
5. 用 `update_node` 写节点级字段，再用 `transition_node(action=confirm)` 推进阶段。
6. 流转后立即回查 `get_workitem_brief` 或 `get_node_detail`，确认状态真的变了。

### 时间表达落法

- 用户说“今天开始做两天”“下周一上线”这类相对时间时，先换成当前时区下的绝对日期。
- `update_node.node_schedule` 传当天零点对应的毫秒时间戳。
- 系统可能把结束时间归一到当天特定时刻，最终以回查结果为准。

### 超时处理

- `transition_node` 偶发超时，不等于失败。
- 先回查状态；只有状态没变，才重试一次。
- 不要把超时直接当成参数错误。

## 缓存维护规则

1. live query 只在必要时做，不要把所有字段都实时查一遍。
2. 一旦 live query 命中新值，就用 `apply_patch` 更新对应业务上下文区块。
3. 只改相关区块，不要重排整个文件。
4. 选项名称、ID、角色 key、用户 key 变化时，优先修正旧值，不要盲目追加重复项。
5. 如果一个空间已经形成稳定映射，后续优先维护这份本地上下文，而不是反复重新探索。

## 常见错误

- 把本地默认值当成已确认值直接创建
- 多选字段传字符串，没传 `option_id`
- 角色更新还走 `fields`，而不是 `role_operate`
- 关联工作项字段传字符串，实际需要数字 ID
- 节点流转前没先查 `get_transition_required`
- 收到超时就判定流转失败
- 每次都从字段配置重新查起，导致对话冗长且成本高

## References

- `references/mcp-connection-setup.md`: 飞书项目 MCP 的前置条件与连接方式摘要
- `references/business-context-template.md`: 业务上下文模板，首次接入或脱敏分享时使用
- 飞书 Project API 文档: https://project.feishu.cn/b/helpcenter/1p8d7djs/4id4bvnf
