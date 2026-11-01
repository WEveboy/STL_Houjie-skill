# 将绑定和函数合成展开成表达式

## R — 原文锚点

> 实际调用表达式，并将 value 绑定为第二参数

出处：§8.4.2，PDF492（页图核验）。

> 内藏了一个 member object

出处：§8.1.3、8.4，PDF468–473、488–500。

## I — 方法解释

绑定先储存参数，调用时再把输入填入剩余位置；非交换运算让绑定第一或第二参数的差别显现。组合把一个调用的结果交给另一个调用，不能仅按名字猜先后。旧配接器依赖的型别约定与现代lambda写法要分开说明。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§8.1.3，PDF469–470，8compose.cpp）：

输入2 21 12 7 19 23；先把plus第二参数绑定2，再把multiplies第二参数绑定3。
compose1把它们串成f(g(v))，transform把返回值写到输出迭代器。
同一按值函数给for_each调用时，返回值被丢弃，原容器保持不变。
原书将for_each笼统称为不能更改元素，不应作为一般C++规则保存；此例不变的具体原因是参数及返回语义。

原书报告：transform输出12 69 42 27 63 75；按值for_each演示仍输出原序列。

证据边界：OCR；compose1属书中SGI扩展；历史nonmutating断言须纠正归因。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

bind1st/bind2nd/not1/compose/ptr_fun/mem_fun、绑定方向、旧仿函数迁移lambda。

以本卡输出契约为准；遇到相邻任务再补读numeric-functors；iterator-adapters，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：函数签名、捕获或绑定值、参数位置、组合结构、值/引用和成员对象。
1. 先展开为普通表达式，例如bind2nd(minus,3)对应x-3，bind1st(minus,3)对应3-x。
2. compose(f,g)逐层写成f(g(x))；not对最终谓词结果取反，而不是任意一个内部参数。
3. 检查保存的对象/引用是否仍存活以及调用const性；旧适配器不可用时给现代lambda或显式函数对象等价式。
4. 输出展开式、若干非对称输入的结果和等价现代写法；只迁移已确定的语义，不声称旧API都能在当前标准编译。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

现代lambda、std::bind或mem_fn是独立补充，不冒充原书例码。不要以乘加等可交换巧例掩盖绑定方向错误；捕获引用的生存期不能由表达式等价保证。

## 相关能力

numeric-functors；iterator-adapters。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
