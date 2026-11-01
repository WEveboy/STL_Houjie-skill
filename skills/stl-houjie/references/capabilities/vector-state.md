# 以size/capacity和生存期推演vector

## R — 原文锚点

> 一个vector的容量永远大于或等于其大小。

出处：§4.2.4，PDF155。

> 重新配置、元素移动、释放原空间

出处：§4.2.5–4.2.6，PDF156–163。

## I — 方法解释

SGI vector的start、finish、end_of_storage分别界定起点、活元素尾和储存尾。size是活元素数，capacity是可容纳数。插入分为容量足够的就地搬移和另分配储存两条路径；只有把构造、赋值、销毁与提交时点分开，才能说明异常与失效。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§4.2.5，PDF156–158，4vector-test.cpp）：

初始包含两个9；依次push_back 1、2、3、4、5。
原书记录size从2增长到7，capacity依次经历2、4、8。
随后的pop_back缩小size而保留capacity=8。
此案例展示SGI实现的历史增长策略，不是所有std::vector必须翻倍的证明。

原书报告：添加5后为9 9 1 2 3 4 5，size=7、capacity=8；三次pop后size=4、capacity=8。

证据边界：页图157已核；该页find后的if(ivite)不是可移植的未找到判定，不能照抄。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

vector扩容、三指针、reserve/resize、insert/erase/clear、引用或迭代器失效。

以本卡输出契约为准；遇到相邻任务再补读object-lifetime；iterator-dispatch；copy-contract，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：原size/capacity、内容、插入或删除位置与数量、元素类型；分析扩容倍率必须另给实现版本。
1. 检查0<=size<=capacity、位置合法；画活区和原始储存区。
2. 余量足够时区分新尾部的构造与已有活对象的赋值；余量不足时列分配、构造新序列、失败清理、销毁旧对象、释放旧储存和提交边界。
3. 输出新内容、size、容量的确定值或实现相关区间、构造/赋值/销毁步骤。标出失效范围，不解引用旧迭代器来验证。
4. SGI增长可由vector-growth模型推演；当前标准库实验只能观察本机capacity，不能要求所有库翻倍。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

reserve不增加size；clear/erase不等于释放capacity。现代异常保证依类型操作而变。地址没变也不能推出插入点后所有旧迭代器仍合法。

## 相关能力

object-lifetime；iterator-dispatch；copy-contract。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
