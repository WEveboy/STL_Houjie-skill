# 任务覆盖审计

分母来自阶段0的15项任务，不从通过候选倒推。覆盖指已经提供限定范围的分析能力及参考路径，不是完整STL重实现或每个重载均经证明。

| 任务 | 实际能力去向 | 输出检查 |
|---|---|---|
| T01 | source-reading | E01, E02 |
| T02 | object-lifetime | E03, E04 |
| T03 | pool-allocation | E05, E06 |
| T04 | iterator-dispatch | E07, E08 |
| T05 | vector-state | E09, E10 |
| T06 | linked-sequences | E11, E12 |
| T07 | deque-navigation | E13, E14 |
| T08 | heap-adapters | E15, E16 |
| T09 | ordered-associative | E17, E18 |
| T10 | hash-table | E19, E20 |
| T11 | copy-contract | E21, E22 |
| T12 | logical-end, ordered-ranges | E23, E24, E25, E26 |
| T13 | sorting-selection, range-reordering | E27, E28, E35, E36 |
| T14 | numeric-functors | E29, E30 |
| T15 | iterator-adapters, callable-adapters | E31, E32, E33, E34 |

重要收窄：有序树覆盖不变量、旋转与插入机制解释，不含完整删除修复证明；内存池工具只核分档，补池有条件推演，不包含线程/OOM故障注入；排序卡逐一保留不同算法后置条件，不复刻所有历史排序代码。来源不足的普遍化语句记录在needs-review.md，未进入active规则。

候选逐项处置见candidate-decisions.json；参考明确进入已发行overview/glossary或A1。三重验证、输出测试、触发路由和源页图检查相互独立。
