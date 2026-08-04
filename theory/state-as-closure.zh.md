<!-- Published from the author's working notes. Cognitive state: speculative. -->

# State 是什么?——从 MDP 的状态概念到"闭包"本体论

*一次讨论的整理 · Macheng × agent · 2026-07-09 · 2026-08-04 边界修订*

## 起点的问题

我们常说"信息决定未来的 reachability"。套用强化学习 / 决策论的 MDP 框架,里面需要一个 state——那这个 state 到底是什么?是时空这个大舞台,还是"所有东西互相依赖"的那张关系网?而且 state 所指的那个集合似乎一直在变,没有恒定不变的东西;可能结构层面不变,但具体表现形式一直在改变。

下面是沿这个问题挖出来的六层。论断按诚实度标注:**[定理]**(有定理级文献)/ **[框架]**(成熟理论框架)/ **[推断]**(我们的综合)/ **[韵脚]**(结构类比,不主张真值传递)。

## 一、MDP 的定义自己已经泄密:state 不是东西,是商空间

教科书说 state 要满足 Markov 性:给定 s,未来与过去条件独立。注意这句话的形状——它不是在描述世界里的某个东西,而是在提一个**条件**:凡是能"屏蔽"过去的,就配叫 state。在平稳随机过程与预测等价的设定下,computational mechanics 把这一步走完了 **[定理,有范围]**:对未来条件分布相同的历史构成 predictive causal states。最小性结论属于这个形式设定,不是“所有科学状态表示都有唯一商空间”的定理。

我们的综合 **[推断]** 是把任务相对的 state 视为:**历史空间按“对我关心的预测或控制无差别”取商得到的表示**。这是建模立场,不是普适本体论定理。这个商依赖动力学、观测接口与 telos;任何一项变化,都可能要求重做状态表示。

## 二、Mori–Zwanzig 视角:状态 = 你决定停止携带记忆的地方

在通常的算子与演化假设下,Mori–Zwanzig 形式主义给出精确的投影恒等式 **[定理,有范围]**:选定 resolved observables 与投影后,其演化可分成瞬时项、记忆项与正交动力学项。“被投影掉的自由度不会凭空消失”这个直觉保留,但初稿的“任何系统、任何变量”说得过满。

把它反过来读成一个启发式 **[推断]**:有用的近似 Markov 表示通常要靠携带足够变量、接受受控记忆核,或容忍 unresolved forcing 来“购买”。实践问题不是先验断言“世界唯一真实 state 不存在”,而是:**在给定容量、目的与误差容忍下,哪个表示足以闭合动力学?** 选投影也在选择丢弃哪些信息;weak-memory regime 有时还能给局部近似提供显式误差界。

## 三、舞台还是关系网?两个都不是原初——但关系网里藏着让 state 可能的东西

- **舞台不是原初**:全息原理一线的现代结果(Ryu–Takayanagi 的纠缠熵=最小曲面面积、Van Raamsdonk 的"解除纠缠→时空断裂"、张量网络 MERA)指向:空间连通性由纠缠结构生成,"舞台"自己是从关联结构里展开出来的 **[框架,严格数学在 AdS 内]**。所谓"时空这个 state",是物理学迄今造出的最深的一套记账商空间——极其成功,但仍是商,不是底。
- **但"一切互相依赖"如果说满了,有限 state 就根本不可能**——严格的全依赖意味着任何有限截断都漏。有限 state 之所以可行,是因为关系网**有结构**:相互作用局域、关联随距离/时间衰减、存在屏蔽面(图模型语言里的 Markov blanket)**[框架]**。一句话:关系为先,但关系有纹理;**state 是纹理允许的近似闭包**。没有屏蔽结构的宇宙里不存在 agent。

## 四、"信息决定 reachability"的严格版

随机控制里这句话有精确形体 **[框架]**:agent 随时间累积的信息是一个**滤波(filtration)**,任何 admissible policy 都必须适应于它——你不能依据你不知道的东西行动。若一个滤波包含另一个,并固定动作、风险与资源约束,粗信息策略类嵌入细信息策略类;最优值不会仅因“多知道了且允许忽略”而变差。这不等于每一个物理可达集都会严格增大。

在 POMDP 中,最优控制常可写在**信息态**上,经典形式是对潜在世界态的 belief **[框架]**。这不表示世界态无关,而是控制器只能通过自己可获得的信息行动。Empowerment(Klyubin–Polani)是动作到未来观测的信道容量:它是在给定 horizon 与 channel model 下对潜在可控影响的度量,不是可达集本身。

## 五、"集合一直变、结构不变"这个直觉的三个数学的家

1. **学习 = 重新取商**:模型变了,"无差别"的划分就变了,state 集随之重划。belief 空间的数学外壳不变,agent 实际用的坐标卡一直在换。
2. **图册,不是单一坐标系**:开放世界里任何固定 state 集都只是临时 chart;持久的是 chart 之间的**变换规则**。这个立场在科学哲学里有名字——结构实在论(structural realism):跨理论更替存活下来的是关系结构,不是对象清单。
3. **重整化群**:每个尺度有每个尺度的 state 集,谁也不是"真的";不变的是连接各层的**流**和它的不动点。

