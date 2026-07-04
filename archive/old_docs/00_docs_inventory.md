# docs 目录文档盘点

首次盘点日期：2026-06-30

最近更新日期：2026-07-04

盘点范围：仅 `personal-blog-system/docs/` 目录。

本次未读取、未修改 `software-practice-records`；未修改 `app/`、`templates/`、`static/`、`models/`、`routes/`、`run.py`、`config.py`、`requirements.txt`；未删除、移动任何文档。

说明：本文只盘点 `docs/` 中已有文档的主题、版本归属和维护建议，不把旧版本计划写成当前实现。凡需要与当前代码、运行结果、提交记录或人工意图核对的内容，均标注为“需人工确认”。

2026-07-04 更新说明：当前 `docs/` 已不再只是正式文档骨架，还包含 ADR、CR、系统理解、产品重新基线化、Skill 使用说明等治理材料。若本文早期条目与当前目录实际情况不一致，以本节之后的“当前补充盘点”为准。

## 0. 当前补充盘点

| 路径 | 类型 | 当前用途 | 维护建议 |
|---|---|---|---|
| `docs/00_仓库结构导航.md` | 仓库导航 | 说明当前仓库各目录职责、可信度和整理边界。 | 作为新协作者入口，后续目录调整时同步更新。 |
| `docs/06_ADR/` | 架构决策记录 | 已包含统一主仓库、技术路线、半自动工程化、产品重新基线化、AI 闭环等 ADR。 | 后续架构变更先补 ADR，不再视为仅有占位目录。 |
| `docs/change-requests/` | 需求变更记录 | 已包含多份 CR 和模板，用于记录受控需求变更。 | 新需求、新整理动作和大改动优先从 CR 进入。 |
| `docs/system-understanding/` | 系统理解材料 | 包含系统总览、目录说明、路由映射、模型关系、追踪表和风险说明。 | 作为读代码前的辅助材料；正式结论仍需代码核验。 |
| `docs/product-rebaseline/` | 产品重新基线化材料 | 包含定位、用户角色、业务闭环、功能取舍、课程验收和下一版本建议。 | 属于产品分析和候选范围，不等同于已实现功能。 |
| `docs/skills-usage/` | Skill 使用治理材料 | 包含 Skill 使用说明、映射和日志。 | 用于 AI 协作追溯，不替代测试或 Review 事实。 |
| `docs/13_教师Agent与Skill融入说明.md` | 补充交付说明 | 说明教师 Agent 与 Skill 如何纳入项目交付链路。 | 作为 00-12 正式文档之外的补充材料维护。 |
| `docs/14_最终交付检查清单.md` | 补充检查清单 | 面向最终交付的检查项。 | 属于补充交付材料；当前是否完成需按清单逐项确认。 |
| `docs/test.md` | 临时启动备忘 | 当前仅包含激活虚拟环境和运行项目的命令，不像正式测试报告。 | 建议后续确认保留、改名或归档。 |

当前 `docs/` 可按四类理解：

1. 正式交付主链路：`docs/00_项目背景与开发方法说明.md` 到 `docs/12_项目总结.md`。
2. 受控变更材料：`docs/change-requests/` 和 `docs/06_ADR/`。
3. 分析辅助材料：`docs/system-understanding/`、`docs/product-rebaseline/`、`docs/skills-usage/`、`docs/13_教师Agent与Skill融入说明.md`、`docs/14_最终交付检查清单.md`。
4. 历史版本材料：`docs/day*.md`、`docs/v0.4.1-*.md`、`docs/v0.5-release-notes.md`、`docs/v5.1-release-notes.md`。

## 1. 当前 docs/ 中的文档

