# 参考 PPT 文本提取

仅提取文本，不代表已完成视觉审查或事实核验。

## 第 1 页
文献精读 · PAPER READING SERIES
深度学习如何「看懂」
复杂结构变异
从单样本解析、跨样本比较到群体泛基因组图谱 —— 方法三部曲
SVision
Nature Methods · 2022
单样本复杂 SV 的图像化解析
SVision-pro
Nature Biotechnology · 2025
de novo / somatic 比较检测
Swave
Nature Genetics · 2026
泛基因组图上的群体 SV 目录
同一方法脉络：西安交通大学 Kai Ye 团队（xjtu-omics）
2026 年 10 月 · 组会分享

## 第 2 页
OVERVIEW · 本次分享路线
三篇论文，一条不断扩展的主线
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
2
I
SVision
Nature Methods · 2022
任务
单样本 long-read 复杂 SV 发现与解析
输入
长读长比对 BAM（HiFi / ONT）
核心
去噪相似图像 + CNN 组件识别 + CSV graph
II
SVision-pro
Nature Biotechnology · 2025
任务
case–control 比较：de novo / somatic
输入
case + control 长读长 BAM
核心
比较图像 + Lite-U-Net 实例分割 + AF 基因分型
III
Swave
Nature Genetics · 2026
任务
群体水平 SSV/CSV 分类与基因分型
输入
参考基因组 + 群体组装（泛基因组图）
核心
图等位路径 + 投影波 + Bi-LSTM 分类
贯穿三部曲的共同主线
比对证据  (alignment)
可学习表示  (image / wave)
深度学习识别  基本成分
组合解释  复杂结构 CSV
三篇论文共享同一设计哲学：不枚举复杂事件类型，而是识别有限的基本成分、再按结构关系组合

## 第 3 页
BACKGROUND · 背景知识
结构变异：SSV 与 CSV
Lin et al. Nat Methods 2022, Extended Data Fig. 1
3
结构变异 (SV)
  通常指 ≥ 50 bp 的基因组大片段重排
长读长测序（HiFi / ONT）让 read 有机会横跨整个事件
SSV 简单结构变异
单个事件可用一个简单模型描述：缺失、插入、倒位、重复等
CSV 复杂结构变异
一个事件内部同时包含多个断点与多种成分（del + inv + dup …），片段在样本基因组中的连接方式才是真正要回答的问题
一个 CSV 事件的解剖（示意）
REF
A
B
C
D
E
ALT
A
C ←
C ←
D
E
B 缺失 → DEL
C 双拷贝 → DUP
拷贝方向反转 → INV
传统 caller 容易输出三条孤立记录（DEL / INV / DUP），丢失「它们属于同一事件」的信息
SVision Extended Data Fig. 1 | 简单与复杂 SV 图例（论文原图）
论文图例给出的成分词表：DEL / INS / INV / tDUP /
DUP(dispersed) —— 后续三篇论文的深度
学习模型都在识别这一级别的基本成分

## 第 4 页
BACKGROUND · 问题定义
为什么 CSV 难以检测：三个层面
Lin et al. Nat Methods 2022, Introduction & Discussion
4
① 组合爆炸
预定义模型无法穷举
传统 caller = 比对模式 → 模板匹配。DEL+INV、DUP+INV+DEL…组合空间迅速爆炸，未知 CSV 无模板可匹配
② 重复干扰
比对模式本身被污染
参考基因组自身含重复：read 与两个同源拷贝同时相似，dotplot 天然出现多条平行线，与 DUP 的信号混淆
③ 表示缺失
人工命名不可计算比较
DelInvDup / InvDup…命名标准不统一；新结构无法与已有事件做算法层面的同构比较，缺乏统一机器可读表示
重复序列造成的假 DUP 信号（示意）
REF 坐标 →
read
参考区有两个同源拷贝 B、B′：正常 read 的匹配线（浅）与
真实 DUP 的证据（深）在图像上几乎无法区分
三个问题的共同根源：
把「比对模式」直接当成「生物学解释」。三篇论文各自重造了中间表示，让 SV 类型从表示中自然产生，而不是先验地匹配。

## 第 5 页
OVERVIEW · 三篇论文一览
同一团队的方法演化：2022 → 2025 → 2026
5
2022 · 6
SVision
Nat Methods 19:1232
输入
long-read BAM
表示
VAR–REF 去噪图像
模型
AlexNet（分类）
输出
CSV graph / GFA
2024 · 3 在线 / 2025
SVision-pro
Nat Biotechnol 43:181
输入
case + control BAM
表示
比较图像 + ACT 轨道
模型
Lite-U-Net（分割）
输出
跨样本差异 + 基因型
2026 · 3
Swave
Nat Genet 58:664
输入
群体组装 + 泛基因组图
表示
等位序列投影波
模型
Bi-LSTM（序列）
输出
群体结构目录 + AF
表示演化：
read 级去噪图像（一条 read 与参考的结构关系）→ 双样本比较图像（结构与支持证据同图）→ 等位序列投影波（把二维 dotplot 压成一维信号）
任务演化：
单样本发现（这里有什么 SV）→ case–control 比较（两边差在哪、AF 变没变）→ 群体目录（谁携带、频率多少、多等位如何共存）

## 第 6 页
I
PART I
SVision
Lin J., Ye K. et al. · Nature Methods · 2022
把长读长比对几何编码成图像，用 CNN 识别基本成分，用 graph 重建复杂事件
面向 HiFi / ONT 长读长数据的单样本 complex SV 解析框架
本部分内容
三大动机
Encoder 编码器
背景相减
tMOR 分割
AlexNet
CSV graph
结果与验证

## 第 7 页
PART I · SVISION
总体框架：三个模块，一条流水线
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w
7
Fig. 1 | SVision overview（论文原图：Encoder / tMOR / Illustrator）
1  
Encoder 编码器
从异常比对提取 VAR/REF，k-mer 局部重比对恢复隐藏对应关系，编码成去噪相似图像
2  
tMOR 定向多目标识别
先把长 read 中的多个事件切成 one-variant image，再在断点附近提取 SOI 交给 CNN 分类
3  
Illustrator 绘图器
按样本基因组真实邻接关系连接片段，生成 CSV graph，用拓扑定义与比较复杂结构
常见误读
SVision ≠ “BAM → CNN → SV 类型”。大量环节是结构化算法与领域知识，CNN 只处在链条中间

