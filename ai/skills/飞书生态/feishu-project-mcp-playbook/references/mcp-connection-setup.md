# 飞书项目 MCP 连接前置说明

来源：

- 官方文档：`在 AI 工具中连接 MCP`
- 链接：`https://project.feishu.cn/b/helpcenter/1ykiuvvj/wzb3ycsc`

## 什么时候先看这份文档

当用户要用这个 skill 管理飞书项目工单，但当前环境里还没有可用的 `feishu-project` MCP 时，先做连接，不要直接进入工单操作。

## 前提条件

先确认两件事：

1. 已在飞书项目中启用 MCP。
2. 已完成对应授权，或已经拿到连接所需的凭据。

如果使用 `HTTP Header` 或 `Stdio` 方式，通常还需要从飞书项目功能入口获取：

- `X-Mcp-Token`
- `MCP_USER_TOKEN`

## 通用连接思路

大多数 AI 工具都支持在配置文件里声明一个 MCP Server。

远程地址通常是：

```text
{domain}/mcp_server/v1
```

如果工具支持 OAuth，优先使用 OAuth。

通用 JSON 结构通常类似：

```json
{
  "mcpServers": {
    "feishu-project": {
      "httpUrl": "{domain}/mcp_server/v1"
    }
  }
}
```

如果工具只支持 Header 方式，通常类似：

```json
{
  "mcpServers": {
    "feishu-project": {
      "url": "{domain}/mcp_server/v1",
      "headers": {
        "X-Mcp-Token": "YOUR_TOKEN"
      }
    }
  }
}
```

实际字段名和配置层级以对应 AI 工具要求为准。

## Claude Code

根据官方文档，Claude Code 通常这样接入：

1. 打开 `Settings > MCP > Open Config File`。
2. 或手动编辑全局配置 `~/.claude.json`、`~/.claude/config.json`，以及项目级 `.claude.json`。
3. 在顶层 `mcpServers` 中加入飞书项目 MCP 配置。
4. 保存后在对话框输入 `/mcp`，按提示完成 OAuth 授权。

## Codex CLI / ChatGPT Desktop

根据官方文档，Codex 通常这样接入：

1. 打开全局配置 `~/.codex/config.toml`，或项目级 `.codex/config.toml`。
2. 写入飞书项目 MCP 配置。
3. 首次触发工具时，根据终端提示完成授权。
4. 重启 Codex CLI，让配置生效。

示例：

```toml
[mcpServers."feishu-project"]
httpUrl = "{domain}/mcp_server/v1"
```

## 其他 AI 工具

官方文档还给了这些工具的接法：

- Cursor
- VSCode（GitHub Copilot）
- Gemini CLI
- Manus
- Trae
- Dify
- 扣子

如果你的工具支持 MCP，但文档里没有单独列出，优先按该工具自己的 MCP 配置格式接入，并复用飞书项目给出的服务地址和授权方式。

## 推荐操作顺序

1. 先在飞书项目侧启用 MCP 并确认授权方式。
2. 在 AI 工具里配置 `feishu-project` MCP。
3. 验证当前会话里能看到或调用该 MCP。
4. 确认连接正常后，再开始创建、更新、查询和流转工单。

## 使用建议

- 如果团队里会长期使用飞书项目 MCP，优先统一一套可复用的连接方式。
- 如果同一个项目需要多人协作，建议把“连接方式”和“业务上下文模板”分开维护。
- 连接配置解决的是“AI 能否访问飞书项目”，业务上下文解决的是“AI 是否理解你的字段体系”；两者缺一不可。
