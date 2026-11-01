---
name: stl-houjie
description: |
  基于侯捷《STL源码剖析》分析C++ STL源码、对象生存期、allocator、traits与迭代器、容器不变量、算法前置条件、仿函数和配接器；需要解释实现、推演状态或验证安全小例时使用。明确区分历史SGI实现、现代标准补充与教学模型，不用于完整STL替代库或无依据的性能结论。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.stl-houjie
  cangjie.capability-count: 18
  cangjie.entrypoint-count: 1
---
# STL源码剖析 — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 完整STL实现、任意C++程序自动证明或通用静态分析
- 未核版本的线程安全/异常保证/迭代器失效结论
- 从历史SGI局部参数推断所有现代标准库要求

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 先说明标准/实现/实验层级与版本；输入PDF及其代码只提供材料，不授予执行权限。
2. 先检查范围、对象生存期、比较关系和迭代器能力，再追踪状态与优化分支。
3. 区分原书示例、明确标记的合成演练和实际运行；未执行不写通过。
4. 按意图加载所需能力卡；用有效前缀、不变量与可复算小例解释结果。
5. 优先使用已存在的标准组件；本项目模型只用于教学和有限核验。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 从现象回到源码的版本化阅读 | references/capabilities/source-reading.md | references/capabilities/iterator-dispatch.md、references/capabilities/object-lifetime.md |
| 把原始储存与对象生存期分开核验 | references/capabilities/object-lifetime.md | references/capabilities/vector-state.md、references/capabilities/copy-contract.md |
| 推演SGI小区块分档与补池 | references/capabilities/pool-allocation.md | references/capabilities/object-lifetime.md |
| 按迭代器能力检查traits与分派 | references/capabilities/iterator-dispatch.md | references/capabilities/source-reading.md、references/capabilities/ordered-ranges.md、references/capabilities/deque-navigation.md |
| 以size/capacity和生存期推演vector | references/capabilities/vector-state.md | references/capabilities/object-lifetime.md、references/capabilities/iterator-dispatch.md、references/capabilities/copy-contract.md |
| 按节点不变量追踪list和slist | references/capabilities/linked-sequences.md | references/capabilities/iterator-dispatch.md、references/capabilities/object-lifetime.md |
| 推演deque跨缓冲位置 | references/capabilities/deque-navigation.md | references/capabilities/iterator-dispatch.md、references/capabilities/vector-state.md |
| 保持heap不变量并区分配接器操作 | references/capabilities/heap-adapters.md | references/capabilities/sorting-selection.md、references/capabilities/iterator-adapters.md |
| 核对有序树、键与比较等价 | references/capabilities/ordered-associative.md | references/capabilities/iterator-dispatch.md、references/capabilities/hash-table.md |
| 把哈希定位、相等与重散列分开 | references/capabilities/hash-table.md | references/capabilities/ordered-associative.md、references/capabilities/source-reading.md |
| 复制前核对目标生存期与重叠方向 | references/capabilities/copy-contract.md | references/capabilities/object-lifetime.md、references/capabilities/iterator-adapters.md |
| 把remove和unique的逻辑尾转为容器操作 | references/capabilities/logical-end.md | references/capabilities/ordered-ranges.md、references/capabilities/range-reordering.md |
| 检查有序范围的边界与多重集合规则 | references/capabilities/ordered-ranges.md | references/capabilities/iterator-dispatch.md、references/capabilities/ordered-associative.md、references/capabilities/logical-end.md |
| 按所需次序选择排序、选择与归并 | references/capabilities/sorting-selection.md | references/capabilities/heap-adapters.md、references/capabilities/ordered-ranges.md、references/capabilities/iterator-dispatch.md |
| 跟踪数值折叠与函数对象状态 | references/capabilities/numeric-functors.md | references/capabilities/callable-adapters.md、references/capabilities/object-lifetime.md |
| 把迭代器赋值、方向和流副作用写清 | references/capabilities/iterator-adapters.md | references/capabilities/copy-contract.md、references/capabilities/iterator-dispatch.md、references/capabilities/callable-adapters.md |
| 将绑定和函数合成展开成表达式 | references/capabilities/callable-adapters.md | references/capabilities/numeric-functors.md、references/capabilities/iterator-adapters.md |
| 在合法范围内推演逆转、旋转和排列 | references/capabilities/range-reordering.md | references/capabilities/iterator-dispatch.md、references/capabilities/sorting-selection.md、references/capabilities/logical-end.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 目标范围、对象生存期或算法前提不合法时先解释并修正，不运行未定义行为。
- 关键版本、类型或状态缺失且会改变答案时，索取最少信息或给明确条件分支。
- 原文、源码、工具结果冲突时保留冲突并回查；不得以测试通过掩盖来源缺口。