## 第 8 页
PART I · SVISION
方法哲学：一条六步转换链
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w
8
01
收集异常比对
CIGAR I/D ≥50bp + split / supplementary
提取 VAR 与 REF
02
局部 k-mer 重比对
k=10 哈希匹配 → 延伸 ≥50bp →
共线链接 chaining
03
序列转图像
X=REF, Y=VAR
matched / duplicated / reversed 三通道
04
背景相减
VAR–REF 图像 − REF–REF 图像
= 去除参考内在重复的 denoised image
05
事件分割
one-variant image → SOI
断点级局部结构对象
06
CNN + graph 重建
AlexNet 五分类 → Illustrator
按邻接关系重建 CSV graph
关键理解：
问题被转化为「恢复 segment 对应关系 → 去除参考背景 → 分解断点组件 → 重建样本结构路径」，而不是直接从 noisy alignment 猜 SV 类型

## 第 9 页
PART I · SVISION / ENCODER ①
Encoder ①：不信任 CIGAR —— VAR 提取与 k-mer 重比对
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Supplementary Note 3.1
9
VAR / REF 是什么
VAR = 携带变异信号的 read 局部序列；REF = 对应参考区域。来源两类：intra-read CIGAR（I / D / 未匹配序列 ≥50bp）与 split / supplementary alignment
为什么重新比对
aligner 的 CIGAR 只是一种比对表示 ≠ 生物学解释。一段 500bp 的 “插入”可能实际来自参考区另一处的拷贝、甚至反向拷贝
两步重比对
① k-mer 匹配：REF 建 k=10 哈希表，扫 VAR k-mer，命中即向两端延伸，≥50bp 才保留；② 链接：VAR/REF 位移比位于 0.8–1.2 且 gap 有限时 chain 成更长 segment
示意：一段 CIGAR “插入” 的真实来历
read
primary A
500bp “I”
suppl. B
把 “I” 与 primary/supplementary 之间的 gap 重新局部比对到 REF：
k=10 哈希
匹配延伸
≥50bp
segment
chaining
0.8–1.2
结果：原先无法解释的序列被恢复为「REF-C 反向同源」——这就是后面识别 inverted DUP 的证据
启发性设计：
不完全相信 aligner 给出的 block 结构，而是重建 segment 级对应关系 —— 复杂 SV 的信息往往藏在 aligner “放弃解释” 的地方

## 第 10 页
PART I · SVISION / ENCODER ②
Encoder ②：序列扩展与 sequence-to-image 编码
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Supplementary Note 3.1
10
序列扩展（scaling）
只看异常区不够 —— 断点两侧还需要正常锚。设变异签名长度为 l，VAR 向两侧各扩约 2l，纳入 concordant 侧翼序列后再裁剪
图像坐标定义
X 轴 = REF 坐标，Y 轴 = VAR 坐标 —— 与经典 dotplot 同构：正常共线 = ↘ 对角线；反向比对 = ↗；一个 REF 位点对应多个 VAR 位点 = 平行线
编码的本质
不是把 A/C/G/T 碱基画成图片，而是把 segment 级坐标关系编码为 224×224×3 的结构图像 —— 强领域先验的手工表示
三个通道分别编码三种结构关系（示意）
matched 通道
正向同源匹配
duplicated 通道
同一 REF 位点 → 多个 VAR 位点
reversed 通道
segment 相对 REF 反向
DUP 为什么“看得见”
REF: A B C → VAR: A B B C 时，同一 x 坐标在竖直方向出现两个匹配 —— duplicated 通道在进入 CNN 之前就已显式编码了 “one REF locus → multiple VAR loci”

## 第 11 页
PART I · SVISION / ENCODER ③
Encoder ③：REF-to-REF 背景相减 —— 全文最漂亮的一步
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Supplementary Note 3.1
11
去噪 = 在参考坐标维度上比较 segment 重叠
VAR-to-REF image（3 条线）
−  REF-to-REF image（2 条线）
=  denoised image（1 条线）
问题
参考基因组自身含重复：VAR 中正常的 B 也能同时匹配两个参考拷贝，图像上出现貌似 DUP 的多条匹配线，但什么 SV 都没发生
解法
先构建 REF 与自身的 similarity map 作为 background；在参考坐标维度比较 segment 重叠，参考内在相似性被抵消，差异 >50bp 的非重叠部分保留
本质
“这种相似关系，参考自己本来就有吗？” 有 → 背景；VAR 相对 REF 新增 / 消失 / 反向的 → 结构信号
最可迁移的思想：
先把「正常 / 背景」显式建模，再看 observation 相对它发生了什么变化 —— 后两篇论文分别以双轨道对照与双背景波继承了这一思想

## 第 12 页
PART I · SVISION / tMOR ①
tMOR ①：major / minor segment 与 one-variant image
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w
12
Extended Data Fig. 5 | one-variant image 的构建与聚类（论文原图）
major segment
来自 aligner / CIGAR 的正常匹配大块 —— 事件两侧可靠的 backbone 锚
minor segment
三类来源：k-mer 重比对新发现的 segment、inverted segment、被其它 segment 完全覆盖者 —— 事件内部的额外结构解释
one-variant image
相邻两个 major（i 与 i+1）+ 夹在中间的所有 minor，构成“左锚 + 内部重排成分 + 右锚”的单事件图像
跨 read 聚类
不同 read 的 image 用位置差 + 跨度差定义距离 Dist = Pos + Span，层级聚类后 cluster size 即支持 read 数
为什么先切再认：
一条长 read 可能跨多个 SV，整图分类无法回答“这里是几个事件”；read support 是在结构图像层面而非 read 层面形成的

## 第 13 页
PART I · SVISION / tMOR ②
tMOR ②：SOI —— 断点级的结构对象
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Supplementary Fig. S5
13
SOI 是什么
Segment of Interest：断点附近由不连续 segment 构成的局部结构对象，是交给 CNN 的最终单元
怎么找
不用通用目标检测（selective search / EdgeBoxes）：基因组相似图像没有纹理、颜色、自然边界，只有线段 —— 用领域知识直接定位：segment 不连续处 ≈ 断点
CNN 认什么
五个 elementary 类型：DEL / INS / INV / DUP / tDUP。SOI-1→DEL、SOI-2→INV、SOI-3→DUP … 复杂事件 = 多个 SOI 的组合，无需预先定义任何完整 CSV 类别
REF 坐标 →
read
坐标
SOI-1 · DEL
SOI-2 · INV
SOI-3 · DUP
segment 不连续处 ≈ 断点：每个断点邻域构成一个 SOI（示意）
DEL
INS
INV
DUP
tDUP
CNN 输出：每个 SOI 一个基本成分标签

