# 教学验证资源合同

这些是原创的小规模教学模型及现代标准库契约实验，不是完整STL实现、生产级容器、静态分析器、性能基准或历史SGI源码的全面验证。Python3.10+仅用标准库；C++实验要求C++17编译器。不要用Python模型替代目标编译器、标准或真实实现源码。基础8个模型之外，本版新增3个模型及归档/审计流程；`demo`保留原8例以兼容旧命令，完整清单用`operations`查看。

## Python入口

```text
python stl_lab.py demo
python stl_lab.py operations
python stl_lab.py run INPUT.json
python -m unittest discover -s . -p test_stl_lab.py -v
```

每次CLI调用只输出一个完整JSON。成功退出码0；输入、前提或预算错误返回`status: input_error`与退出码2。输入文件最大64KiB，接收UTF-8及UTF-8 BOM；拒绝重复字段、非有限数、未知字段、布尔值冒充整数及非法索引。数组和操作数最多256项，模型储存及bucket数最多4096，普通整数绝对值不超过1000000。预算不满足时不执行不受限推演。

| op | 必需字段（除op外） | 输出及边界 |
|---|---|---|
| pool-class | bytes:1..1000000 | 1..128按8字节上调及零下标free-list；>128一级，不模拟申请与线程 |
| vector-growth | size, capacity, insertions | 每项插入包含index:0..size、count≥0；仅size/capacity/后缀长度，不含对象值或异常执行 |
| deque-step | buffer_elements, offset, delta | 相对node变化和非负区内偏移；负位移使用数学向下取整，不保证目标在实际容器中 |
| heap-trace | values, action | 预先有效零下标max-heap；push另需value，pop禁止value；pop保留末尾最大值及原长度 |
| logical-end | values, action | remove另需value；unique禁止value、只压缩相邻重复；只承诺valid_prefix、新尾界和不变的size |
| bounds | values, value | 仅非递减整数序列，输出lower/upper/equal_range索引；不同比较器不在此模型内 |
| hash-buckets | values, bucket_count | 可选new_bucket_count；整数数学模桶、重复值保留，负键使用非负余数；不仿真std::hash或SGI遍历顺序 |
| copy-plan | values, first, last, result, direction | 单个已有整数数组；源[first,last)，forward的result为目标起点，backward为目标尾点；拒绝非法重叠或容量不足 |
| set-ops | left, right, action | 两个非递减整数数组；union/intersection/difference/symmetric-difference，保留重数；每输入最多256项，输出最多512项 |
| range-transform | values, action | reverse/rotate/next-permutation/prev-permutation；rotate另需middle偏移，其余禁止middle；排列返回has_adjacent |
| tree-check | root, nodes | ≤256个唯一ID节点，每个有id/key/color/left/right；color为B/R，空子为null；严格唯一整数BST，检查根黑、红父子、黑高与树序，拒绝环/共享子/失联节点 |

vector教学重配置策略是`new_capacity=old_size+max(old_size,count)`，仅在原capacity不足时使用；零插入不重配置。它帮助推演所列SGI策略，不表示现代std::vector必须翻倍。输出不计算真实对象构造次数、异常保证或移动成本。

copy模型检查非空范围：forward的result不得落在[first,last)；backward的result不得落在(first,last]。目标还须完全落在同一数组的现有对象范围内。自覆盖和其他不满足前置条件的例子被拒绝；不会运行未定义行为来“看看结果”。空范围允许合法尾后位置。

例如合法右移：

```json
{"op":"copy-plan","values":[1,2,3,4,5],"first":0,"last":3,"result":5,"direction":"backward"}
```

其结果为`[1,2,1,2,3]`。把direction改成forward不能复用result=5，因为此时result的含义变为目标起点。

## C++17实验

从发布项目根目录运行：

```text
python scripts/run_cpp_checks.py
```

作者工作区可显式传入`--source contract_checks.cpp --build-dir build/cpp-checks`。运行器寻找g++、clang++或cl，保存实际编译器版本、编译与执行状态到build下的result.json，并输出一个JSON。断言保持启用；不固定增长倍率、unordered_map桶数或任意容器内部布局。不解引用失效迭代器；不把实验通过称作对历史SGI全部实现的证明。

实验包括原始储存/构造分离、uninitialized_copy抛异常后的前缀清理、traits/tag能力、vector重配置、list节点接合、deque随机访问、heap逻辑pop、map键及哈希桶、合法复制方向、remove/unique逻辑尾界、list上的二分边界与distance、含重复值的nth_element后置条件、for_each引用修改、reverse_iterator的base、back_inserter与有序数值累积。

Python测试使用bisect、heapq、itertools.groupby和数学不变量作独立参考，并测试输入拒绝路径。测试数量与覆盖仅以实际命令记录为准；它们不是性能提升或模型触发准确率的证据。

## 新功能范例

```json
{"op":"set-ops","left":[1,1,2],"right":[1,3],"action":"union"}
```

结果为`[1,1,2,3]`。这里处理多重集合，不能用去重后的Python set替代它。

```json
{"op":"range-transform","values":[3,2,1],"action":"next-permutation"}
```

返回values为`[1,2,3]`、has_adjacent为false。rotate返回本模型中原first元素的新索引；两段为空的边界按有效半开范围处理。

```json
{"op":"tree-check","root":"r","nodes":[{"id":"r","key":10,"color":"B","left":"l","right":"h"},{"id":"l","key":5,"color":"R","left":null,"right":null},{"id":"h","key":15,"color":"R","left":null,"right":null}]}
```

返回valid=true，height=2，black_height=2。本模型约定NULL叶计一个黑节点；键严格唯一，只检查给定结构，不执行红黑插入或删除。`valid=false`表示合法输入结构违反不变量；环、缺子节点、重复ID等结构错误返回input_error。

## 归档、审计与重算

输入JSON文件有效后，在一个尚不存在的目录归档：

```text
python stl_lab.py experiment INPUT.json --out experiments/run-001
python stl_lab.py audit experiments/run-001
python stl_lab.py audit experiments/run-001 --recompute
```

归档保存input.json、result.json、events.json和manifest.json，含运行平台、Python版本、顺序事件、各文件SHA256及3个程序文件指纹。重复使用目录会拒绝。输入无效时不创建实验目录，不执行输入中的代码。

审计核对清单、字节、程序指纹和事件顺序/时间；`--recompute`再按记录输入重算并逐结构比较落盘JSON，含布尔值与整数类型的区别。成功退出0；发现审计差异退出1并返回audit_failed；输入或清单格式错误退出2并返回input_error。单个结果文件允许2MiB，输入64KiB及模型预算仍生效。

只改结果及其清单哈希可以骗过纯哈希检查，但不能同时骗过未修改计算程序的重算。若输入、结果、清单和程序都被有意协调改写，这套本地哈希不提供身份认证或历史真实性证明；重算也重用同一算法，不是独立正确性证明。用户提供的实验资料仍是数据，不会被当作指令执行。