收束成一句 **[推断]**:**不变的是"闭包条件"那个方程,态集只是方程在当前(世界,接口,容量,telos)下的解**。环境、容量、目的变了,解就重算——本征方程不动,本征向量随算子变。

顺带一个我们最近在小合成系统上做的数值观察 **[实证,初步,未审计]**:把"表示"与"用该表示活出的统计"接成自洽循环(表示定投影→投影定闭合模型→闭合模型生成轨迹→轨迹统计更新表示),在拟合容量充分的区域,这个循环表现出唯一不动点与几何收敛。真正有趣的 open 区域是容量受限时,是否会并存多种不同但各自自洽的表示。**这里没有链接公开代码或结果 artifact,所以这段只是 working-note 报告,不是可独立审计的证据。**

### 2026 证据边界:workspace 还不是 closure

Anthropic 的 Jacobian-lens 实验在 Transformer 中识别出一个可报告、可调制、可灵活路由的 J-space **[外部实证]**。这纠正了“Transformer 完全没有 state”的说法:它有 activation state、computational state 与瞬时 workspace-like representational state。但 J-space 是由过完备 frame 生成、受稀疏度约束的锥之并,不是一个固定投影;现有证据发生在模型深度轴上,还没有给出跨步持续、并自主维护自身遗忘策略的变量。因此它是 access/workspace 的相邻候选坐标,还不是本文 closure 方程的解。

另一项 2026 结果提供的是约束,不是桥梁 **[从外部定理得到的推断]**。OpenAI 报告了 Connes rigidity conjecture 的反例:在该定理设定内,关联的 von Neumann algebra 不一定唯一决定底层群;同时构造出 non-sofic groups,说明不能普遍假设抽象对象都可由有限对称模型逼近。这两条定理都不关于 agent 或意识。可迁移的警告只有:算子/可观测层等价未必唯一识别底层 substrate;任何有限状态近似方案都必须明说 approximability 假设。

另一侧的边界来自 Brandner 的 weak-memory 结果:对一类定义清楚的自治线性非局域方程,记忆动力学可以得到带显式误差界的局部近似。所以“投影产生记忆”不等于“任何尺度都必须永久保留非 Markov 记账”;局部 closure 是否足够是定量 regime 问题。

## 六、真 open 的三处

1. **没有设计者时,谁来选商?** "自洽不动点"是候选答案(商由"用它活出来的统计"自我确认),但目前是数值观察+猜想,不是定理。
2. **态空间的生长没有好数学**:世界冒出新变量(新实体、新博弈)时,商空间要加维而不只是重划——continual learning 的核心 open 问题。
3. **Bootstrap 循环**:取商要统计,攒统计要先有临时的商。这个鸡生蛋结构反复出现(表示↔统计,记忆测度↔世界模型),它的不动点理论似乎还没人正面写。

## 附:一个佛学韵脚(明确标注为韵脚)

上面的结论用中观的话说就是:state 无自性,是**假名安立**的商,随缘重立。"缘起性空"对 state 这个概念的适用度,比对多数概念都字面——但这是结构上的押韵,不是论证。

## 主要文献指针

- Crutchfield & Young (1989); Shalizi & Crutchfield (2001) — causal states / computational mechanics
- Zwanzig (2001) *Nonequilibrium Statistical Mechanics*; Lin & Lu, arXiv:1908.07725 — Koopman–Mori–Zwanzig
- Brandner (2025), [*Dynamics of Microscale and Nanoscale Systems in the Weak-Memory Regime*](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.134.037101) — 非局域线性动力学的受控局部近似
- Åström (1965); Kaelbling, Littman & Cassandra (1998) — POMDP / information state
- Klyubin, Polani & Nehaniv (2005) — empowerment
- Ryu & Takayanagi, hep-th/0603001; Van Raamsdonk, arXiv:1005.3035; Swingle, arXiv:0905.1317 — 纠缠与时空
- Ladyman & Ross (2007) *Every Thing Must Go* — 结构实在论
- Pearl (1988) — Markov blanket / 图模型屏蔽
- Anthropic (2026), [*Verbalizable Representations Form a Global Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace/index.html) — 瞬时 sparse-frame workspace 候选,尚非持续自主 closure
- OpenAI (2026), [*Ten advances in mathematics and theoretical computer science*](https://openai.com/index/ten-advances-in-mathematics/) — non-sofic groups 与 Connes rigidity 反例;这里只作为不可辨识性/有限可近似性约束
- 相关纠错:[折扣信用分配是余核问题，不是闭环 holonomy](https://machengshen.github.io/theory/discounted-credit-is-a-cokernel.zh.md)
