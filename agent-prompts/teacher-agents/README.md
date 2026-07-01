# Teacher Agents Prompt Mapping

生成日期：2026-07-01

适用分支：`work/v1.0-course-delivery`

本目录用于保存教师 Agent 在 `personal-blog-system` 项目中的项目化提示词映射。这里的内容不是教师资料原文搬运，也不表示已经实际运行了外部 Agent 或 Skill；它只定义后续在本项目中如何按角色边界使用这些 Agent 方法。

## 1. 目录定位

`agent-prompts/teacher-agents/` 面向 v1.0 课程交付与工程治理，用于说明不同 Agent 如何服务于需求、设计、数据库、前端、测试、Review 与交付材料维护。

本目录遵守以下边界：

1. 只保存项目化 prompt 映射文档。
2. 不修改业务代码。
3. 不复制教师资料全文。
4. 不读取或修改 `software-practice-records`。
5. 不提交 zip、jar、字体、HTML、缓存或无关二进制资源。
6. 不把未执行的 Agent、Skill、测试、Review 或导出工作写成已完成。

## 2. 文件清单

| 文件 | 对应角色 | 主要用途 |
| --- | --- | --- |
| `requirements_analyst_agent.md` | Requirements Analyst Agent | 需求澄清、范围拆解、需求追溯、CR 输入整理。 |
| `system_design_agent.md` | System Design Agent | 架构追溯、方案比较、ADR 判断、概要设计辅助。 |
| `dba_agent.md` | DBA Agent | 数据模型、SQLite 约束、初始化与迁移风险评估。 |
| `frontend_developer_agent.md` | Frontend Developer Agent | 页面体验、模板样式一致性、前端验收提示词。 |
| `test_engineer_agent.md` | Test Engineer Agent | 测试计划、测试用例、验收清单、缺陷记录。 |

## 3. 与现有 docs 的关系

本目录内容应与 `docs/13_教师Agent与Skill融入说明.md` 保持一致。`docs/` 中的正式文档仍然是项目交付材料的主要承载位置，本目录只提供可复用的 Agent 使用提示词和角色边界。

当某个 Agent 产出需求、设计、测试或 Review 内容时，应把最终结果沉淀到对应 `docs/` 文件、CR、ADR、测试报告或 Review 记录中，而不是只停留在 prompt 文件里。

## 4. 使用原则

1. 先确认输入材料，再生成输出材料。
2. 只引用当前仓库代码和正式文档能支撑的事实。
3. 对缺失信息使用“待补齐”或“需人工确认”。
4. 只有真实执行过的测试、Review、导出或验证，才能写成“已执行”。
5. 涉及架构、数据库、技术路线或业务范围变化时，必须先进入 CR / ADR 判断。

## 5. 本轮完成情况

本轮仅创建本目录下的 Agent prompt 映射文档。未修改业务代码，未运行测试，未生成 docx，未渲染 UML，未进行浏览器视觉验收，未读取或修改 `software-practice-records`。
