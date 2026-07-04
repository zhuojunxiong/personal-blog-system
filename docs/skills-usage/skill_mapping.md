# Skill 与项目交付物映射

本文建立教师 Skill、Vibe Coding 工作流与本项目交付物的映射。映射只表示后续可追溯的使用入口和交付位置，不表示所有 Skill 都已经实际运行。

## 映射总表

| Skill / 工作流 | 本项目交付物映射 | 当前状态 | 使用边界 |
| --- | --- | --- | --- |
| `project-requirements` | `docs/07_需求规格说明书.md`、`docs/02_v0.5.1需求追溯.md`、`docs/product-rebaseline/`、CR 文档 | 计划使用；已纳入映射说明 | 可用于需求整理、需求边界和追溯矩阵，不替代人工确认。 |
| `requirements-clarity` | `docs/change-requests/`、`docs/07_需求规格说明书.md`、`docs/skills-usage/skill_usage_log.md` | 计划使用；已纳入映射说明 | 可用于复杂需求进入实现前的澄清、范围收敛和验收标准确认。 |
| `system-designer` | `docs/08_概要设计说明书.md`、`docs/03_v0.5.1架构追溯.md`、`docs/06_ADR/` | 计划使用；已纳入映射说明 | 可用于设计说明、接口契约和架构风险整理；不得更换 ADR-002 已确认技术路线。 |
| `prototype-prompt-generator` | 后续原型提示词、前端实现说明、视觉验收准备材料 | 计划使用 | 本轮未生成新原型，不提交 HTML 原型导出物。 |
| `ui-ux-pro-max` | 后续 UI/UX 验收记录、页面一致性检查、可访问性检查 | 计划使用 | 本轮未做浏览器视觉验收，不修改模板、CSS、JS 或图片资源。 |
| `md-to-srs-docx` | `docs/07_需求规格说明书.md` 到课程要求 docx 的导出流程 | 已建立项目化入口；未实际导出 | `.skills/docx-requirement/SKILL.md` 已补充使用规程；导出结果需要后续记录输入、输出和人工确认。 |
| `md-to-sd-docx` | `docs/08_概要设计说明书.md` 到课程要求 docx 的导出流程 | 已建立项目化入口；未实际导出 | `.skills/docx-design/SKILL.md` 已补充使用规程；导出结果需要后续记录输入、输出和人工确认。 |
| `uml-generator` | `diagrams/plantuml/`、`docs/08_概要设计说明书.md`、UML 说明材料 | 已建立项目化入口；未实际渲染 | `.skills/uml-generate/SKILL.md` 已补充使用规程；本轮未提交 jar，未生成新图片。 |
| Vibe Coding 工作流 | `AGENTS.md`、CR、ADR、测试报告、Review 记录、AI 协作记录、项目总结、Git 小步提交记录 | 已用于流程组织和边界说明 | 用于约束需求澄清、设计判断、小步实现、验证和复盘，不替代测试结果。 |

## 与现有本地 Skill 骨架的关系

| 教师 Skill | 当前仓库可对应位置 | 说明 |
| --- | --- | --- |
| `requirements-clarity` | `.skills/requirement-clarify/SKILL.md` | 已补充项目化使用规程，可作为需求澄清类 Skill 的入口。 |
| `md-to-srs-docx` | `.skills/docx-requirement/SKILL.md` | 已补充项目化使用规程，可作为需求规格说明书 docx 导出入口。 |
| `md-to-sd-docx` | `.skills/docx-design/SKILL.md` | 已补充项目化使用规程，可作为概要设计说明书 docx 导出入口。 |
| `system-designer` | `.skills/docx-design/SKILL.md`、`agent-prompts/architect_agent.md` | 当前仅建立映射，后续需人工确认具体使用方式。 |
| `uml-generator` | `.skills/uml-generate/SKILL.md` | 已补充项目化使用规程，可作为 PlantUML 源文件生成或维护入口。 |
| `project-requirements` | 后续可补充项目化说明 | 当前仅纳入映射，不新增 Skill 文件。 |
| `prototype-prompt-generator` | 后续可补充项目化说明 | 当前仅纳入映射，不新增 Skill 文件。 |
| `ui-ux-pro-max` | 后续可补充项目化说明 | 当前仅纳入映射，不新增 Skill 文件。 |

## 禁止纳入的资源

以下资源不进入当前仓库，除非后续另有明确 CR、必要性说明和人工确认：

- 整个教师资料 zip。
- 教师资料原文全文。
- jar、字体、HTML 导出物、缓存目录。
- 大型二进制资源、无关示例工程或不可追溯的压缩包。
- `software-practice-records` 中的内容。

## 人工确认要求

使用 Skill 生成或整理出的内容必须经过人工确认，尤其是以下内容：

- 需求范围、优先级和验收标准。
- 架构方案、ADR 判断和技术路线。
- docx 导出结果和课程交付口径。
- UML 图是否准确反映当前设计。
- UI/UX 评审结论和是否进入实现。
- 测试结果、Review 结论和项目总结表述。
