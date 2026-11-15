<!-- ppt-master-schema: design-spec/v1 -->
# Swiss Preview - Design Spec

## I. Project Information
| Item | Value |
| --- | --- |
| Project Name | swiss_preview_20261115 |
| Canvas Format | ppt169 1280×720 |
| Page Count | 3 |
| Primary Language | zh-CN |
| Target Audience | 全体部门与领导 |
| Communication Intent | 从这套课件的成品和制作需求入手，理解如何交代可交付的任务，并引入人人可用的办公 Agent |
| Desired Audience Outcome | 能描述一个具体交付标准，并理解 Agent 对普通办公人员的意义 |
| Core Message / Ask / Action | 给 AI 一项明确、能验收的工作 |
| Delivery Context | 中文现场投屏，三页分别对应全稿第1、8、13页 |
| Artifact Afterlife | 可编辑 PowerPoint 和逐页讲稿 |
| Reading Mode | presentation |
| Content Strategy | 使用本次制作的真实要求，办公案例留给全稿 |
| Design Style | 公司模板的红色与左轴，Swiss Grid 的非对称网格、开放留白与黑红层级 |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — 用户要求逐页照读稿 |
| Custom Animations | disabled — 静态样稿供审阅 |
| Narration Audio | disabled — 本轮交付为PPT和讲稿 |
| Created Date | 2026-11-15 |

## II. Canvas Specification
| Property | Value |
| --- | --- |
| Format | ppt169 |
| Dimensions | 1280×720 |
| viewBox | `0 0 1280 720` |
| Margins | 72 px |
| Content Area | 72 64 1136 592 |

## III. Visual Theme
### Theme Style
- **Mode**: custom
- **Mode Behavior**: 成品先行、真任务对照、人物原话进场。
- **Visual style**: custom
- **Visual Style Behavior**: 米白底上用黑字、公司红和细线组织阅读。大块空白来自资料与文字的边缘对齐。
- **Theme**: Swiss Grid 课件样稿
- **Tone**: 直接、克制、具体
### Color Scheme
| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #F6F3EC | 暖米白 |
| Secondary background | #F6F3EC | 图片承载区 |
| Primary | #171715 | 文字 |
| Accent | #C50000 | 关键变化 |
| Secondary accent | #C50000 | 重点标记 |
| Body text | #171715 | 正文 |
| Secondary text | #171715 | 署名、列标 |
| Divider | #171715 | 分隔线以低透明度衬托 |

## IV. Typography System
### Font Plan
| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | 人文无衬线粗体 | Microsoft YaHei | Microsoft YaHei | sans-serif |
| Body | 人文无衬线常规 | Microsoft YaHei | Microsoft YaHei | sans-serif |
- **Title stack**: Microsoft YaHei
- **Body stack**: Microsoft YaHei
### Font Size Hierarchy
| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 32 |
| Title | 58 |
| Subtitle | 32 |
| Annotation | 24 |

## V. Layout Principles
- **Hierarchy direction**: 大标题与主证据优先，其次为读图必需的标签。
- **Composition tendency**: 成品预览、左右对照、人物与引语。
- **Cross-page continuity**: 共用左轴和边距，有必要时使用红色标记。
- **Spacing posture**: open
- **Spacing anchors**: margin 72, gutter 48, leading 44, radius 0

## VI. Icon Usage Specification
- **Primary bundled library**: none
| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List
| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prompt_slide.png | 1280×720 | 16:9 | 封面展示同一套样稿的实际第二页 | Screenshot | 右半边放完整页面缩略图 | no-crop | user | Existing | 本样稿第2页的 PowerPoint 原生渲染 | allow | evidence |
| peter_steinberger.jpg | 460×460 | 1:1 | 与原话对应的真人照片 | Photo | 左侧方形照片邻接右侧引语 | no-crop | user | Existing | 主对话提供的本人官网头像 peter-avatar.jpg | avoid | subject |

## IX. Content Outline
### Part 1: 开场、提示词、Agent
#### Slide 01 - cover
- **Audience move**: 从正在看的课件入手，意识到本次分享会拆解一项真实交付
- **Relationships**: 标题与样稿预览是link
- **Composition**: 左侧两行题目，右侧为实际样稿页。
- **Title**: AI 怎样帮我们把工作做完？
- **Core message**: 用这套课件说明任务怎样从需求走到可编辑交付。
- **Cover impact**: 实际提示词示例页作为开场的工作成果。
- **Content**:
  - 这次分享的 PPT，就是例子。
  - 实际课件样稿页面。
#### Slide 02 - prompt
- **Audience move**: 从模糊要求走向具体的制作和验收要求
- **Relationships**: 模糊请求与具体要求是contrast；三条具体要求按范围、参考、交付组织
- **Composition**: 左窄右宽，细线连接三个制作要求。
- **Title**: 把「做个 PPT」说具体
- **Core message**: 明确听众和时长，告诉 AI 看哪些资料，说明交付物。
- **Content**:
  - 一句话需求：帮我做个 AI 分享 PPT。
  - 听众是全体同事，分享少于一小时。参考公司模板和 Swiss Grid。交付可编辑 PPT 和能照读的讲稿。
#### Slide 03 - quote
- **Audience move**: 从任务描述进入普通人如何使用 Agent
- **Relationships**: 原话、译文与有署名的头像是link
- **Composition**: 左方形肖像，右英文原话、中文译文及一行署名。
- **Title**: My next mission is to build an agent that even my mum can use.
- **Core message**: 普通人也能用 Agent 是一个设计目标。
- **Content**:
  - 我的下一个目标，是做出一个连我妈妈也会用的智能体。
  - Peter Steinberger，OpenClaw 创始人。

## X. Speaker Notes Requirements
- **Generation**: enabled
- **Filename**: match each SVG filename under notes/
- **Content**: 中文照读稿，以课件及引语来源为依据
- **Total duration**: 约三分钟，现场计时待排练
- **Notes style**: conversational
- **Presentation purpose**: 科普办公 AI 及其协作方法。
