# React TypeScript Project with TailwindCSS

这是一个使用Vite创建的React TypeScript项目，集成了TailwindCSS、Prettier和其他最佳实践工具。

## 功能特性

- ⚡️ **Vite** - 极速的前端构建工具
- ⚛️ **React 19** - 最新版React
- 🔒 **TypeScript** - 类型安全
- 🎨 **TailwindCSS** - 实用优先的CSS框架
- 🧹 **ESLint** - 代码质量检查
- 💅 **Prettier** - 代码格式化
- 🌙 **暗黑模式** - 支持亮色/暗色主题切换
- 🧩 **组件化架构** - 模块化和可重用组件
- 🪝 **自定义Hooks** - 包含localStorage等实用钩子
- 🔄 **API服务层** - 集中管理API请求
- 🔐 **环境变量** - 安全管理配置和密钥

## 开始使用

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 代码格式化

```bash
npm run format
```

## 项目结构

```
/
├── public/              # 静态资源
├── src/
│   ├── assets/          # 图片、字体等资源
│   ├── components/      # 可重用组件
│   ├── hooks/           # 自定义React钩子
│   ├── services/        # API服务和数据处理
│   ├── types/           # TypeScript类型定义
│   ├── App.tsx          # 应用主组件
│   ├── index.css        # 全局样式
│   └── main.tsx         # 应用入口
├── .env.example         # 环境变量示例
├── .env.local           # 本地环境变量（不提交到版本控制）
├── .eslintrc.js         # ESLint配置
├── .prettierrc          # Prettier配置
├── postcss.config.js    # PostCSS配置
├── tailwind.config.js   # TailwindCSS配置
└── tsconfig.json        # TypeScript配置
```

## 最佳实践

### 组件开发

- 使用函数组件和React Hooks
- 为组件定义明确的Props接口
- 将大型组件拆分为更小的可重用组件
- 使用TailwindCSS实用类进行样式设计

### 状态管理

- 对于简单状态，使用useState和useReducer
- 对于持久化状态，使用自定义的useLocalStorage钩子
- 对于复杂状态，考虑使用Context API或状态管理库

### API调用

- 使用services/api.ts中的函数进行API调用
- 处理加载状态和错误
- 使用TypeScript接口定义API响应类型

### 环境变量

- 所有环境变量必须以VITE\_前缀开头
- 在.env.example中提供示例，但不包含敏感信息
- 敏感信息存储在.env.local中（已在.gitignore中排除）

## 贡献

欢迎提交问题和拉取请求！
