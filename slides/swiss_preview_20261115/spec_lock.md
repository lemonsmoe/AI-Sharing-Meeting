<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock
## canvas
- viewBox: 0 0 1280 720
- format: ppt169
## communication
- primary_language: zh-CN
- audience: 全体部门与领导
- objective: 能描述一项明确可验收的任务，并理解普通办公人员为什么关心 Agent
- core_message: 给 AI 一项明确、能验收的工作
- consumption_mode: presentation
## mode
- mode: custom
- mode_behavior: 成品先行、真任务对照、人物原话进场。
## visual_style
- visual_style: custom
- visual_style_behavior: 米白底、黑字、公司红，非对称网格和有目的的留白。
## colors
- background: #F6F3EC
- secondary_bg: #F6F3EC
- primary: #171715
- accent: #C50000
- secondary_accent: #C50000
- body_text: #171715
- secondary_text: #171715
- divider: #171715
## typography
- font_family: Microsoft YaHei
- body_family: Microsoft YaHei
- title_family: Microsoft YaHei
- title: 58
- body: 32
- subtitle: 32
- annotation: 24
## icons
- library: none
- inventory: none
## page_rhythm
- P01: anchor
- P02: dense
- P03: breathing
## pptx_structure
- mode: flat
## images
- prompt_slide: images/prompt_slide.png | source=user | crop=no-crop
- peter_steinberger: images/peter_steinberger.jpg | source=user | crop=no-crop
## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
