# 按迭代器能力检查traits与分派

## R — 原文锚点

> 最常用到的迭代器相应型别有五种

出处：§3.3–3.4，PDF121–129。

> 但是可用并不代表最佳！

出处：§3.4.5，PDF129–136。

## I — 方法解释

迭代器屏蔽了容器布局，却仍须向算法提供所指类型、距离类型与能力。traits统一类的嵌套型别和原生指针的特化；tag dispatch利用这些型别在编译期选分支。Input与Output不是一根可互换链，随机存取也不等于连续储存。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§3.1，PDF116–117，3find.cpp）：

相同数组被用来建立vector、list和deque。
三次find以各容器的begin/end为范围，分别查找4、6、8。
找到时解引用返回迭代器；未找到时用对应容器的end判断。

原书报告：原书报告4 found、6 found、8 not found。

证据边界：OCR正文及代码输出可辨；数组完整初值未据损坏OCR复刻。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

iterator_traits、五种关联型别、tag dispatch、advance/distance、list能否sort或deque是否连续。

以本卡输出契约为准；遇到相邻任务再补读source-reading；ordered-ranges；deque-navigation，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：迭代器定义或类别、算法需要的操作和有效区间。
1. 列value_type、difference_type、pointer、reference、iterator_category；指针特化检查const T*的value_type仍为T而reference为const T&。
2. 逐个核对解引用、递增、重复遍历、后退、跳跃；不从容器名字猜类别。
3. 对advance/distance写出所选重载和复杂度；Input/Forward负位移、越界或跨容器距离直接拒绝。
4. 输出能力表、缺失操作、分派路径和比较次数/步数的分离说明。需要时用编译期断言验证；不依靠故意编译UB。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

书中的继承tag表示分派关系，不要求所有迭代器继承同一对象基类。现代concepts、代理引用及迭代器细节需目标标准补充。内置随机存取操作并不保证元素连续。

## 相关能力

source-reading；ordered-ranges；deque-navigation。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