| 路径 | 类型 | 对应版本或主题 | 当前状态判断 |
|---|---|---|---|
| `docs/00_项目背景与开发方法说明.md` | 正式文档骨架 | 项目背景、开发方法 | 待填写，适合继续维护 |
| `docs/01_v0.5.1现状盘点.md` | 正式文档骨架 | v0.5.1 当前现状盘点 | 待填写，适合继续维护 |
| `docs/02_v0.5.1需求追溯.md` | 正式文档骨架 | v0.5.1 需求来源、变化、实现追溯 | 待填写，适合继续维护 |
| `docs/03_v0.5.1架构追溯.md` | 正式文档骨架 | v0.5.1 架构现状、依据、演进 | 待填写，适合继续维护 |
| `docs/04_未来需求与产品方向.md` | 正式文档骨架 | 未来需求、产品方向、待确认事项 | 待填写，适合继续维护 |
| `docs/05_技术路线决策报告.md` | 正式文档骨架 | 技术路线与决策说明 | 待填写，适合继续维护 |
| `docs/06_ADR/.gitkeep` | 目录占位文件 | ADR 目录占位 | 目录已建立，ADR 正文尚未建立 |
| `docs/07_需求规格说明书.md` | 正式文档骨架 | 需求规格说明书 | 待填写，适合继续维护 |
| `docs/08_概要设计说明书.md` | 正式文档骨架 | 概要设计说明书 | 待填写，适合继续维护 |
| `docs/09_测试报告.md` | 正式文档骨架 | 测试报告 | 待填写，适合继续维护 |
| `docs/10_代码Review记录.md` | 正式文档骨架 | 代码 Review 记录 | 待填写，适合继续维护 |
| `docs/11_AI协作记录.md` | 正式文档骨架 | AI 协作记录 | 待填写，适合继续维护 |
| `docs/12_项目总结.md` | 正式文档骨架 | 项目总结 | 待填写，适合继续维护 |
| `docs/day1-development-record.md` | 历史开发记录 | V0.1 第一阶段，项目骨架搭建 | 适合作为历史版本记录 |
| `docs/day2-development-record.md` | 历史开发记录 | V0.2 业务闭环实现 | 适合作为历史版本记录 |
| `docs/day3-development-record.md` | 历史开发记录 | V0.3 多用户知识专栏平台 | 适合作为历史版本记录 |
| `docs/day4-development-record.md` | 历史开发记录 | V0.4 前端与交互重构 | 适合作为历史版本记录 |
| `docs/v0.4.1-design-note.md` | 历史设计说明 | v0.4.1 页面、交互、路由、AI 占位策略 | 适合作为历史版本记录，也可为架构追溯提供素材 |
| `docs/v0.4.1-implementation-rules.md` | 历史实施规则 | v0.4.1 技术边界、模板/CSS/JS 规则、未来演进 | 适合作为历史版本记录 |
| `docs/v0.5-release-notes.md` | 版本迭代文档 | V0.5，真实 AI 接入、安全加固、写作体验升级 | 适合作为历史版本记录；其实现状态需人工确认 |
| `docs/v5.1-release-notes.md` | 版本迭代文档 | V5.1，AI 智能搜索、演示数据、启动体验优化 | 适合作为历史版本记录；版本命名与 v0.5.1 关系需人工确认 |
| `docs/startup-and-test-guide.md` | 使用与验收指南 | V5.1 启动、DeepSeek API 接入、验收流程、常见问题 | 适合维护为当前使用指南，但内容有效性需人工确认 |

## 2. 适合作为正式文档继续维护

以下文档与 `AGENTS.md` 中规划的正式文档结构一致，建议作为后续主文档继续维护：

- `docs/00_项目背景与开发方法说明.md`
- `docs/01_v0.5.1现状盘点.md`
- `docs/02_v0.5.1需求追溯.md`
- `docs/03_v0.5.1架构追溯.md`
- `docs/04_未来需求与产品方向.md`
- `docs/05_技术路线决策报告.md`
- `docs/06_ADR/`
- `docs/07_需求规格说明书.md`
- `docs/08_概要设计说明书.md`
- `docs/09_测试报告.md`
- `docs/10_代码Review记录.md`
- `docs/11_AI协作记录.md`
- `docs/12_项目总结.md`

补充建议：

- `docs/startup-and-test-guide.md` 可作为当前使用指南继续维护，但应先核对其中的版本号、命令、测试账号、AI 接入说明和当前代码是否一致。
- `docs/00_docs_inventory.md` 可作为阶段性文档治理清单维护。

## 3. 适合作为历史版本记录

以下文档记录了早期阶段或特定版本的目标、变更、设计和验收信息，建议保留为历史记录，不直接当作当前实现事实：

- `docs/day1-development-record.md`：V0.1 第一阶段项目骨架。
- `docs/day2-development-record.md`：V0.2 基础业务闭环。
- `docs/day3-development-record.md`：V0.3 多用户知识专栏平台。
- `docs/day4-development-record.md`：V0.4 前端与交互重构。
- `docs/v0.4.1-design-note.md`：v0.4.1 设计说明。
- `docs/v0.4.1-implementation-rules.md`：v0.4.1 实施边界。
- `docs/v0.5-release-notes.md`：V0.5 版本总结。
- `docs/v5.1-release-notes.md`：V5.1 版本总结，版本命名需人工确认。

这些文档可以作为 `01_v0.5.1现状盘点.md`、`02_v0.5.1需求追溯.md`、`03_v0.5.1架构追溯.md` 的历史素材，但写入正式文档时应区分：

- 历史上计划或目标；
- 历史文档声称完成；
- 当前代码可验证已经实现；
- 当前仍需人工确认。

## 4. 可能重复的内容

