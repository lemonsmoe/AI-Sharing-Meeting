# PPT Master 制作源码快照

`ppt_master_6_9_0.zip` 保存本项目实际使用的完整Skill资源树。来源：https://github.com/hugohe3/ppt-master 的 `skills/ppt-master`，2026-11-09下载、2026-11-15归档，入口6.9.0。当时没有可信上游commit；同目录JSON的归档和逐文件SHA256固定本地实际内容，不把版本或摘要说成commit。

原作者Hugo He，MIT许可。完整LICENSE、赞助信息、模板和资源随附许可均保留，另有PPT_MASTER_LICENSE.txt供查阅。仅排除运行生成的__pycache__和pyc，未改写源码。

```text
python scripts/migration/restore_ppt_master.py
python scripts/migration/restore_ppt_master.py --apply
```

标准库脚本先校验归档及全部文件，默认预览；已有不同文件拒绝覆盖。恢复到被忽略的.context_runtime/ppt_skill_candidates/ppt_master。不改全局Skill目录，不安装依赖，不生成PPT或启动服务。

新机先读恢复后的SKILL.md并执行attribution_guard，再按工作流准备Python虚拟环境。完整上游requirements.txt在归档中。本项目使用python-pptx、Pillow、openpyxl、xlsxwriter，以及Flask、PyYAML、skia-pathops、uharfbuzz、resvg-py；不要复制旧机Windows二进制依赖或Codex运行库路径。

原机额外依赖记录（不是跨平台锁文件）：Flask3.1.3、PyYAML6.0.3、skia-pathops0.9.2、uharfbuzz0.57.0、resvg-py0.5.0；附属blinker1.9.0、click8.5.1、itsdangerous2.2.0、Jinja2 3.1.6、MarkupSafe3.0.4、Werkzeug3.1.9。按新机平台安装可用版本并验证。

三页已导出文件可直接查看。新机宋体/微软雅黑、PowerPoint/WPS及浏览器需另核；源码恢复不证明跨机渲染等价。
