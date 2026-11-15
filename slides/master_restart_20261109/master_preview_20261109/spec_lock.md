<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock
## canvas
- viewBox: 0 0 1280 720
- format: ppt169
## communication
- primary_language: zh-CN
- audience: 全体部门与领导，编程基础不一
- objective: 科普介绍为主，让观众理解明确任务、组件配合和结果核验
- core_message: 清楚交代任务，让组件配合，再核验来源
- consumption_mode: presentation
## mode
- mode: custom
- mode_behavior: 由熟悉请求进入具体任务，解释配合，再以可核验成果收束
## visual_style
- visual_style: custom
- visual_style_behavior: 暖白纸面、墨色细线、深红批注；正文、关系图、宽表格分别承担主视觉
## colors
- background: #F7F4EE
- secondary_bg: #EDE7DC
- primary: #243142
- accent: #B8372C
- secondary_accent: #297B83
- body_text: #202933
- secondary_text: #59616C
- divider: #C9C2B8
## typography
- font_family: Microsoft YaHei, Arial
- body_family: Microsoft YaHei, Arial
- title_family: SimSun, Georgia
- body: 32
- title: 48
- subtitle: 36
- annotation: 26
- footnote: 18
## icons
- library: tabler-outline
- stroke_width: 3
- inventory: none
## page_rhythm
- P01: anchor
- P02: dense
- P03: dense
## pptx_structure
- mode: flat
## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
