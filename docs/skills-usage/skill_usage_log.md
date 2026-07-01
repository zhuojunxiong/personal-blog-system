# Skill 使用记录

本文记录教师 Skill 和 Vibe Coding 工作流在本项目中的使用状态。记录原则是：未实际运行的 Skill 不写成已运行，未生成的文件不写成已生成，未验证的结论不写成已通过。

## 当前记录

| 日期 | 分支 | Skill / 工作流 | 使用状态 | 已关联文档 | 输出或用途 | 人工确认 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-02 | `work/v1.0-course-delivery` | Vibe Coding 工作流 | 已用于流程组织和边界说明 | `AGENTS.md`、`docs/13_教师Agent与Skill融入说明.md`、`docs/change-requests/CR-002-教师Agent与Skill融入交付流程.md`、`docs/skills-usage/README.md`、`docs/skills-usage/skill_mapping.md`、本文 | 按“读约束 -> 建映射 -> 写索引 -> 检查 diff”的方式组织本轮文档交付。 | 仍需项目负责人确认最终交付口径。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `project-requirements` | 计划使用；已纳入映射说明 | `docs/skills-usage/skill_mapping.md` | 后续可用于需求整理、需求边界和追溯矩阵补强。 | 使用前需确认输入文档范围。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `requirements-clarity` | 计划使用；已纳入映射说明 | `docs/skills-usage/skill_mapping.md`、本文 | 后续可用于 CR 前置澄清、范围收敛和验收标准确认。 | 使用前需确认澄清问题和不纳入范围。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `system-designer` | 计划使用；已纳入映射说明 | `docs/skills-usage/skill_mapping.md` | 后续可用于概要设计、接口契约、架构风险和 ADR 判断。 | 使用前需确认不改变 ADR-002 技术路线。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `prototype-prompt-generator` | 计划使用 | `docs/skills-usage/skill_mapping.md` | 后续可用于页面原型或前端实现提示词。 | 使用前需确认目标页面和输出格式。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `ui-ux-pro-max` | 计划使用 | `docs/skills-usage/skill_mapping.md` | 后续可用于视觉一致性、可用性和可访问性评审。 | 使用前需确认验收页面和浏览器环境。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `md-to-srs-docx` | 计划使用 | `docs/skills-usage/skill_mapping.md` | 后续可将需求规格说明书导出为 docx。 | 导出后需人工确认格式和内容。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `md-to-sd-docx` | 计划使用 | `docs/skills-usage/skill_mapping.md` | 后续可将概要设计说明书导出为 docx。 | 导出后需人工确认格式和内容。 |
| 2026-07-02 | `work/v1.0-course-delivery` | `uml-generator` | 计划使用 | `docs/skills-usage/skill_mapping.md` | 后续可生成或维护 PlantUML 源文件。 | 生成后需人工确认图与设计一致。 |

## 本轮未执行事项

本轮没有执行以下操作：

- 未运行教师 Skill 工具链。
- 未生成 docx。
- 未生成或渲染 UML 图片。
- 未执行浏览器视觉验收。
- 未执行自动化测试。
- 未修改业务代码。
- 未读取或修改 `software-practice-records`。
- 未提交整个 zip、jar、字体、HTML、缓存文件或大型二进制资源。

## 后续记录模板

后续每次实际使用 Skill 时，建议追加以下字段：

| 日期 | 分支 | 触发来源 | Skill | 输入范围 | 输出文件 | 是否实际运行 | 是否测试或验证 | 人工确认事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 待填写 | 待填写 | CR / ADR / 文档任务 | 待填写 | 待填写 | 待填写 | 是 / 否 | 是 / 否 / 不适用 | 待填写 |

## 状态口径

| 状态 | 含义 |
| --- | --- |
| 已用于流程组织和边界说明 | 已经用于组织本项目文档工作或说明交付流程，但不等同于运行外部 Skill。 |
| 已纳入映射说明 | 已在索引或映射表中建立关系，后续可追溯。 |
| 计划使用 | 后续可用，但当前没有运行证据或输出文件。 |
| 已实际运行 | 后续只有在真实执行 Skill 并记录输入、输出和结果后才能使用。 |
| 需人工确认 | AI 或 Skill 生成内容需要项目负责人复核，不能自动视为最终结论。 |
