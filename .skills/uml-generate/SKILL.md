# UML Generate Skill

状态：v1.0 课程交付

用途：基于当前代码事实生成 PlantUML 源文件，用于架构说明、设计文档和答辩材料。

## 触发短语

说出以下任一即可触发本 Skill：
- "generate UML" / "生成类图" / "画架构图" / "生成时序图"
- "更新 PlantUML" / "补充用例图"
- "准备答辩用的图"

## 触发场景

- 补充或更新 `docs/08_概要设计说明书.md` 中的架构图
- 答辩前需要展示类图、ER 图或时序图
- 代码模型变更后需要同步更新 PlantUML 源文件
- 需求文档需要用例图支撑

## 工作步骤

### 步骤 1：读取代码事实源 —— 类图
读取 `app/models.py`，提取所有模型类及其关系：
- **模型类**：User, BlogColumn, Category, Tag, Article, Comment, Like, Favorite, AiLog
- **关联表**：ArticleTag (article_id, tag_id)
- **关系**：User 1→N Article; BlogColumn 1→N Article; Category 1→N Article; Article N↔N Tag; Article 1→N Comment; Article 1→N AiLog; User 1→N Like/Favorite
- **关键字段**：status 枚举（article: draft/published; comment: pending/approved/hidden），时间戳字段（created_at, updated_at, published_at）

### 步骤 2：读取架构事实源 —— 组件图/部署图
读取 `app/__init__.py`，提取：
- **蓝图（Blueprint）**：public, auth, admin, dashboard, article, column, category, tag, comment, ai, user（共 11 个）
- **扩展**：db (SQLAlchemy), login_manager (Flask-Login), csrf (Flask-WTF)
- **中间件**：error handlers (400/403/404/500), template helpers (markdown filter, csrf_token)
- 同时读取 `config.py` 了解环境配置，读取 `app/extensions.py` 了解扩展初始化

### 步骤 3：生成 PlantUML 源文件
基于步骤 1-2 的代码事实（不基于推测或计划），生成 .puml 文件并保存到 `diagrams/plantuml/`：

| 图类型 | 输出文件 | 数据来源 |
| --- | --- | --- |
| 类图 | `diagrams/plantuml/class-diagram.puml` | `app/models.py` |
| ER 模型图 | `diagrams/plantuml/er-model.puml` | `app/models.py` |
| 组件图 | `diagrams/plantuml/component-diagram.puml` | `app/__init__.py` |
| 用例图 | `diagrams/plantuml/use-case.puml` | `docs/07_需求规格说明书.md` |
| 时序图/活动图 | `diagrams/plantuml/main-flow.puml` | 目标流程（如登录、发文、评论审批） |

已有文件（architecture.puml, er-model.puml, main-flow.puml, use-case.puml）在更新时原位覆盖。

### 步骤 4：渲染（可选）
- 检查是否安装了 Java 和 plantuml.jar。本项目不提交 plantuml.jar。
- 如能渲染：执行 `java -jar plantuml.jar diagrams/plantuml/*.puml`（jar 路径用户提供）。
- 如不能渲染：在输出中标注"仅生成 .puml 源文件，未渲染为图片"。

## 输出格式

```
## UML 生成结果

| 图类型 | 输出文件 | 渲染状态 | 备注 |
| --- | --- | --- | --- |
| 类图 | diagrams/plantuml/class-diagram.puml | 仅源文件 | 基于 app/models.py 共 9 个模型类 |
| 组件图 | diagrams/plantuml/component-diagram.puml | 仅源文件 | 基于 app/__init__.py 共 11 个蓝图 |
```

## 禁止事项

1. 不提交 `plantuml.jar` 或大型二进制工具。
2. 不把未渲染的 .puml 写成"已生成图片"。
3. 不让图的内容超出当前代码实现事实——不画计划中的表或路由。
4. 不复制教师资料全文。
5. 不读取或修改 `software-practice-records`。
