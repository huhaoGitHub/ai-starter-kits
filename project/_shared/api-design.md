---
name: api-design
description: RESTful API 设计规范
---

# API Design

## URI 规范

- 使用名词复数：`/users`、`/orders`
- 资源层级用斜杠：`/users/:id/orders`
- 查询参数用于过滤/排序/分页

## 方法语义

| 方法 | 语义 | 示例 |
|------|------|------|
| GET | 查询 | `/users?page=1` |
| POST | 创建 | `/users` |
| PUT | 全量更新 | `/users/:id` |
| PATCH | 部分更新 | `/users/:id` |
| DELETE | 删除 | `/users/:id` |

## 分页

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```