## 第 14 页
PART I · SVISION / 深度学习
AlexNet：一个“普通”网络，五类基本成分
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Methods
14
网络结构
▪ 
输入 224 × 224 × 3（三通道结构图像）
▪ 
5 个卷积层 + 3 个全连接层（经典 AlexNet）
▪ 
输出：五分类 SoftMax
▪ 
ImageNet 预训练参数迁移，主要微调后三个全连接层
DEL
INS
INV
DUP
tDUP
训练设置
▪ 
75,000 个 SOI = 15,000 × 5 类
▪ 
约一半真实 SV、一半模拟 —— 平衡真实数据中 INS/DEL 占绝对优势、INV/DUP/tDUP 不足的问题
▪ 
learning rate 0.001 · batch 64 · 5,000 iterations
▪ 
10-fold 交叉验证 + 独立 7,500 SOI 测试集
作者自己的定位（Supplementary Discussion）
novelty 不在发明新网络：SVision 把 SV 检测从 sequence problem 转化为 image recognition problem，AlexNet 只被当作特征提取器。真正让 CNN「能用」的是前面整套知识驱动的表示
泛化能力的边界：
不需要预定义「复杂组合模板」≠ 没有先验。它预定义的是基本结构语言（matched/inverted/duplicated + 五类成分），新组合可以识别，全新基本关系依然在词表之外

## 第 15 页
PART I · SVISION / ILLUSTRATOR
Illustrator：用 graph 表达复杂事件的内部结构
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w
15
示例：REF = A·B·C·D → ALT = A·C⁻·C⁻·D 的 CSV graph
S1 (A)
D1 (C⁻)
D1′ (C⁻)
S4 (D)
adjacency edge：样本基因组中的真实邻接（ALT 路径）
REF · C
duplication edge：
拷贝来源 → 参考原件
graph 的定义
▪ 
节点三类：skeleton（backbone 片段）、insertion（无参考对应）、duplication（可溯源到参考来源）
▪ 
节点携带属性 (Seq, Pos, Strand)
▪ 
路径编码：S1⁺ → D1⁻ → D1′⁻ → S4⁺ ，⁺/⁻ 为遍历方向 —— 哪些片段、什么顺序、什么方向、是否重复，一目了然
为什么 graph 优于 “DelInvDup” 标签
命名是人工语义标签，标准不统一、无法算法比较；graph 从拓扑定义 CSV —— 两项研究即使命名不同，拓扑相同即可视为同一结构
质量评分（0–100）
▪ 
结构一致性：多个支持 image 间 segment 位移 / 长度非线性分数的离散度 —— 越一致越可信
▪ 
CNN 可靠性：各 SOI SoftMax 概率均值 ×100
▪ 
两因素归一化整合，而非 “概率 >0.5 即 PASS”

## 第 16 页
PART I · SVISION / ILLUSTRATOR
graph 的比较、同构与输出
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Extended Data Fig. 10 / S15
16
Extended Data Fig. 10 | graph 及其镜像对称结构（论文原图）
两个 CSV graph 是否同一结构？比较流程
节点数 / 边数 不同 → 直接判异
graph path 拓扑是否一致
构造 mirror graph (5′→3′ 两方向观察)
exact / isomorphic / different
关键先验：节点可按参考坐标排序，把一般 NP 难的图同构问题简化为有序路径比较
输出格式
graph 可导出 GFA；VCF 记录保留 BKPS（断点集）、GraphID、GFA_FILE_PREFIX 等结构字段 —— 复杂结构成为可追溯、可比较的一等公民
定位提醒
这是对「已检出的局部 CSV」的结构化表示，不是全基因组 / 染色体级重排图 —— 适合一条或若干长 read 能跨越的局部复杂事件

## 第 17 页
PART I · SVISION / 结果 ①
基准测试：简单 SV 追平最优，CSV 断层领先
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Fig. 1c / Fig. 2 / Extended Data Fig. 2–3
17
3,000 个模拟 CSV（10 种结构）的检出率 (%)
exact-match：位置 + 内部 subcomponents 全部正确
89%
  CSV 被完整解析
超过第二名的两倍以上 —— 其余 caller 多数只能找回部分简单成分
HG002 简单 SV 基准（vs Sniffles / SVIM / pbsv / cuteSV）
HiFi F-score 0.83 – 0.90 · ONT F-score 0.76 – 0.92（5×–47× 覆盖度），与主流 caller 相当或更优
为什么能领先
传统 caller 把 CSV 拆成孤立简单成分、在合并与过滤中丢失；SVision 在 image/graph 层面保持事件完整性
注：区域匹配 = 断点区间重叠即算命中；精确匹配 = 内部成分类型与位置均需正确

## 第 18 页
PART I · SVISION / 结果 ②
真实数据：找回被漏掉 / 误判的复杂事件
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Fig. 1d–e / Fig. 2
18
NA12878
18
个此前短读报道的复杂区被复核确认为 CSV
涉及 6 种独特结构，含 1 个此前无法分类的新结构；SVision 对全部 18 个事件正确解析了内部结构
HG00733
80
个高质量 CSV · 25 种结构 · 20 种全新
novel 结构占事件半数；19/80 与基因重叠，含一个被 PAV 误报为 1,737bp 插入的复杂重复
三级验证手段
graph alignment
与已知结构 graph 对齐比较
assembly / contig 重构
用 HiFi 分型组装独立重建事件区域
PCR + Sanger
实验验证断点连接
解读：
在一个已被短读深度研究过的样本里仍能确认新结构 —— 说明 CSV 的“暗物质”主要不是不存在，而是缺少能看见它们的表示

