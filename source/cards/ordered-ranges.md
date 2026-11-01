# 检查有序范围的边界与多重集合规则

## R — 原文锚点

> 必须是有序区间，元素值允许重复出现。

出处：§6.5，PDF367–375。

> 指向第一个“不小于value”的元素。

出处：§6.7.2–6.7.4、6.7.10，PDF414–418、439–441。

## I — 方法解释

有序算法依赖相同的比较关系，不依赖容器名字。lower与upper对应不同的边界表达式，重复值让这种差别直接可见。集合算法按有序多重集合处理出现次数；二分减少比较次数，却未必减少链式迭代器的移动次数。

## A1 — 原书示例或标明的演练

合成演练：对[1,2,2,4]查2，lower偏移1、upper偏移3、equal范围[1,3)。集合输入A=[1,1,2]、B=[1,3]，union保留每键次数的最大值，得到[1,1,2,3]；intersection取最小次数，得到[1]。

以上为本项目合成演练，不冒充作者亲历或独立来源。

## A2 — 触发与近邻区分

lower_bound/upper_bound/equal_range/binary_search、set_union/intersection/difference、重复值、list二分复杂度。

以本卡输出契约为准；遇到相邻任务再补读iterator-dispatch；ordered-associative；logical-end，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：合法范围、比较器、查询键或第二输入范围；先检查具体算法所需partition/同序前提。
1. lower找首个!comp(element,value)，upper找首个comp(value,element)；不存在时返回last。
2. 对二分查询分别报告比较次数O(log N)与Forward上的移动O(N)；有树容器时考虑成员边界查找。
3. 集合双游标遇相等值按算法消耗；union/max、intersection/min、difference/max(a-b,0)、symmetric difference/abs(a-b)。
4. 输出边界偏移/区间或多重集合结果、前提与成本。bounds工具只接受已排序整数数组，不自动重排不合法输入。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。


有序整数多重集合可调用set-ops的union/intersection/difference/symmetric-difference。两个输入各最多256项；顺序前提不满足则拒绝，输出按重数保留，不能改成普通set。

## B — 边界与失败信号

不能把严格升序当唯一合法输入，也不能忽略重复值。二分的精确前提是相关表达式的partition；升序是常用充分条件，不是所有重载的最弱必要条件。

## 相关能力

iterator-dispatch；ordered-associative；logical-end。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。
