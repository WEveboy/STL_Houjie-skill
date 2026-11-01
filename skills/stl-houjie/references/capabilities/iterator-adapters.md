# 把迭代器赋值、方向和流副作用写清

## R — 原文锚点

> 在insert iterators的operator=操作符中调用底层容器的push_front()或push_back()或insert()

出处：§8.3.1，PDF475–477。

> 对逆向迭代器取值，就是将“对应之正向迭代器”后退一格而后取值

出处：§8.3.2，PDF477–482。

## I — 方法解释

插入迭代器把赋值转成push或insert，因此copy可以让容器增长。反向迭代器保存的是正向边界，所表示元素在base前一格；流迭代器则让构造、递增或赋值关联到实际读写。相同迭代语法不代表相同副作用。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§8.1.2，PDF467–468，8iterator-adapter.cpp）：

从0 1 2 3 4 5建立deque，copy到ostream迭代器负责输出。
front_inserter追加来源项1到头部，back_inserter把3加到尾部。
找到原值5，在其前用inserter写入0 1 2，再通过反向迭代器输出。
最后把流输入通过inserter接到容器头部；输入结束由流状态决定。

原书报告：插入后序列为1 0 1 2 3 4 0 1 2 5 3；反向输出3 5 2 1 0 4 3 2 1 0 1。

证据边界：OCR；示例只向front插入单项，不把它误作多项插入保持源序的证明。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

back_inserter/front_inserter/inserter、reverse_iterator::base、istream_iterator/ostream_iterator与copy。

以本卡输出契约为准；遇到相邻任务再补读copy-contract；iterator-dispatch；callable-adapters，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：底层容器或流、源区间、期望顺序和所需配接器；先确认底层支持相应push_front/push_back/insert。
1. 输出为空或需增长时选插入迭代器，追踪operator=实际调用；front_inserter可能反转输入顺序。
2. 对有效可解引用反向迭代器r，解释*r等于*prev(r.base())；rend().base()==begin不能解引用rend或begin前位置。
3. 流输入记录初始读取和递增读取、EOF状态与单遍性质，避免复制迭代器后假定独立游标。
4. 输出真实容器变化、反向/正向位置映射或读写轨迹；用安全C++标准配接器验证。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

只reserve而没对象不能充当copy目标；反向base不是同一元素位置。不能对流迭代器做随机访问，也不能由deque随机访问推出连续地址。

## 相关能力

copy-contract；iterator-dispatch；callable-adapters。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
