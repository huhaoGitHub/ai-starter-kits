---
name: frontend
description: 前端开发规范与组件约束
---

# Frontend

## 规范

- 组件单一职责，一个文件一个组件
- 样式方案遵循项目现有约定（CSS Modules / Tailwind / styled-components 等）
- 状态管理优先本地 state，必要时再提升

## 文件组织

```
components/
├── common/       # 通用组件
├── feature/      # 业务组件
└── layout/       # 布局组件
```

## 性能

- 列表渲染带 key
- 大型列表使用虚拟滚动
- 图片懒加载