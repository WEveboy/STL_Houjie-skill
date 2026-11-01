# 三重验证与晋级记录

V1：原书限定版本及可定位机制；页图抽核见audit/source-check.md。V2：先用新输入纸面推演，再由独立执行者完成代表任务。V3：固定任务检查生存期、范围、操作能力和输出口径，减少遗漏；是否提升正确率只看同题对照，不由自评得出。

候选分流计数：{"verified": 56, "reference": 84, "needs_review": 1, "rejected": 10}。数量只反映合并粒度，不表示读完全部代码或所有公式都已实证。

| 能力 | 来源候选 | V1范围 | V2代表任务 | V3可检查用途 |
|---|---|---|---|---|
| source-reading | f02, p01 | 以卡片R与B为限 | E01/E02 | 从现象回到源码的版本化阅读 |
| object-lifetime | p03, p04, f07 | 以卡片R与B为限 | E03/E04 | 把原始储存与对象生存期分开核验 |
| pool-allocation | p05, p07, f05 | 以卡片R与B为限 | E05/E06 | 推演SGI小区块分档与补池 |
| iterator-dispatch | p08, p09, p10, f08 | 以卡片R与B为限 | E07/E08 | 按迭代器能力检查traits与分派 |
| vector-state | p12, p13, f11 | 以卡片R与B为限 | E09/E10 | 以size/capacity和生存期推演vector |
| linked-sequences | f12, p14, p15 | 以卡片R与B为限 | E11/E12 | 按节点不变量追踪list和slist |
| deque-navigation | f13, p16, p17 | 以卡片R与B为限 | E13/E14 | 推演deque跨缓冲位置 |
| heap-adapters | p18, p19, p20, f16 | 以卡片R与B为限 | E15/E16 | 保持heap不变量并区分配接器操作 |
| ordered-associative | p21, p22, p23, f18 | 以卡片R与B为限 | E17/E18 | 核对有序树、键与比较等价 |
| hash-table | p25, p26, f19 | 以卡片R与B为限 | E19/E20 | 把哈希定位、相等与重散列分开 |
| copy-contract | p27, p28, f22 | 以卡片R与B为限 | E21/E22 | 复制前核对目标生存期与重叠方向 |
| logical-end | p30, f24 | 以卡片R与B为限 | E23/E24 | 把remove和unique的逻辑尾转为容器操作 |
| ordered-ranges | p29, p31, p32, f23, f26 | 以卡片R与B为限 | E25/E26 | 检查有序范围的边界与多重集合规则 |
| sorting-selection | p33, p34, p35, p36, f29, f30 | 以卡片R与B为限 | E27/E28 | 按所需次序选择排序、选择与归并 |
| numeric-functors | p37, p38, f21, f32 | 以卡片R与B为限 | E29/E30 | 跟踪数值折叠与函数对象状态 |
| iterator-adapters | p39, p40, p41, f33, f34, f35 | 以卡片R与B为限 | E31/E32 | 把迭代器赋值、方向和流副作用写清 |
| callable-adapters | p42, f36 | 以卡片R与B为限 | E33/E34 | 将绑定和函数合成展开成表达式 |
| range-reordering | f25, f27 | 以卡片R与B为限 | E35/E36 | 在合法范围内推演逆转、旋转和排列 |

五项晋级判断：18项均有独立意图、输入输出契约、可独立读取的机制、复用情境和可测任务；这些合格项仍按用户要求模仿的single工程保留内部路由，不强行为18个发现入口。知识保留与发现入口数分开判断。

本表记录知识分流；实际执行成绩见audit/eval-results.json及../docs/EVALUATION.md。不把源审阅者参与过提取的核对称为独立盲评。
