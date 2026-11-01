# 保持heap不变量并区分配接器操作

## R — 原文锚点

> stack所有元素的进出都必须符合“先进后出”的条件

出处：§4.5–4.8，PDF204–222。

> SGI STL提供的heap并未使用这一小技巧。

出处：§4.7.1–4.7.2，PDF210–217。

## I — 方法解释

heap利用数组表示树形次序，最大堆只要求父节点不小于孩子，不要求整个数组有序。push_heap修复已在末尾加入的元素，pop_heap把堆顶送到末尾并修复前缀；容器的真正增删是另一操作。priority_queue把这组操作封装起来。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§4.7.4，PDF218–219，4heap-test.cpp）：

初始序列为0 1 2 3 4 8 9 3 5；make_heap建立最大堆。
先push_back(7)，再push_heap把新末项纳入堆。
pop_heap把原最大值移到末尾，随后pop_back才真正缩短vector。
最后对剩余堆执行sort_heap。

原书报告：pop_heap后back为9；删除后sort_heap得到0 1 2 3 3 4 5 7 8。

证据边界：OCR；内部堆数组排列是该实现示例，不应作为所有实现的唯一预期。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

push_heap/pop_heap/make_heap/sort_heap、priority_queue、stack/queue底层容器与接口。

以本卡输出契约为准；遇到相邻任务再补读sorting-selection；iterator-adapters，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：序列、比较关系、现有堆区间和操作；先统一零下标，父=(i-1)//2、子=2i+1/2i+2。
1. 验证操作前所需堆前缀；push必须先有末尾新元素，pop必须非空。
2. 追踪上溯/下溯路径，每次检查父子关系；pop_heap后只把末尾排除出堆范围，尚未减少size。
3. 若需求是真正删除，再调用底层pop_back或priority_queue::pop；stack/queue仅允许各自公开接口。
4. 输出堆区间、末尾被移出的值、容器size和比较关系。heap-trace只模拟整数最大堆，不承诺标准库内部排列。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

sort_heap需要堆前提；堆顶只是相对比较关系的极值。不可把书中一基示意的子节点公式混入零基数组。配接器不暴露任意遍历接口。

## 相关能力

sorting-selection；iterator-adapters。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
