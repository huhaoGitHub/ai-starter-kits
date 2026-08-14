---
name: backend
description: 后端开发规范与 API 约束
---

# Backend

## 规范

- 控制器层只做参数校验和路由分发
- 业务逻辑封装在 Service 层
- 数据访问通过 Repository / DAO 层

## API 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

## 错误处理

- 统一异常处理中间件
- 业务异常带错误码和可读消息
- 不暴露内部实现细节（堆栈、SQL 等）