## 第 19 页
PART I · SVISION / 小结
SVision：贡献与局限
Lin & Ye et al. Nature Methods 19, 1232–1238 (2022) · doi:10.1038/s41592-022-01609-w · Discussion
19
三个问题 → 三个解法
比对太复杂  
→  
sequence-to-image 表示
重复序列干扰  
→  
REF-to-REF 背景相减
CSV 组合爆炸  
→  
基本成分 + graph 组合
一句话定位
以 segment 级比对几何为中间表示、CNN 负责局部识别、graph 完成事件表达的 long-read 复杂 SV 框架
局限（作者自述 + 我们的补充）
强依赖上游结构化算法
k-mer 重比对 / one-variant 分割 / SOI 提取任何一步出错，CNN 无法挽回 —— 作者也指出未来需要 unsupervised 方法优化
仍是五类先验词表
解决的是「组合不必预定义」，不是「完全摆脱结构先验」
局部事件框架
不面向跨远距离 locus / 多染色体的大尺度重排重建
重复区仍有残留
HG00733 分析仍需排除低 MAPQ、着丝粒、gap、STR/VNTR 区域

## 第 20 页
II
PART II
SVision-pro
Wang H., Lin J., Ye K. et al. · Nature Biotechnology · 2025
把 case 与 control 的结构证据和支持覆盖编码进同一张比较图像
一个分割网络同时完成成分识别、断点定位与跨样本等位基因频率比较
本部分内容
动机与现有路线
M/V/I 符号化
比较图像与 ACT
Lite-U-Net 分割
四类差异
结果：trio / somatic
小结与局限

## 第 21 页
PART II · SVISION-PRO
任务升级：从「这个样本有什么」到「两个样本差在哪」
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7
21
Fig. 1 | SVision-pro overview（论文原图）
目标场景
trio de novo SV（子有亲无）与肿瘤–配对正常 somatic SV，同时输出比较结论与基因型
根本改变 ①
中间表示：不再依赖单 read 的 VAR–REF 去噪图像，而是把两组样本的比对结构与覆盖证据共同编码成一张比较图像
根本改变 ②
学习任务：从 SOI 分类 + graph 重建，改为像素级实例分割 —— 类型、断点跨度、AF 在同一个 mask 中输出
不是
简单地给 SVision 加一个 normal 样本 —— 候选发现、表示、模型、输出全部重新设计

## 第 22 页
PART II · SVISION-PRO / 动机
现有两条路线为何不够
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Introduction
22
路线 A · Callset merging（如 Jasmine 合并）
case 单独
call → VCF
control 单独
call → VCF
merge / compare
→ 差异
✗ 
漏检不可恢复：父亲因覆盖不足漏检杂合 DEL → 合并后误判 de novo
✗ 
不同 caller 断点 / 类型 / 基因型表示不一致 → 重叠记录与矛盾
路线 B · Read-inference（如 nanomonsv）
直接比较 case / control 比对证据
预设信号 / 推断规则 → somatic SV
✗ 
规则面向特定信号：简单 DEL/INS 自然，CSV 需为每种结构写专门模型
✗ 
未定义组合出现时，要么漏检要么误判 —— 与 CSV 的组合本性冲突
SVision-pro 的第三条路：
把比较做进输入表示 —— case 与 control 的结构和证据从第一阶段就同图；再让一个分割网络统一处理「识别 + 定位 + 频率 + 比较」，不依赖事后 VCF 合并，也不为结构类型写规则

## 第 23 页
PART II · SVISION-PRO / STEP 1
候选位点发现：M / V / I 符号序列 + 聚类
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Extended Data Fig. 1
23
Extended Data Fig. 1 | 符号化与候选发现（论文原图）
符号
含义
来源
M
正向比对片段
primary / supplementary
V
反向比对片段
反向 split alignment
I
read 中额外序列
CIGAR 插入 + split 间未比对序列
每个符号携带：参考/ read 坐标区间 · 子序列长度 · read 名，按 read 顺序排列
过滤纯 M 的 正常 read
异常符号序列 迭代聚类
≥10 条 read 支持 (默认)
candidate SV locus
关键设计：候选发现与类型解释分离
候选只要「异常模式成簇」即可成立，不需要先符合任何完整 SV 类型 —— model-free 指的是这一步；后续仍有 M/V/I 与训练好的网络作为先验

## 第 24 页
PART II · SVISION-PRO / STEP 2a
结构素描：符号序列 → 二维相似图像
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Extended Data Fig. 2
24
画什么
M / V / 可确定参考来源的 I → 图中的比对线段；未比对的 I → gap；相邻块的 reference gap 一并编码
坐标
X = reference，Y = read（与 SVision 的 VAR–REF 图像同构，但直接由符号序列生成）
原则
不同类型 SV 不强行转成同一种信号，而是用与其坐标特性匹配的图像表达
结构信号的形态（X = reference，Y = read）
正常 / 共线
↘ 对角线
DEL
X 轴方向 gap
INS
Y 轴方向 gap
INV
↗ 反向线段
tDUP
平行线
invDUP
反向平行线

## 第 25 页
PART II · SVISION-PRO / STEP 2b
内容渲染：ACT 增强覆盖轨道
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Extended Data Fig. 3
25
Extended Data Fig. 3 | ACT 构建（论文原图）
普通 coverage track
每个参考位置计读数 —— 只知「多少条 read 覆盖」，不知这些 read 以什么比对关系支持
ACT 的增强
按 mapping condition 分别计数：forward / reversed / duplicated / reverse-duplicated 四种条件
RGB 三通道
以正向匹配颜色为基准（R150 G200 B250），通过调整 G、B 通道标记反向与重复；同时反向且重复则同时调整
重复匹配判定
不是靠覆盖度猜测 —— 检查同一条 read 内的 alignment 是否被其它 alignment 包含
ACT 同时提供两类信息
支持强度（局部有多少 reads 给出证据）+ 支持性质（正常 / 反向 / 重复 / 反向重复中的哪一种）—— 复杂结构判断两者缺一不可

## 第 26 页
PART II · SVISION-PRO / STEP 2c
比较图像：case 与 control 同图 + INS 的特殊轨道
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Fig. 1b / Methods
26
control · ACT（上轨道）
参考坐标 →
结构
线段
case · ACT（下轨道）
橙色 = 反向 / 重复匹配条件（示意）
同一张图内：候选区结构关系 + case 证据 + control 证据 + 两样本差异 —— 比较无需事后合并 VCF
为什么 INS 要特殊处理
插入序列只存在于 read 中、没有参考坐标 —— 参考方向的 coverage 无法表达插入序列本身的支持
做法
▪ 
在插入引起的垂直 gap 两侧开辟空白轨道
▪ 
对插入序列相关 reads 做 read-level 计数，分别生成 case / control 的垂直 ACT
▪ 
insertion-associated inversion 场景同时使用 read 级 + reference 级计数
设计原则：按坐标特性选择表达方式，而非一刀切