| 重复主题 | 涉及文档 | 说明 |
|---|---|---|
| 启动流程、环境准备、访问地址 | `startup-and-test-guide.md`、`day1-development-record.md`、`day2-development-record.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md` | 早期开发记录和版本总结中均出现启动说明，正式维护时建议以 `startup-and-test-guide.md` 为主。 |
| 测试账号和验收流程 | `startup-and-test-guide.md`、`day2-development-record.md`、`day3-development-record.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md` | 账号数量、验收项和覆盖范围可能随版本变化，需人工确认当前有效版本。 |
| AI 功能说明 | `startup-and-test-guide.md`、`v0.4.1-design-note.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md`、`day2-development-record.md` | AI 从占位到真实接入再到智能搜索，各版本语义不同，整理时必须标明版本阶段。 |
| 技术栈和架构边界 | `v0.4.1-implementation-rules.md`、`v0.4.1-design-note.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md`、正式文档骨架 | 多处都说明 Flask + Jinja2 + SQLite 等边界，可汇总进 `05_技术路线决策报告.md`，但需人工确认当前事实。 |
| 页面、路由、模板和静态资源清单 | `day1-development-record.md`、`day2-development-record.md`、`day3-development-record.md`、`day4-development-record.md`、`v0.4.1-design-note.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md` | 历史清单可能与当前仓库不完全一致，不能直接写入当前概要设计。 |
| 后续计划和遗留事项 | `day1-development-record.md`、`day2-development-record.md`、`day3-development-record.md`、`day4-development-record.md`、`v0.4.1-design-note.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md`、`04_未来需求与产品方向.md` | 建议统一迁入或引用 `04_未来需求与产品方向.md`，并区分已完成、计划中、放弃、需人工确认。 |

## 5. 需要人工确认的内容

以下内容仅从 `docs/` 文档可见，当前未与代码、运行结果或 Git 历史核对，因此需要人工确认：

1. `AGENTS.md` 中说当前项目发展到 `v0.5.1`，但 `docs/v5.1-release-notes.md` 和 `docs/startup-and-test-guide.md` 使用 `V5.1` 表述。`v0.5.1` 与 `V5.1` 是否为同一阶段或命名误差，需人工确认。
2. `docs/v0.5-release-notes.md` 中声称 84 项端到端测试全部通过，需人工确认测试文件、测试命令、执行时间和当前结果。
3. `docs/v5.1-release-notes.md` 中声称新增 AI 智能搜索、56 位用户、133 篇文章、65 个标签、50+ 行业演示数据，需人工确认当前代码和数据库脚本是否一致。
4. `docs/startup-and-test-guide.md` 中的 DeepSeek API 接入、模型选择、环境变量、测试账号和一键启动说明，需人工确认当前仍然有效。
5. `docs/v0.5-release-notes.md` 中提到曾删除 `docs/deepseek-ai-setup-guide.md`，但本次只盘点当前 `docs/`，未追溯历史删除事实，需人工确认。
6. `docs/06_ADR/` 目前只有 `.gitkeep`，是否已有 ADR 存放在其他位置，需人工确认。
7. `docs/09_测试报告.md`、`docs/10_代码Review记录.md`、`docs/11_AI协作记录.md` 均为待填写，不能视为已有正式测试报告、Review 记录或 AI 协作记录。
8. 历史开发记录中的“已完成”“验收结果”“暂未实现”只代表对应文档所属阶段，是否仍符合当前版本需人工确认。

## 6. 后续整理建议

1. 先确认版本命名：统一 `v0.5.1`、`V5.1`、`v5.1` 的关系，避免正式文档中出现两个当前版本。
2. 保留历史文档原貌，不删除、不移动；在正式文档中通过引用方式吸收历史信息。
3. 优先填写 `docs/01_v0.5.1现状盘点.md`，把当前代码可验证事实、历史文档声称事实和需人工确认事项分栏记录。
4. 再填写 `docs/02_v0.5.1需求追溯.md`，把 Day1-Day4、v0.4.1、v0.5、V5.1 中的需求演进整理成追溯表。
5. 将 `v0.4.1-design-note.md`、`v0.4.1-implementation-rules.md`、`v0.5-release-notes.md`、`v5.1-release-notes.md` 中的架构和技术边界内容，人工核对后汇总到 `docs/03_v0.5.1架构追溯.md` 与 `docs/05_技术路线决策报告.md`。
6. 将各历史文档中的后续计划统一汇总到 `docs/04_未来需求与产品方向.md`，并标注“已完成”“计划中”“不再计划”“需人工确认”。
7. 在有可验证测试执行记录后再填写 `docs/09_测试报告.md`；不要直接复制历史版本中的测试通过结论作为当前测试结果。
8. 在实际 Review 和 AI 协作发生后再填写 `docs/10_代码Review记录.md` 与 `docs/11_AI协作记录.md`，避免伪造治理成果。
9. 更新 `docs/startup-and-test-guide.md` 前，先用当前仓库命令逐项验证启动、初始化、AI 配置、测试账号和验收流程。
