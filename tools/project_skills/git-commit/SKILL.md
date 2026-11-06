---
name: git-commit
description: 以精简、可审计、可回退的方式执行 Git 操作。用于检查仓库、确定基线、规范分支、创建外置 worktree、审查和提交当前任务、集成已验收提交，以及在明确授权后推送、打 tag 或整理旧分支；默认保护脏工作树、现场配置、子模块和未验收成果。
---

# Git 操作规范

用最少但必要的流程完成 Git 工作。先确认事实，再执行变更；不为了“整洁”破坏可回退性。

## 1. 权限边界

- `status`、`diff`、`log`、`show`、`branch --contains`、`worktree list` 等只读检查可直接执行。
- 创建任务分支或 worktree，应有已确认的任务和明确基线。
- 只有用户明确要求“提交”“工作后保存”或等价表达时才创建提交。
- 合并、cherry-pick 到验收主线、推送、打 tag、发布、删除/重命名已共享分支，分别需要明确授权；提交授权不自动包含这些动作。
- 禁止用 `reset --hard`、强推、批量删分支或清理未跟踪文件处理不确定状态。

## 2. 先确认仓库事实

至少检查：

```powershell
git status --short --branch
git rev-parse HEAD
git worktree list --porcelain
git remote -v
```

- 从仓库 `AGENTS.md`、当前上下文或 runbook 确认实际验收基线；不要假定一定是 `main`。
- 发现脏工作树、子模块变化、现场配置、构建产物或他人改动时，先划清任务文件，禁止重置或顺手提交。
- 需要远端新状态时只做明确范围的 `fetch`；脏工作树中不要直接 `pull` 或隐式 rebase。

## 3. 简化分支模型

- 验收基线：使用项目记录的当前基线分支；`main` 仅在项目确实以其为已验收主线时使用。
- 普通任务：`task/<三位编号>-<英文短语>`，例如 `task/002-startup-diagnostics`。
- 打回重做：`task/<三位编号>-r<修订号>-<英文短语>`。
- `release/<版本>` 和 `hotfix/<版本>-<短语>` 只在正式发布维护确有需要时创建。
- 分支名使用小写英文、数字和连字符；不要把人员姓名、日期、含糊的 `test/new/final` 当分支名。

已有分支不批量改名。规范化前先记录：当前 worktree、远端跟踪关系、独有提交、是否已发布、替代分支和回退方式。共享分支采用“创建规范新分支 -> 验证 -> 更新协作入口 -> 获批后再归档旧分支”，不直接破坏性重命名。

## 4. 任务隔离

- 默认一个实现任务对应一个分支和一个 worktree。
- worktree 放在仓库外的兄弟目录 `<repo_parent>/<repo_name>_wt/<task>`，避免污染搜索、打包和暂存。
- 从精确基线 SHA 创建，不从碰巧打开的分支猜测：

```powershell
git worktree add -b task/002-startup-diagnostics `
  D:\code\Project\<repo_name>_wt\002-startup-diagnostics <baseline_sha>
```

- 多日、多人或高风险任务要保存简短 branch brief，至少记录目标、基线 SHA、范围、禁改项、验收和关键文件。小型单次修复可由清晰的任务说明代替，不强制增加形式文档。

## 5. 修改与提交

提交前：

```powershell
git status --short --branch
git diff --stat -- <paths>
git diff -- <paths>
```

- 一次提交只表达一个可审查、可回退的意图。
- 显式暂存任务文件：`git add -- <file1> <file2>`；禁止默认使用 `git add .`、`git add -A` 或 `git commit -a`。
- 暂存后检查：

```powershell
git diff --cached --name-only
git diff --cached --stat
git diff --cached
```

- 默认使用中文 Conventional Commit 风格：`类型(范围): 中文摘要`。常用类型只保留 `feat`、`fix`、`docs`、`test`、`build`、`refactor`、`chore`。
- 正文说明关键行为、验证结果和刻意未改的边界；不要写空泛的“更新代码”。
- 钩子或测试失败时先定位原因，不使用 `--no-verify` 绕过，除非用户明确批准且风险已说明。

## 6. 验证与集成

- 提交前后运行与风险相称的测试，并明确区分自动化、仿真、离线证据和真机验收。
- 优先通过 PR/MR 审查后合入验收主线；本地项目采用 cherry-pick 流程时，只摘取已确认的原子提交，并记录来源 SHA。
- 集成前确认目标分支干净、基线正确、提交未重复吸收；可使用 `git cherry`、`merge-base --is-ancestor` 或 patch 等价检查。
- 不自动解决含义不明确的冲突，不把现场配置或无关脏修改带入集成。

## 7. 推送、tag 与整理

- 推送前报告目标 remote、分支和将要推送的提交范围；未经授权不执行。
- tag 只标识不可变源码点，不等同于测试或真机验收通过。正式 tag 应与发布 manifest、包哈希和验收记录对应。
- 删除 worktree/分支前依次确认：工作树干净、无未跟踪重要文件、独有提交已保存、远端或归档可恢复、替代入口已生效，并再次获得用户确认。
- 子模块先在子仓库提交并推送可达提交，再单独更新外层 gitlink；不得让外层指向未发布的子模块提交。

## 8. 完成回报

按实际执行内容报告：

- 仓库、基线、任务分支和 worktree；
- 提交哈希、标题、文件清单；
- 测试及其证据等级；
- 保留的脏修改、未完成验收和回退点；
- 是否执行了集成、推送、tag、发布或清理。未执行的动作必须明确写“未执行”。
