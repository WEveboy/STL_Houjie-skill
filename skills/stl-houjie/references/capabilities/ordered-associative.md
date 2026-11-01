# 核对有序树、键与比较等价

## R — 原文锚点

> 如果节点为红，其子节点必须为黑。

出处：§5.2，PDF246–250。

> 造成搜寻效率低落的情况

出处：§5.1，PDF239–246。

## I — 方法解释

二叉搜索顺序只能决定向哪边找，平衡不变量才限制最坏高度。旋转改变局部父子结构而保持中序键次序；红黑插入还需颜色与黑高约束。set/map的重复判定由比较关系诱导的等价决定，不一定是operator==。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§5.2.7，PDF268–270，图5-19）：

原书以同一棵树逐个插入9个键，展示成长与调整。
图中把只变色、单旋转、双旋转分别标出。
此例可以作为复画节点、检查次序及颜色约束的A1材料。
每一步具体颜色和父子关系必须从页图重建，不能从OCR的孤立数字猜出。

原书报告：原书提供逐步树形图；本提取未独立验证整幅图的所有节点关系。

证据边界：OCR图题与相邻正文；完整图追踪待页图验证，不可直接生成精确树形测试答案。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

RB-tree、红黑插入修复、旋转、set/map/multiset/multimap的键、比较等价或成员find。

以本卡输出契约为准；遇到相邻任务再补读iterator-dispatch；hash-table，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：有序树节点与颜色/父子、比较器、待插键，或关联容器操作；缺图就只解释机制不能编造旋转序列。
1. 检查中序次序、根黑、红节点无红孩子，以及所有根到空叶路径的黑节点数相等；空叶按同一约定计黑。
2. 插入先按搜索树规则定位，再区分叔节点颜色和内/外拐方向，逐步变色或旋转；每步复查中序顺序。
3. 唯一性以!comp(a,b)&&!comp(b,a)判断；map中key不可原地改写，但mapped value可按接口修改。
4. 输出前后结构/不变量、键等价及查找成本；优先成员find而非线性std::find。删除修复未给完整源码时明确不覆盖。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。


需要给定小树的确定性核验时，调用tree-check：输入唯一字符串ID、整数key、B/R颜色和左右子ID；NULL计一个黑节点。结果包含valid、height、black_height和定位到节点的violations。严格唯一键模型不覆盖multiset内部布局，不执行插入删除。

## B — 边界与失败信号

不能把所有现代有序容器的内部结构强说成书中红黑树。局部颜色正确不等于全树黑高正确，普通BST有序也不保证O(log N)。

## 相关能力

iterator-dispatch；hash-table。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