## 第 27 页
PART II · SVISION-PRO / 表示
图像尺寸 = 等位基因频率的可表示精度
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Methods / Extended Data Fig. 3
27
图像尺寸 (px)
ACT 轨道高度 (px)
理论 AF 分辨率
256 × 256
25
0.04
512 × 512
50
0.02
1024 × 1024
100
0.01
轨道越高，低频信号占据的像素越多
25 px
AF 0.01 不足 1 像素
50 px
100 px
AF 0.01 ≈ 1 像素
橙色带 = 低频 SV 证据高度（示意）
两点注意
① 图像尺寸不只是计算参数，直接决定低频 somatic SV 的可表示性；② 0.01 不是绝对检测下限 —— 实际能力还受测序深度、比对质量与支持证据制约
与 SVision 的对比
SVision 的图像解释「一个样本中的局部结构」；SVision-pro 的图像让两个样本的证据在同一坐标系下直接对照 —— 跨样本比较从输入端就被纳入模型

## 第 28 页
PART II · SVISION-PRO / STEP 3
Lite-U-Net 实例分割：一个 mask 同时回答四个问题
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Fig. 1 / Extended Data Fig. 4
28
control 轨道
DEL
INV
case 轨道
DUP
DEL
INV
水平跨度 = 断点区间
垂直跨度 = AF
为什么选实例分割
▪ 
跨样本比较涉及识别 / 定位 / 比结构 / 比 AF / 多成分五件事
▪ 
多个独立分类器需要额外设计连接方式；分割网络在同一张图上一次输出全部
预测类别（7 类）
DEL
INS
INV
DUP
invDUP
另含 REF（与参考一致）与 Background 两类
仍然只学基本成分
网络不学 “DEL+INV+DUP” 这类完整组合 —— 复杂事件由识别出的成分按 read 顺序组合得到，与 SVision 一脉相承

## 第 29 页
PART II · SVISION-PRO / 训练
训练数据、超参与模型选型
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Supplementary Note 1 / Extended Data Fig. 1c–d
29
训练数据（VISOR 模拟）
▪ 
五类基本 SV × 1,000 个不重叠事件 = 5,000 个 SSV
▪ 
DUP / invDUP 各含 tandem 与 dispersed 两式、各占一半
▪ 
标签来自已知类型 / 长度 / 基因型，而非人工枚举复杂组合
训练设置
▪ 
Lite-U-Net 编码器–解码器，解码端结合高分辨率特征图以保留断点信息
▪ 
batch 2 · lr 1e-4 · Adam · Cross-Entropy + Dice Loss
▪ 
early stopping：验证准确率连续 15 epoch 稳定（容差 0.001）
五个模型同台比较（mini-Unet / Lite-Unet / Unet / FCN / DeepLabV3）
选型三因子
▪ 
验证准确率 · 参数量 · 可解释性
▪ 
mini-Unet 在 256px 表现好，但 1024px 验证精度跌至 91%
▪ 
Lite-Unet（约 610 KB）三种尺寸下均约 99% —— 大模型无抵消开销的增益
可解释性不是可选项
Grad-CAM 与 Feature Ablation 归因图显示：模型预测某成分时关注的像素区域与该 SV 成分一致 —— 证据可视化让生物学审阅成为可能

## 第 30 页
PART II · SVISION-PRO / STEP 4
跨样本比较：三问 → 四类差异 → 基因型
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Extended Data Fig. 4
30
对 case / control 的 mask 逐一比较
成分类型一致？
断点跨度一致？
等位基因频率一致？
Germline
control 存在相同成分，断点与 AF 一致
两样本表现一致 → 遗传自亲本
New component
control 中不存在该成分
case 特有 → de novo / somatic 候选
New breakpoint
control 有同类成分，断点跨度不同
结构等位发生变化
New allele
成分存在，但 AF 不同
等位基因频率改变（≠新序列/新机制）
trio 判定：
child vs father 与 child vs mother 两次比较均为 New component → de novo；输出 0/0 · 0/1 · 1/1 基因型
Extended Data Fig. 4 | mask → 差异 → 基因型（论文原图）

## 第 31 页
PART II · SVISION-PRO / 结果
结果：成分识别、孟德尔一致性与低频 somatic
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Fig. 2 / Extended Data Fig. 6–10
31
模拟亚克隆肿瘤基因组 · somatic F1-score
领先 somatic-capable 的 Sniffles2 与 nanomonsv 0.03 – 0.45；AF 低至 0.01 仍可检出
96–98%
  CSV 成分识别准确率
较上一代 SVision 平均提升 15 个百分点
trio 孟德尔一致性
HiFi 97.3–98.4%（逐对比较）→ one-to-N 模式 98.4–99.3%（HiFi）/ 96.8–98.8%（ONT），均居首
HCC1395 肿瘤–正常细胞系
对已发表 somatic 位点的召回显著领先：Sniffles2 66–81%、nanomonsv 仅 6–29%
结果支撑的设计主张
跨样本检测 + 结构识别 + 基因分型整合于同一比较式图像分割框架 —— 而非三个模块的缝合

## 第 32 页
PART II · SVISION-PRO / 小结
SVision-pro：贡献与局限
Wang, Lin & Ye et al. Nature Biotechnology 43, 181–185 (2025) · doi:10.1038/s41587-024-02190-7 · Discussion / Data availability
32
四点贡献
✓ 
比较进入输入表示：case/control 证据从第一阶段同图，无需事后 VCF 合并
✓ 
组合式分割：不枚举复杂类型，识别基本成分后按 read 顺序组合
✓ 
检测 + 基因分型一体：类型 / 断点跨度 / AF 同一 mask 输出
✓ 
轻量且可解释：610 KB 模型 + Grad-CAM 归因
局限
依赖 BAM 表示质量
图像模型能解释 alignment，却无法恢复比对已丢失的信息；重复区错误定位会传导
低频受双重约束
图像分辨率 + 测序证据；肿瘤 AF 未做纯度 / 拷贝数 / 亚克隆模型校正，≠ 克隆比例
未知基本成分仍难
五类词表之外的全新结构可能被错误拆分或分类
非染色体级重建
输出局部比较结果，不能当全局重排图使用；群体模式当时仍依赖外部合并（Swave 论文指出）

