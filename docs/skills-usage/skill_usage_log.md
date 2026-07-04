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
| 2026-07-03 | `work/v1.0-course-delivery` | Requirements Analyst Agent | 已用于系统理解和需求分流辅助 | `docs/change-requests/CR-003-需求澄清与新增功能评估.md`、`docs/system-understanding/06_需求-模块-代码追踪表.md`、本文 | 辅助反向阅读当前需求状态，区分已实现、部分实现、接口存在需验证、后续计划和 v1.0/v1.1/v2.0 分流。 | 项目负责人负责阅读、理解、人工确认和后续决策。 |
| 2026-07-03 | `work/v1.0-course-delivery` | System Design Agent | 已用于系统架构理解辅助 | `docs/system-understanding/01_当前系统总览.md`、`docs/system-understanding/02_目录结构与模块说明.md`、`docs/system-understanding/03_技术架构通俗解释.md`、本文 | 辅助整理 Flask、Blueprint、Service、Model、Template、配置和目录边界，不改变 ADR-002 技术路线。 | 项目负责人负责确认架构理解和后续 CR 是否进入设计或代码。 |
| 2026-07-03 | `work/v1.0-course-delivery` | DBA Agent | 已用于数据模型理解辅助 | `docs/system-understanding/05_数据模型与数据库关系.md`、`docs/system-understanding/07_当前系统风险与不确定项.md`、本文 | 辅助整理用户、文章、专栏、分类、标签、评论、点赞、收藏、AI 日志等数据关系和 ReadingHistory 候选风险。 | 项目负责人确认本轮不新增表、不新增字段、不修改数据库。 |
| 2026-07-03 | `work/v1.0-course-delivery` | Frontend Developer Agent | 已用于页面和视觉风险理解辅助 | `docs/system-understanding/04_路由-页面-模板映射.md`、`docs/system-understanding/07_当前系统风险与不确定项.md`、本文 | 辅助整理路由、页面、模板、角色、演示路径和视觉一致性待验收事项。 | 项目负责人确认本轮不修改模板、CSS、JS 或页面实现。 |
| 2026-07-03 | `work/v1.0-course-delivery` | Test Engineer Agent | 已用于测试与验收风险理解辅助 | `docs/system-understanding/07_当前系统风险与不确定项.md`、`docs/change-requests/CR-003-需求澄清与新增功能评估.md`、本文 | 辅助整理启动、初始化、E2E、AI、错误路径、权限路径和视觉验收缺口。 | 项目负责人确认测试脚本存在不等于测试通过，真实执行进入后续 CR。 |
| 2026-07-03 | `work/v1.0-course-delivery` | `requirements-clarity` | 已参考 | `docs/change-requests/CR-003-需求澄清与新增功能评估.md`、本文 | 辅助需求澄清、范围收敛、v1.0 必做/可选和未来版本边界判断。 | 结论需项目负责人确认，不自动授权代码修改。 |
| 2026-07-03 | `work/v1.0-course-delivery` | `project-requirements` | 已参考 | `docs/system-understanding/06_需求-模块-代码追踪表.md`、本文 | 辅助把 F001-F050 与模块、路由、模板、脚本和文档建立追踪关系。 | 追踪状态以当前仓库事实和人工阅读为准。 |
| 2026-07-03 | `work/v1.0-course-delivery` | `system-designer` | 已参考 | `docs/system-understanding/01_当前系统总览.md` 至 `docs/system-understanding/07_当前系统风险与不确定项.md`、本文 | 辅助整理架构、模块、数据模型、路由页面映射和风险说明。 | 不夸大为自动完成系统设计，不替代人工确认。 |
| 2026-07-04 | `work/v1.0-course-delivery` | Requirement / Architect / Frontend / Tester / Reviewer Agent | 已建立项目化主入口 | `agent-prompts/requirement_agent.md`、`agent-prompts/architect_agent.md`、`agent-prompts/frontend_agent.md`、`agent-prompts/tester_agent.md`、`agent-prompts/reviewer_agent.md` | 将待填写骨架补充为本项目可直接使用的 Agent prompt，明确输入、输出、禁止事项和标准提示词。 | 仅表示流程入口已建立；后续每次实际使用仍需按任务记录。 |
| 2026-07-04 | `work/v1.0-course-delivery` | `requirements-clarity` / `md-to-srs-docx` / `md-to-sd-docx` / `uml-generator` / `code-review` | 已建立项目化 Skill 规程 | `.skills/requirement-clarify/SKILL.md`、`.skills/docx-requirement/SKILL.md`、`.skills/docx-design/SKILL.md`、`.skills/uml-generate/SKILL.md`、`.skills/code-review/SKILL.md` | 将待填写骨架补充为可执行的使用规程，明确触发场景、输入材料、步骤、输出和禁止事项。 | 本轮未生成 docx、未渲染 UML、未运行外部教师工具链。 |
| 2026-07-04 | `work/v1.0-course-delivery` | Vibe Coding 工作流 | 已用于交付检查收束 | `docs/14_最终交付检查清单.md`、本文 | 建立课程交付前检查清单，串联需求、设计、测试、Review、AI 协作、Agent/Skill 使用记录和项目总结。 | 交付前仍需根据真实测试、AI 调用、视觉验收和人工确认更新状态。 |

## 本轮仍未执行事项

本轮 Agent / Skill 只用于反向阅读、整理和记录当前系统理解，没有执行以下操作：

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
