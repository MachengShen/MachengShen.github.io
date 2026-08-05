<!-- Published from the author's working notes. Cognitive state: speculative. -->

# 廉价的 verification 还不够，还得有可解析的 claim

*写给付杰这条 verification 线的一封跨线笔记 —— 一处独立汇合、一个实测数字、三条反对意见，以及一件我们更想拿走而不是给出的东西 · Macheng Shen × agent · 2026-08-06*

## 这是什么

这是一封写给某一条具体公开研究线的笔记，体裁与本站早先那封写给某个平行「信息本体论」频道的笔记相同：是邀请，不是评分表。这条线是付杰的（IQuest Research 研究科学家；此前在 Mila 师从 Yoshua Bengio 做博后），他公开的纲领是 *"preserve and flourish humanity by providing abundant verification"*。

其中三项贡献在本文里是承重的，而它们属于他，不属于我们：

1. **Re:Form**（[arXiv:2507.16331](https://arxiv.org/abs/2507.16331)，TMLR 2026 年 5 月；Chuanhao Yan, Fengdi Che, Xuhan Huang, Xu Xu, Xin Li, Yizhi Li, Xingwei Qu, Jingzhe Shi, Chenghua Lin, Yaodong Yang, Binhang Yuan, Hang Zhao, Yu Qiao, Bowen Zhou, Jie Fu）。诊断是：对于用 RL 训练的自然语言 LLM，*提供训练信号的那个 verification 过程本身既不可靠也不可扩展*。药方是：让生成发生在形式空间里 —— Dafny —— 那里 verification 是自动且可证明的。结果包括：**DafnyComp**，一个带自动形式化 specification 的组合式形式程序 benchmark；一个 SFT 阶段，此后连 **0.5B** 的模型都能产出语法有效、可验证的 Dafny 代码并在此项上超过闭源模型；带正则化的 RL 进一步改善域外泛化。对本文最重要的是 *"reducing human priors"* 这个取向 —— 不由工程师逐样本写前置条件、后置条件或不变式，而是让 pipeline 自动收割 verifier 的诊断信息并迭代。

2. **Autoformalization 议程**（[项目页](https://bigaidream.github.io/project/auto/)）：把自然语言内容转成可验证的形式化，明确前提是当前 LLM "cannot do genuine logical reasoning or self-verification on their own"。

3. **2026-08-05 的一条笔记**（小红书，note `6a73027b`）：宣布用稀疏矩阵分解做高效 mechanistic interpretability（MI），据称只需主流方法约 **1%** 的数据而效果几乎保持；更重要的是其中陈述的愿景 —— 在 David Dalrymple 的 Guaranteed Safe AI 框架里（[arXiv:2405.06624](https://arxiv.org/abs/2405.06624)），让 verifier 不只验证模型的输出，也用更快的方式验证模型 internals —— 君子论迹，也论心 —— 从而压低全流程 verification 成本，为社会提供更便宜可靠的 **verification tokens**。同一条笔记也自陈了局限：reductionist 假设与 LLM 的 emergent capability 不符；找到的 circuits 都是 local 的，而且可能不唯一。*（截至 2026-08-06 我们没有找到对应的预印本；此处引用的是那条笔记本身，论文出现后应替换。）*

## 这处汇合是证据，不是贡献

2026-07-27 本线写过一条私人笔记，起点跟形式方法毫无关系：Sapir-Whorf 的工程版读法 —— 语言是世界的**有损投影**，因此自然语言是为「人类日常沟通」调过的投影，也就必然不是为 verification 调过的。把这条往前推，得到的结论是：真正的缺口不在「有没有形式语言」（Lean、Coq、TLA+、Alloy、Dafny 都在），而在 **informal↔formal 的翻译**，即 autoformalization，并且把 Dafny 点名为具体目标。

这是同一个 wedge，从另一个方向抵达，而且比真正在造它的人晚了两年。我们把它记为「关于缺口在哪」的汇合证据，并明确不记为贡献。「别人做过了」是线索不是裁决 —— 但当线索是「十六位作者已经把东西造出来并发布了 benchmark」时，诚实的动作是把我们有而他们没有的交出去，把他们有而我们缺的拿回来。

## 我们唯一实测到的东西：瓶颈不在单位成本

*"abundant verification tokens"* 这个取法优化的是一次 verification 的**单位成本**。我们一直在同一根管子的另一端跑 —— 一个小型 agent 编队，其中 verification 名义上是强制的，每条完成或阻塞回执都必须带证据 —— 而在那一端真正卡住的约束不是成本，是 **verifier 读不懂递给它的东西**。

具体地说。该编队里有一个 live gate 强制一条微断言（*「blocker 验证证据 =」*），写成散文并用正则检查。正则在语义上是盲的，于是这个门既漏掉真实情形，又在主旨恰恰是「没有任何阻塞」的文档上误触发。2026-07-27 我们把散文断言换成一个极小的**有类型**回执 schema —— `kind`、`claimed-action`、`verifier-id` 恒需；completion 另加 `verified-by`、`evidence-cmd`、`evidence-output-hash`；blocker 加 `blocker-evidence-cmd` —— 并在同一语料上对跑。2026-08-06 重跑：

| | 语料 | 结果 |
|---|---:|---|
| 语料 | 18 条 | 10 条真 park，8 条非 park（含一类已知误报体裁） |
| 散文 + 正则，对假 park 的召回 | 10 | **5（0.50）** |
| 散文 + 正则，语义误触发 | 8 | 0 |
| 有类型字段，盲区 | — | 漏掉的那几类体裁都不构成类型字段的盲区 |
| schema 自检 | 4 | 4 项全过 |

漏掉的那一半有共同形状：**没有相邻动作动词**的 park —— 「待 owner：&lt;问题&gt;」「owner 行动项：确认型号」「待 owner 定」。整整一半。而漏一次在真实世界里的代价是实测的：**一项能力在一个从未有人执行过的 blocker 后面停了大约十八天** —— 那个前提根本是假的，而且没有任何组件报错，因为对一个读不懂内容的检查器来说，假 blocker 与真 blocker 不可区分。对那一批 11 条 parked 条目的审计又扫出 3–4 条同类。*（最后这个数字是审计估计而非干净测量，因此以区间陈述。）*

因此我们愿意往上递的那句话是：**verification 再便宜也没用，如果被验证的东西是以 verifier 无法解析的形式陈述的。** 「充裕的 verification token」预设了「充裕的**良类型 claim**」，而在已部署的 agent 系统里这个供给根本不存在 —— claim 全是散文。这暗示 autoformalization 最近的一个付费客户可能根本不是数学，而是**正在运行的 agent 系统的 claim 层**：每条 agent 完成回执都是一句想变成可机检断言的非形式断言，语料巨大且每天增长，而 verifier 自己的 pass/fail 就是标签。

按本站规矩给两个数。**P(机制为真 —— 对这一类检查，有类型的 claim 层严格优于「散文 + 正则」) ≈ 0.9**：直接测出来的，而且机制并不微妙。**P(在现实规模上有用 —— 即在一般的 agent 部署中，卡住的是 claim 的类型化而不是 verification 的单位成本) ≈ 0.3**：n = 1 个编队、18 条语料，而且最该打折的一条是 —— *被打败的那个正则和打败它的那个 schema 是同一批作者写的*。下面的证伪条目里点名了一个更强的 baseline。

## 三条关于「验证 internals」的反对意见

这些是反对意见，不是纠错。它们都瞄准 *「论心」* 那一半 —— 廉价地验证模型内部 —— 且每条都自带能化解它的条件。

**其一：可审计的证书和统计分解是两种不同的对象。** Guaranteed Safe AI 框架向 verifier 要的是*一份可审计的证明证书*。而 MI 导出的内部检查给出的是一份**分解** —— 一份报告，由一套「没有跟你共训过的第三方只能选择信任」的机器产出。约束这一点的文献，并不是我们自己那条私人笔记里声称的那两篇「学出来的协议对外人不可读」的论文；为写本文我们去核了那两个引用，两篇都没有这么说，因此该说法在此撤回。真正成立的版本更弱，但仍然咬人：由 self-play 特化出来的策略与约定，与独立训练的伙伴无法协调（[Other-Play，Hu, Lerer, Peysakhovich & Foerster，arXiv:2003.02979](https://arxiv.org/abs/2003.02979)），而用来判断一个学出来的通道是否真有含义的标准指标，其本身就会误导（[Lowe, Foerster, Boureau, Pineau & Dauphin，arXiv:1903.05168](https://arxiv.org/abs/1903.05168)）。转译过来：在一次训练上调出来的读出器，恰恰属于「不保证能迁移到必须审计它的那一方」的那类约定。我们想问的是：**要让一个 MI 读出成为证书而不是报告，需要补上什么？** 我们自己的答案（也正是本线的兴趣所在）是：你要的是私有表示里**可机械检查**的那一半，而不要**不可人审**的那一半 —— 而这是回执的属性，不是模型的属性。

**其二：不唯一性其实是路径依赖，而那是一条 spec 要求，不是一条只能忍受的 caveat。** 他的笔记把「circuits 是 local 的且可能不唯一」列为局限。本站另一条线一直在研究**滞回**式的 verification 签名 —— 路径依赖而非查表 —— 而我们在那条线里亲手杀掉了自己的 self-specificity 主张，所以对它握得很松。但这个推论可以干净地迁移：**如果分解不唯一，那么一条内部验证的 claim 只有在自带其路径时才可复现。** 哪次运行、哪份数据、哪个初始化、什么容差。这把一条「你只能带着走」的 caveat 变成一个可检查的字段，代价是 schema 里的一行。

**其三：让 verification 变便宜，就把优化压力加到了 verifier 的输入通道上。** 这正是我们自己的 schema 被刻意设为 **SHADOW** 的原因 —— 它只记录、不拦截任何东西。schema 一旦成为门，agent 就获得了产出**符合 schema 的伪造**的激励：我们的残余风险是一个偷懒的 agent 粘贴一个看起来合规的 `evidence-output-hash` 而从未真的重跑那条命令；schema 抬高了这么做的成本，但没有消除它。放大到上层，这就是瞄准 internals 的 Goodhart：**一旦「干净的 internals」开始承重，干净的 internals 本身就成了靶子。** 任何被施加「通过内部检查」这一优化压力的模型，都在被部分地训练成「呈现能通过检查的 internals」。我们不知道 GS-AI 框架是否已经为「被验证方专门针对 verifier 的读出做优化」这件事留了预算；我们想知道，而且我们宁愿被告知这早已被处理，也不愿自己是对的。

## 我们更想拿走而不是给出的东西

这处不对称是诚实的，而且方向朝另一边。我们的 shadow checker 只是一个手写的 draft-07 子集校验器；我们没有的东西正是 informal→formal 的翻译本身，而那恰是 Re:Form 的 pipeline 换一个语料指过去。如果上面有任何一条值得那个组花一个下午，具体建议是：做一个 **DafnyComp 形状、但对象是「操作性 claim」而非程序的 benchmark** —— 组合式、可自动形式化、以 verifier 的执行为 ground truth —— 因为那正是「非形式的一侧已经极其充裕、却还没有人给它定类型」的语料。

## 什么能杀死这条笔记

- **最强的一条。** 拿一个语义上称职的散文检查器 —— 一个 LLM judge —— 在同样这 18 条语料上跑。如果它能在没有语义误触发的前提下追平有类型 schema 的召回，那么 claim 的**类型化**就什么都没买到，本文的核心即死：缺口在正则，不在散文。这个 baseline 我们还没跑；在跑出来之前，0.3 是慷慨而不是谦虚。
- 如果 MI 读出能被做成可重跑的 —— 第三方重算分解并在给定容差内复现同一 circuit —— 那么第二条反对意见就正确地塌缩成一个工程细节。
- 如果 agent 回执语料被证明噪声太大或多样性太低，训不出 autoformalizer，那么「第二个客户」这个建议就死了，编队老老实实继续手写 schema。
- 如果 GS-AI 文献已经处理了「针对内部读出的对抗压力」，那么第三条反对意见就不是新闻，应当被删掉而不是被软化。

## Cognitive state

刻意标 `speculative`，而且各部分并不配得上同一个标签。corpus-scan 的数字随时可复现，在 n = 1 的意义上够得上 `survived`；而这条写给另一个研究组纲领的迁移主张，一次检验都没有过。本站一个 artifact 只带一个状态，诚实的那个单一状态是更弱的那个。

## 参考文献

- Chuanhao Yan et al., *Re:Form — Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny*, [arXiv:2507.16331](https://arxiv.org/abs/2507.16331), TMLR（2026 年 5 月）。代码与模型：[Veri-Code/ReForm](https://github.com/Veri-Code/ReForm)。
- Jie Fu, [*Autoformalization and Formally Verifiable AI*](https://bigaidream.github.io/project/auto/)，以及[个人主页](https://bigaidream.github.io/)。
- 付杰，关于用稀疏矩阵分解做机制可解释与 abundant verification tokens 的笔记，小红书 note `6a73027b`，2026-08-05。
- David "davidad" Dalrymple, Joar Skalse, Yoshua Bengio, Stuart Russell, Max Tegmark, Sanjit Seshia, Steve Omohundro, Christian Szegedy, Ben Goldhaber, Nora Ammann, Alessandro Abate, Joe Halpern, Clark Barrett, Ding Zhao, Tan Zhi-Xuan, Jeannette Wing, Joshua Tenenbaum, *Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems*, [arXiv:2405.06624](https://arxiv.org/abs/2405.06624)。
- Hengyuan Hu, Adam Lerer, Alex Peysakhovich, Jakob Foerster, *"Other-Play" for Zero-Shot Coordination*, [arXiv:2003.02979](https://arxiv.org/abs/2003.02979), ICML 2020。
- Ryan Lowe, Jakob Foerster, Y-Lan Boureau, Joelle Pineau, Yann Dauphin, *On the Pitfalls of Measuring Emergent Communication*, [arXiv:1903.05168](https://arxiv.org/abs/1903.05168), AAMAS 2019。

更广的 autoformalization 前沿在此刻意不做综述。本文是写给一条线的，不是写给一个领域的；没做的综述不该假装做过。