## 第 33 页
III
PART III
Swave
Wang J., Ye K. et al. · Nature Genetics · 2026
以泛基因组图 snarl 为候选位点，从图路径提取等位序列
把 REF–ALT dotplot 压缩成投影波，用 Bi-LSTM 逐段识别基本成分
结构分类、单倍型基因分型、群体等位频率在图上统一完成
本部分内容
动机：群体水平困境
图构建与等位提取
三类 dotplot
投影波
波形语义
Bi-LSTM
结果与局限

## 第 34 页
PART III · SWAVE
总体框架：图负责等位，波形负责结构
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6
34
Fig. 1 | Swave overview：graph parse → dotplot & projection → deep learning（论文原图）
输入
参考基因组 + 多样本（可单倍型分辨）组装，Minigraph 建泛基因组图
输出
群体 SV 结构目录：每条等位路径的结构类型、携带单倍型、基因型与等位频率
三模块
① Graph：snarl 提取等位序列；② Sequence-to-image：dotplot → 投影波；③ Deep learning：Bi-LSTM 分类
职责分离
基因型来自图路径（谁携带），结构来自波形分类（是什么）—— 不从 read 覆盖度猜基因型

## 第 35 页
PART III · SWAVE / 动机
群体水平的两个老问题，图给出新答案
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Introduction
35
✗ 
PAV / SVIM-asm 多按等位序列长度差等简单模式分类
✗ 
REF vs ALT 长度差只能给净差，无法恢复内部 DUP+INV+DEL 的结构
问题① 组装级 caller 的先验太粗
✗ 
Jasmine / SURVIVOR / Truvari 合并需判断两个 call 是否同一等位
✗ 
断点偏差、表示差异、CSV 拆分不一致 → 错误合并与基因型缺失
问题② 逐样本 call + 事后合并
泛基因组图的答案：等位差异本来就在图里
S1
S4
A · B (REF)
C · D (ALT)
snarl
图把 SV 识别与基因分型直接建立在等位路径上
样本走哪条路 = 携带哪个等位；剩下的唯一问题是：这条 ALT 相对 REF 到底是什么结构 —— 这正是深度学习模块要回答的

## 第 36 页
PART III · SWAVE / MODULE ①
图构建与等位序列提取
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Methods / Extended Data Fig. 1
36
Extended Data Fig. 1 | 泛基因组图与等位路径（论文原图）
1
建图
Minigraph（-cxggs）顺序输入参考与各样本组装；面向 ≥50bp SV —— PGGB / Minigraph-Cactus 适用更小变异，非本文场景
2
回映射
Minigraph call 将输入组装重新映射到图，恢复每个样本的 traversal path
3
snarl
路径分歧处形成 snarl（局部变异子结构）；可含多节点、多条等位路径，甚至多个内部成分
4
重建序列
按路径顺序拼接 GFA 节点序列，得到完整 REF / ALT 等位序列，并记录每个 ALT 的携带样本 / 单倍型
5
基因型
两条单倍型分别定路径，按输入相位合并为 0|1 式样本基因型；群体频率 = 携带等位的单倍型数 / 总单倍型数
前提：
等位序列必须被正确组装并在图中可恢复 —— 图的表示质量是后续一切的上限

## 第 37 页
PART III · SWAVE / 设计原则
职责分离：图回答「谁」，模型回答「什么」
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Fig. 1a,c
37
图路径 · 对应关系问题
样本 / 单倍型
traversal path
等位 allele
▪ 
“哪个样本、哪条单倍型携带这段序列？”
▪ 
多等位 snarl：不同结构等位各自成路，不被压成二等位记录
▪ 
AF(等位) = 携带单倍型数 / 位点总单倍型数
深度学习 · 结构解释问题
ALT 序列
dotplot → 投影波
Bi-LSTM 分类
▪ 
“这条等位序列相对 REF 是什么 SV？”
▪ 
输出五类成分标签，再合并 / 组合成 SSV 或 CSV
▪ 
不从 read 覆盖度猜基因型 —— 组装已给出确定答案
为什么这很重要：
表示与推断分离 —— 图负责确定性强的对应关系，网络专注不确定的结构解释。两个问题各自的噪声来源、验证方式、失败模式完全不同，绑在一起只会互相污染

## 第 38 页
PART III · SWAVE / MODULE ②a
三类 dotplot：先看清，再压缩
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Methods / Extended Data Fig. 2
38
Extended Data Fig. 2 | dotplot 生成、精修与投影（论文原图）
Dotplot
坐标
用途
REF2REF
REF × REF
参考序列自身匹配背景
ALT2ALT
ALT × ALT
替代序列自身匹配背景
REF2ALT
REF × ALT
等位间结构差异信号
k-mer 匹配
较长序列建 k=30、步长 1bp 的 k-mer 索引，遍历较短序列查完全匹配；正 / 反向匹配都记录
结构骨架
识别长度 >50bp 的线性点簇作为比对骨架；REF2REF / ALT2ALT 能解释的重复匹配信号仅作背景
碱基级精修
k-mer 边界最多引入 k−1=29bp 断点偏差 —— 在匹配线终止边界做局部碱基重匹配修正，dotplot 不只是粗图像

## 第 39 页
PART III · SWAVE / MODULE ②b
投影波：把二维 dotplot 压成一维结构信号
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Fig. 1b / Methods
39
投影：固定 X 位置，统计 Y 方向的匹配点数
dotplot → 沿 X 轴投影 → 每个基因组位置一个匹配强度（波形）
双波设计
每次投影同时生成 forward / reverse 两条波 —— 保留链方向性，inversion 的关键信号
背景波
REF2REF → REF 内部重复背景；ALT2ALT → ALT 内部重复背景。无重复序列：均匀、均值≈1；重复密集：波动大、均值升高
SV 指示波
REF2ALT 投影到 X 轴；已成线的匹配点赋更高权重（默认 = 背景波均值），再与背景波对比
为什么不直接把 dotplot 给 CNN
▪ 
高拷贝重复区：一个 k-mer 在多条位置重复出现，点阵爆炸
▪ 
模型需在庞大点阵中区分 SV 引起的变化 / 重复自身的多重匹配 / 双方内部重复
▪ 
投影波只保留「每位置的匹配强度 + 方向」，信号更稳定
与 SVision / SVision-pro 的对照
SVision：VAR–REF 图像减 REF–REF 背景（图像层面相减）；
SVision-pro：双样本 ACT 轨道同图对照（跨样本层面）；
Swave：REF / ALT 各自背景波 + 指示波对比（序列层面）—— 同一思想在三种粒度上的实现

