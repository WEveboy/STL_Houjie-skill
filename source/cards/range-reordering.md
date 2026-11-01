# 在合法范围内推演逆转、旋转和排列

## R — 原文锚点

> rotate() 可以交换两个长度不同的区间

出处：§6.7.1，PDF399–404。

> 再将 i1 之后的所有元素颠倒排列

出处：§6.7.5–6.7.6，PDF419–421。

## I — 方法解释

reverse改变整个方向，rotate交换两个相邻区段且保留各段内部次序，next_permutation按比较器定义寻找相邻字典序排列。它们都保留元素多重集，但后置条件不同，不能用排序的结果要求来评价。

## A1 — 原书示例或标明的演练

合成演练：对[1,2,3,4,5]以middle偏移2执行rotate，结果为[3,4,5,1,2]；next_permutation把[1,3,2]变为[2,1,3]；最大字典序[3,2,1]返回false并回到[1,2,3]。

以上为本项目合成演练，不冒充作者亲历或独立来源。

## A2 — 触发与近邻区分

reverse/rotate/next_permutation/prev_permutation、循环移动、字典序下一个排列与重复值。

以本卡输出契约为准；遇到相邻任务再补读iterator-dispatch；sorting-selection；logical-end，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：有效[first,last)、可选middle、比较器及所需变换；检查迭代器能力与middle可达。
1. reverse交换对称位置；rotate将[first,middle)接到[middle,last)之后，先处理空段。
2. next_permutation从右找可上升支点，找合适后继、交换并反转后缀；找不到时反转全区间并返回false。
3. 重复值按同一比较器的等价处理，不假定所有元素互异；prev_permutation按相反次序推导。
4. 输出变换前后序列、返回布尔值（如适用）、支点/段边界及元素多重集检查；不以固定库内部交换次数作保证。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。


有限整数序列可调用range-transform；rotate需middle，其余操作禁止middle。next/prev-permutation以has_adjacent及重置后的序列共同验收，重复值无需互异。

## B — 边界与失败信号

reverse需要双向能力，rotate最低能力与所用版本有关。某个具体排列后继不同于全排列生成或排名工具；原书random_shuffle是历史接口，不为当前随机质量背书。

## 相关能力

iterator-dispatch；sorting-selection；logical-end。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。
