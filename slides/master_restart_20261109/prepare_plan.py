from pathlib import Path

root = Path(__file__).parent / 'master_preview_20261109'
spec = '''<!-- ppt-master-schema: design-spec/v1 -->
# Master Preview - Design Spec

## I. Project Information
| Item | Value |
| --- | --- |
| Project Name | master_preview_20261109 |
| Canvas Format | ppt169 1280×720 |
| Page Count | 3 |
| Primary Language | zh-CN |
| Target Audience | 全体部门与领导，编程基础不一 |
| Communication Intent | 科普介绍为主、教学为辅，理解AI协作及可用成果 |
| Desired Audience Outcome | 理解明确任务、组件配合和核验产物的作用 |
| Core Message / Ask / Action | 清楚交代任务，让组件配合，再核验来源 |
| Delivery Context | 中文现场分享；三页代表稿，不代表整场内容比例 |
| Artifact Afterlife | 可编辑PPTX与讲者备注，供审阅与复用 |
| Reading Mode | presentation |
| Content Strategy | balanced default；用户材料发散度留空 |
| Design Style | A 资料批注式课堂；主对话在委托范围内选择 |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — 用户明确需要讲稿 |
| Custom Animations | disabled — 委托方案先核验静态表达 |
| Narration Audio | disabled — 用户暂缓视频配音 |
| Created Date | 2026-11-12 |

## II. Canvas Specification
| Property | Value |
| --- | --- |
| Format | ppt169 |
| Dimensions | 1280×720 |
| viewBox | `0 0 1280 720` |
| Margins | 48 px |
| Content Area | 48 40 1184 640 |

## III. Visual Theme
### Theme Style
- **Mode**: custom
- **Mode Behavior**: 以一句愿望进入真实提示词，解释组件配合，最后展示能继续使用的产物；介绍意义先于操作细节。
- **Visual style**: custom
- **Visual Style Behavior**: 暖白纸面、墨色细线和深红批注，材料正文、关系图、表格分别承担三页主视觉；通过间距和字体层级区分信息，边注对准所解释对象。
- **Theme**: 资料批注式课堂
- **Tone**: 平实、清楚、有依据
### Color Scheme
| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #F7F4EE | 纸面 |
| Secondary background | #EDE7DC | 材料底 |
| Primary | #243142 | 标题与结构 |
| Accent | #B8372C | 编号与变化 |
| Secondary accent | #297B83 | 工具连接 |
| Body text | #202933 | 正文 |
| Secondary text | #59616C | 辅助说明 |
| Divider | #C9C2B8 | 分隔 |

## IV. Typography System
### Font Plan
| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | 宋体对比 | SimSun | Georgia | serif |
| Body | 清晰黑体 | Microsoft YaHei | Arial | sans-serif |
- **Title stack**: SimSun, Georgia
- **Body stack**: Microsoft YaHei, Arial
### Font Size Hierarchy
| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 32 |
| Title | 48 |
| Subtitle | 36 |
| Annotation | 26 |
| Footnote | 18 |

## V. Layout Principles
- **Hierarchy direction**: 结论标题→主要材料→解释与边界
- **Composition tendency**: 批注、协作图、宽表格随语义变化
- **Cross-page continuity**: 小编号和红色重点持续，材料形态变化
- **Spacing posture**: open
- **Spacing anchors**: margin 48, block gap 24, gutter 40, corner radius 0, body leading 44

## VI. Icon Usage Specification
- **Primary bundled library**: tabler-outline
- **Stroke Width**: 3
| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List
| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline
### Part 1: 三种表达验证
#### Slide 01 - prompt
- **Audience move**: 知道说需求→理解可验收任务
- **Relationships**: 请求与补充任务是contrast；五条批注与原句是link
- **Composition**: 完整提示词为主体，右边短批注
- **Title**: 把“整理一下”变成能验收的任务
- **Core message**: 交代清楚交付物，AI才知道做到哪一步
- **Cover impact**: “帮我整理一下会议记录”这一熟悉愿望成为具体任务的入口
- **Content**:
  - 宽泛请求：帮我整理一下会议记录。
  - 依据会议原文和会后补充，输出一页纪要和 Excel 行动清单。会后确认覆盖原安排；每个待办列负责人、期限、来源。未说明的信息留空或标为待确认，采购建议不要写成批准。完成后检查日期变更和来源能否对上。
  - 目标、材料、格式、边界、验收五类批注；生成后仍核对原文。
#### Slide 02 - collaboration
- **Audience move**: 以为术语是升级链→理解一次工作中的不同职责
- **Relationships**: 用户目标到Agent到成果是order；Skill、接口、记录与工作是link；运行环境与工作是membership
- **Composition**: 运行框架包围工作过程，支持组件接入对应位置
- **Title**: 这些组件，在同一次工作里配合
- **Core message**: 不是相互淘汰，而是各自承担不同职责
- **Content**:
  - 提示词说明目标；Agent读取材料、选择下一步、调用工具、检查结果，交付纪要和表格。
  - Skill提供可复用做法；API/MCP连接数据与操作，MCP可选，Skill可无MCP。
  - 项目记录保存决定与进度，不等于修改模型参数。
  - Harness负责环境、调度、检查与接续；图为概念示意，不表示公司已接入。
#### Slide 03 - evidence
- **Audience move**: 看见漂亮文字→看见能跟进且可核对的产物
- **Relationships**: 原期限与新期限是contrast；来源与记录是link
- **Composition**: 三行表格为主体，日期变化与未批准状态留在下方
- **Title**: 结果能跟进，还要能对回来源
- **Core message**: 有来源、分清变更与未知，产物才方便继续用
- **Content**:
  - 更新价格表，周，11月9日12:00，M03/C02；收齐两家支架报价，周，11月10日17:00，C05/C06；交测试摘要，林，11月11日12:00，M02/C01。
  - 测试摘要原11月10日18:00被会后确认覆盖；采购仍未批准；正式演示11月13日15:00会议室A。
  - 模拟材料，Codex实际生成；不是其他产品实测，不声称节时比例。
- **Visualization**: action-table，三条待办与四个字段的文本表格
- **Native-ready**: action-table=yes
- **Data class**: scenario

## X. Speaker Notes Requirements
- **Generation**: enabled
- **Filename**: match each SVG filename under notes/
- **Content**: 依据最终画面与原始材料，自然讲述，说明模拟与概念边界
- **Total duration**: 约6分钟，未试讲
- **Notes style**: conversational
- **Presentation purpose**: 科普介绍AI协作意义，辅以可理解的办公案例
'''
(root / 'design_spec.md').write_text(spec, encoding='utf-8')