## 第 40 页
PART III · SWAVE / MODULE ②c
波形语义：五种基本成分的签名
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Fig. 1b / Methods
40
DEL 缺失
REF 有、ALT 无 → 该区域 k-mer 找不到对应，指示波相对 REF 背景局部降低
DUP 重复
ALT 含额外拷贝 → 额外匹配点，指示波局部升高
INV 倒位
序列仍在但方向相反 → 反向匹配波出现新的局部峰
INS 插入
无 REF 坐标 → 换到 Y 轴（ALT 轴）投影，与 ALT2ALT 背景对比呈局部降低
invDUP 反向重复
兼有重复增强与反向波新峰 —— 作为独立类别训练，而非普通 DUP
橙柱高于/低于青柱 = 指示波相对背景波的变化（正向 / 反向双波分别解读）；理想化示意，非论文原始数据

## 第 41 页
PART III · SWAVE / MODULE ③
Bi-LSTM：逐段分类 + 上下文
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Methods / Extended Data Fig. 3
41
Extended Data Fig. 3 | 特征元组与 Bi-LSTM（论文原图）
输入：每个基因组位置一个四元组（压缩后按区段）
span
区段跨度长度
bg
背景波均值
Δf
正向波 − 背景
Δr
反向波 − 背景
压缩
连续位置后三个特征相同 → 合并为一个区段，首特征改记跨度长度；重复区仍可能产生多个区段
为什么要上下文
单个区段的波形不足以定型；Bi-LSTM 双向读取整条序列，把分散区段归入同一 SV 类型
训练（沿用 SVision-pro 的 VISOR 方案）
▪ 
五类 SSV × 1,000（长度 ~N(500bp, 150bp)；DUP/invDUP tandem 与 dispersed 各半）
▪ 
70:30 训练/验证 · batch 128 · lr 1e-4 · 交叉熵 · Adam · early stopping 30 epoch（容差 0.001）
▪ 
第 7 个 epoch 收敛，验证集平均分类准确率 0.99*
* 模拟验证精度 ≠ 真实基因组精度；泛化取决于模拟分布对真实 SV 的覆盖

## 第 42 页
PART III · SWAVE / 输出
从逐段分类到群体结构目录
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Fig. 1a,c
42
1
逐位置分类
Bi-LSTM 输出每个区段的五类标签之一
2
合并同类
连续同类区段合并为一个成分（DEL|DEL|DEL → 一个 DEL）
3
组合 CSV
断点关系相连的不同成分按顺序组合，如 invDUP + DEL + INV
4
挂回图路径
成分结构注释到 ALT 等位，携带者与基因型来自图
5
群体频率
逐等位统计 AF，多等位 snarl 各自报告 → 群体 VCF
示例：一个三等位倒位位点
Allele 0 · REF
S1 → S4
Allele 1
INV
Allele 2
INV + 内部 DEL
三种结构等位在同一 snarl 共存、分别统计频率 —— 传统流程往往把它们拆成断点各异的多条记录或粗暴合并
与前两篇的组合方式对比
SVision：graph 统一表达事件内部结构；SVision-pro：分割成分按 read 顺序组合；Swave：波形成分按位置与断点关系组合 —— 都不枚举完整 CSV 类型

## 第 43 页
PART III · SWAVE / 结果
结果：个体检出、家系一致性到群体应用
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Fig. 2 / Extended Data Fig. 4–8
43
HG002 组装 · 简单 SV F1-score
组装级 CSV 检测 F1：Swave 0.956 vs SVision-pro 在组装数据上 0.655 —— 输入形态与设计目标决定表现
0.940
家系平均孟德尔一致性
居所有对比方法之首（vg-vcfwave 0.914）
0.075
HGSVC 基因分型缺失率
群体图路径直接定基因型的收益
334 + 574
健康人群 + GA4K 罕见病单倍型
复杂倒位多态性与潜在致病 SV 的群体分布
一句话结论
组装 + 图路径让 Swave 在结构分辨率与群体一致性上同时领先 —— 表示质量的提升比网络结构更重要

## 第 44 页
PART III · SWAVE / 局限
Swave 没有解决的问题
Wang & Ye et al. Nature Genetics 58, 664–672 (2026) · doi:10.1038/s41588-026-02538-6 · Discussion
44
上游瓶颈
组装与图质量决定上限：部分假阴性源于携带变异的组装缺少可映射到 snarl 的序列，着丝粒 / 端粒附近尤甚
窗口视野
dispersed DUP 的真实来源可能落在比对窗口之外（窗口按 ALT 长度扩展仍有限）→ 被误报为 INS —— 投影波概括不了没进 dotplot 的东西
词表边界
五类成分之外的结构（易位、全局染色体重排）无法充分表达；训练依赖模拟 SSV
压缩损失
不同二维匹配结构可能产生相近的一维波形；Bi-LSTM 能用上下文，但不保证唯一还原二维结构
Extended Data Fig. 10 | dispersed DUP 误分类为 INS 的案例（论文原图）

## 第 45 页
SYNTHESIS · 三篇对比
一张表看懂三篇论文
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
45
维度
SVision
SVision-pro
Swave
发表
Nat Methods 2022
Nat Biotechnol 2025
Nat Genet 2026
核心任务
单样本 CSV 发现与结构解析
case–control 比较 + 基因分型
群体分类 + 基因分型 + 频率
输入
长读长比对 BAM
case + control 的 BAM
群体组装 + 泛基因组图
候选发现
异常 read 提取 VAR
M/V/I 符号序列聚类
图 snarl → 等位路径
中间表示
VAR–REF 去噪图像（224²×3）
结构线段 + 双样本 ACT 轨道
三类 dotplot → 投影波
重复背景处理
REF–REF 图像相减
mapping-condition 编码 + 对照
REF/ALT 双背景波对比
深度学习
AlexNet 图像分类
Lite-U-Net 实例分割
Bi-LSTM 序列分类
基本成分
DEL INS INV DUP tDUP
DEL INS INV DUP invDUP
DEL INS INV DUP invDUP
CSV 组合
Illustrator 建 graph
分割成分按 read 顺序组合
波形区段按位置/断点组合
基因型来源
非核心目标
case/control 掩膜 + AF 对比
图路径与单倍型状态
群体频率
非目标
非目标（依赖外部合并）
核心输出
三行最值得记住：中间表示 · 重复背景处理 · CSV 组合 —— 它们的差异就是三个阶段的方法论差异

