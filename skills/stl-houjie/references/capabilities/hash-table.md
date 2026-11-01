# 把哈希定位、相等与重散列分开

## R — 原文锚点

> 不可能只是原封不动地拷贝而已

出处：§5.7，PDF290–300。

> 不能直接以const char*做比较。

出处：§5.8–5.9，PDF311–316。

## I — 方法解释

哈希值先选桶，相等谓词再在碰撞链中判断键。重散列改变桶数后必须重新计算位置，而不是把旧桶原样复制；大小不变也可能改变迭代顺序。字符串内容相等不能用无关的指针地址比较代替。

## A1 — 原书示例或标明的演练

原书例题／程序演示（§5.7.6，PDF302–305，5hashtable-test.cpp）：

以50作为初始bucket请求值，SGI质数表选择53。
依次插入59、63、108、2、53、55；2、108、55落入同一bucket。
再insert_equal加入0至47，使元素总数达到54，超过53后触发重建。
新bucket数量为97；旧的bucket索引与遍历次序随重散列改变。

原书报告：初始size=6时bucket[2]有3个节点；size=54时bucket_count=97。

证据边界：页图303已核插入顺序与53/54/97；这是历史SGI策略，不是现代unordered容器规定。不是本次重跑历史程序的结果。

## A2 — 触发与近邻区分

hashtable、bucket、碰撞链、rehash/resize、hash_map/hash_set、字符串哈希和相等。

以本卡输出契约为准；遇到相邻任务再补读ordered-associative；source-reading，不把一个术语命中当作已经完成任务。

## E — 输入、执行与完成标准

输入：键序列、hash与相等定义、桶数及重建规则；缺hash时可明确提出整数mod的教学约定，不能冒充库实现。
1. 检查相等的键必须得到相容哈希，并区分唯一键/允许重复。
2. 按bucket=hash(key)%bucket_count逐个定位，碰撞在桶内用相等谓词核验。
3. 改桶数后重新分配每个键并记录新桶；不从旧迭代器或旧遍历顺序继续操作。
4. 输出桶分布、冲突、元素数/桶数和重散列前后变化。hash-buckets使用整数mod模型，不实现真实SGI prime表或完整哈希容器。

需要代码时先查随包usage资源；没有运行条件应标注推演，不能声称实跑。

## B — 边界与失败信号

常数平均查找依分布等条件，不能保证最坏O(1)。旧hash_*不是现代unordered_*的同名标准接口。原书prime选择“大于”文字与lower_bound的>=边界需以代码为准。

## 相关能力

ordered-associative；source-reading。依赖与组合关系按本卡A2/E说明使用；不要求每次全包加载。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/stl_lab.py](../../resources/stl_lab.py)
- [resources/stl_extensions.py](../../resources/stl_extensions.py)
- [resources/experiment_audit.py](../../resources/experiment_audit.py)
- [resources/test_stl_lab.py](../../resources/test_stl_lab.py)
- [resources/test_stl_extensions.py](../../resources/test_stl_extensions.py)
- [resources/contract_checks.cpp](../../resources/contract_checks.cpp)
- [resources/usage.md](../../resources/usage.md)
