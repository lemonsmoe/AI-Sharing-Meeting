# 方法来源与适配

2026-11-09实际读取Anthropic原始Skill：
- https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search/skills/search-strategy/SKILL.md ：全文203行。
- https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search/skills/knowledge-synthesis/SKILL.md ：全文234行，末段另行补读。

采用问题拆解、按来源检索、重复证据合并、保留冲突、主张追溯。企业连接器占位符映射到当前可用web检索和本地rg，不假称已接入Slack等企业来源。原文排序权重不充当校准质量评分。以项目ai-workflow-research门槛作为验收标准；无需部署框架。GitHub主分支可变，当前尚未保存提交哈希或下载快照，此版本固定缺口保留。