## 第 46 页
SYNTHESIS · 演化主线 ①
表示的演化：图像 → 比较图像 → 波形
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
46
SVision · read 级去噪图像
对象：一条 read 与参考的结构关系
▪ X=REF, Y=VAR，三通道编码
▪ REF–REF 相减去背景
▪ 粒度：单 read 的局部事件
SVision-pro · 双样本比较图像
对象：两个样本的结构 + 支持证据
ctl
case
▪ 结构线段居中，双 ACT 轨道同图
▪ AF 编码进垂直维度
▪ 粒度：候选区间的跨样本差异
Swave · 等位序列投影波
对象：REF/ALT 等位序列的匹配结构
▪ dotplot 投影成一维双波
▪ REF/ALT 各自背景波对照
▪ 粒度：群体可复用的等位特征
演化逻辑：
二维保真（图像）→ 引入对照（比较图像）→ 主动压缩（波形）—— 每次变化都是为了容纳新的证据维度：read → 样本对 → 群体等位

## 第 47 页
SYNTHESIS · 演化主线 ②
任务、证据与网络形态的同步演化
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
47
2022 · SVision
2025 · SVision-pro
2026 · Swave
证据源
long-read 比对（read 视角）
case + control 双 BAM（样本对视角）
群体组装 + 泛基因组图（群体视角）
核心问题
这里有什么 SV？内部结构如何？
两个样本差在哪？AF 变了吗？
谁携带？频率多少？多等位如何共存？
网络形态
CNN 分类（SOI → 类型）
U-Net 分割（mask → 类型+位置+AF）
LSTM 序列建模（波形 → 逐段类型）
先验落点
图像编码 + SOI 提取
ACT 编码 + 候选聚类
图结构 + 特征元组设计
任务形态决定网络形态：
分类（这是什么）→ 分割（在哪、多高）→ 序列建模（前后文里这是什么）—— 网络不是越新越好，而是与表示的性质匹配

## 第 48 页
SYNTHESIS · 共同设计原则
五条贯穿三部曲的方法论
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
48
① 组合式表示
复杂事件 = 有限基本成分 × 结构关系
泛化来自组合而非枚举：新 CSV 不需要新类别，三篇论文全部只学 5 类成分
② 背景建模
先问「参考本来就这样吗」
REF–REF 相减 / 双轨道对照 / 双背景波 —— 把「正常」显式建模，结构信号才可分辨
③ 候选与解释分离
发现不必知道类型，解释不必穷举模板
M/V/I 聚类、one-variant 分割、snarl 提取都是「先把可疑处切出来」
④ 表示与推断分离
确定性归算法，不确定性归模型
Swave 最典型：图路径定携带者（确定），网络只解释结构（不确定）
⑤ 轻量 + 可解释 + 模拟器
AlexNet / 610KB U-Net / 单层 Bi-LSTM
VISOR 模拟器造精确标签，Grad-CAM 归因可视化 —— 小模型配好表示胜过大模型配裸数据

## 第 49 页
SYNTHESIS · 开放问题
三部曲共同留下的难题
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
49
上游是硬上限
比对 / 组装 / 建图丢失的信息，图像和波形都无法恢复 —— 深度学习解释不了不存在于输入里的结构
五类词表的天花板
三篇论文的基本成分词表几乎相同（仅 tDUP → invDUP 的演化）；易位、复杂全局重排、全新基本关系仍未覆盖
局部 vs 全局
三者都是局部事件框架；染色体级 / 跨位点的衍生重排重建仍缺方法
模拟与真实的差距
训练标签几乎全部来自 VISOR 模拟 —— 长度分布、重复背景、断点精度与真实 SV 的偏差直接限制泛化
重复序列依然是共同敌人
相减、对照、背景波都显著缓解但未消除：三篇论文的结果分析都仍需排除低 MAPQ / 着丝粒 / STR 区
五个问题都指向同一方向：更好的上游表示 + 可扩展的结构词表 + 真实数据验证闭环

## 第 50 页
SYNTHESIS · 启发
对我们的研究有什么用
Lin et al. Nat Methods 2022 · Wang et al. Nat Biotechnol 2025 · Wang et al. Nat Genet 2026
50
CIGAR ≠ 真相
比对器“放弃解释”的地方（I、split gap）往往正是复杂结构的藏身处 —— 值得为它重建 segment 级对应关系，而不是直接消费比对块
先恢复对应，再谈类型
把 DEL/INV/DUP 概念建立在显式的 segment correspondence 上，类型从关系中产生，鲁棒性远高于模式匹配
背景相减可以迁移
任何“信号 vs 噪声”问题都可以先显式建模噪声（self-similarity / 对照样本 / 背景波），再看残差
比较放进输入，不要放在后处理
SVision-pro 的教训：事后合并 VCF 无法恢复漏检；把对照证据编码进输入表示，才能让模型“看见”差异
波形 = 高效但损失信息的压缩
投影波把二维压到一维，换来稳定性与群体可复用性；用它的地方要清楚知道哪些结构会变得不可分
小团队可复用的范式
VISOR 造标签 + 轻量网络 + Grad-CAM 归因 + 模拟/真实双验证 —— 低算力下做出可发表方法论的完整路径

## 第 51 页
SUMMARY
从把 SV 变成图像，到把比较变成图像，
再到把群体变成波形
三篇论文证明了一件事：在强领域知识设计的表示之上，轻量的深度学习足以解析最复杂的结构变异 —— 表示的质量，而不是网络的规模，决定方法的上限
SVision
Lin J.*, Ye K.* et al. SVision: a deep learning approach to resolve complex structural variants. Nature Methods 19, 1232–1238 (2022)
SVision-pro
Wang H.*, Lin J.*, Ye K. et al. De novo and somatic structural variant discovery with SVision-pro. Nature Biotechnology 43, 181–185 (2025)
Swave
Wang J.*, Ye K. et al. Population-level structural variant characterization using pangenome graphs. Nature Genetics 58, 664–672 (2026)
代码：github.com/xjtu-omics
谢谢 · 欢迎讨论