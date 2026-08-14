---
name: testing
description: 测试策略与规范
---

# Testing

## 层次

| 层次 | 目标 | 工具 |
|------|------|------|
| 单元测试 | Service / Utils | Vitest / Jest |
| 组件测试 | UI 组件 | Testing Library |
| E2E 测试 | 关键流程 | Playwright / Cypress |

## 规范

- 测试文件与被测文件同目录：`foo.ts` → `foo.test.ts`
- 描述清晰：`describe('Module')` + `it('should ...')`
- 不测实现细节，只测行为
- Mock 外部依赖（网络、数据库、文件系统）

## 覆盖率目标

- 单元测试：核心业务逻辑 ≥ 90%
- 组件测试：公共组件 ≥ 80%
- E2E：核心用户流程覆盖