# 迁移核验

2026-11-06；任务 TASK-20261106-882e82df。机器可读摘要见 verification.json。

## 已完成

- 初始远端 ls-remote 成功，未返回分支；本地原本没有 Git，已创建 main 并配置用户指定 origin。
- 初始提交 2985d7c 的 1,159 个受控文件，在独立干净克隆中逐文件 SHA-256 一致。
- 克隆中执行 bootstrap 预览、apply、task status、discussion sync、workflow doctor，全部退出 0；6 个讨论议题无未整理条目，新运行库没有旧任务认领。
- 原项目 project.json、workflow_install.json、.codex/hooks.json 哈希保持不变。只在克隆中生成新 Hook 和本机绑定。
- 7 项保护测试通过：预览不写入、应用后路径与真实身份一致、重复迁移拒绝、已有任务库保护、已有 Hook 保护、身份缺失拒绝、上下文脚本改变拒绝、源目录保护（应用与重复迁移在同一项中）。测试首次发现 SQLite 连接未显式关闭导致 Windows 临时目录清理失败，已修正并全量重跑通过。
- 对候选文件和可读取的压缩包文本扫描常见私钥、GitHub/API/Bearer/AWS 密钥模式，无命中。忽略规则确认排除 .codex、.context_runtime、node_modules 和下载的语音运行库。模式扫描不等于所有形式的敏感信息识别。
- 克隆中重绑媒体依赖路径，15 个变更的 JavaScript 模块通过 node --check。没有生成新内容，没有声称新版本 API 或完整生产兼容。
- 自定义 Skill 23 文件快照逐项哈希记录。任务与操作历史已导出，讨论和最新质量否决随仓库保存。

## 验证边界

测试是在同一 Windows 机器的独立克隆中完成；第二台机器、非 Windows、Hook 信任及真实生命周期、字体、Office/WPS、浏览器和媒体完整运行尚未验证。离线 doctor 明确保留 Hook 提示。

已有样片与 PPT 的用户质量否决不变，所有生产继续暂停。迁移事件中追加远端提交与同步结果；不要据此升级创作验收状态。
