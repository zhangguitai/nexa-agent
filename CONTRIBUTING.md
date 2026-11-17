# 开发与提交规范

本文档说明 NEXA Agent Workspace 的代码组织、质量检查和 Git 协作约定。

## 开发环境

- Node.js 20 或更高版本。
- 可选：Python 3.10 或更高版本，用于浏览器验收。
- 不需要安装生产依赖，项目只使用 Node.js 内置模块。

## 代码组织

| 位置 | 职责 |
| --- | --- |
| `server.mjs` | 静态服务、模型调用、工具注册、Agent 循环与降级策略 |
| `assets/app.js` | 页面状态、模板渲染、交互事件和本地演示数据 |
| `assets/icons.js` | 本地 SVG 图标定义 |
| `assets/styles.css` | 页面布局、组件视觉和响应式规则 |
| `tests/visual_check.py` | 浏览器视觉与交互验收 |
| `tools/check_code_style.mjs` | 无第三方依赖的代码规范检查 |

## 编码约定

- 使用 UTF-8、LF 换行、两空格缩进；Python 使用四空格缩进。
- JavaScript 使用 ES modules，优先使用 `const`，避免全局可变状态。
- 函数、变量和工具名称使用清晰的英文小驼峰或蛇形命名。
- 注释只解释设计原因、边界和复杂逻辑，不复述代码表面行为。
- 服务端新增能力必须纳入工具白名单，并同步补充输入校验与失败处理。
- 前端动态内容必须经过安全文本渲染，不得直接注入模型返回的 HTML。

## 质量检查

提交前运行：

```bash
npm run check
```

该命令检查文本格式、缩进、行尾空格、文件末尾换行，以及三个核心 JavaScript 文件的语法。

涉及界面交互时，再运行：

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tests/visual_check.py
```

## Git 约定

- 提交信息使用 `feat:`、`fix:`、`docs:`、`test:`、`chore:` 前缀。
- 一个提交只处理一个清晰主题，避免把格式化、功能与生成产物混在一起。
- 不提交 `.env`、API Key、Cookie、访问令牌和临时编辑文件。
- 提交前使用 `git diff --check` 和 `git status` 检查意外内容。
- 功能分支建议使用 `feat/<topic>`、`fix/<topic>` 或 `docs/<topic>`。

## 发布检查

发布到 GitHub 或 Gitee 前，确认仓库为 Public 或已向评审方提供只读访问权限，并检查 README、Git 历史、环境变量模板和依赖清单均已入库。
