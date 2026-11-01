# 案例候选池（独立案例视角）

本文件只记录原书中的例题、程序演示及图解，全部 `worked_example`；不把它们写成作者的真实人生决策。定位使用 PDF 的 1-based 物理页。原书输出是历史 SGI 环境的报告，本提取器没有重新编译这些程序；`outcome` 不是本次实测结果。

取材记录：已在 `reading/chapter-01.txt` 至 `chapter-08.txt` 的全文中检索“例如、举例、实例、范例、测试、结果”等信号，读取下列候选的相邻完整页。页图复核：PDF104、157、189、303；其余候选依据 OCR 与相邻正文，复杂图中的颜色、箭头和难辨数字没有据 OCR 补造。此工作不是全书所有程序的逐行校对；示例池保留高价值、可定位的案例，不声称穷尽全部例题。网站广告、序跋经历和历史工具链测试未转为技术案例。

```yaml
- id: c01
  title: 32、64、96字节请求共享内存池
  type: case
  example_kind: worked_example
  source_chapter: §2.2.10，PDF104–105，图2-7
  source_quote: "内存池只够供应 (32*20)/64=10 个64 bytes区块"
  summary: |
    从空池开始，请求32字节规格的一批20块，系统先取得40块大小的储存。
    第1块交给客户，19块挂free_list[3]，其余20块留作内存池。
    随后64字节规格只能从剩余640字节取得10块；1块交出，9块挂free_list[7]。
    再请求96字节规格时池为空，需重新向heap取空间。
  bound_to: [小区块配置与内存池分批供应]
  outcome: "32字节链剩19块、64字节链剩9块；第二批后池内剩余为0。96字节请求触发补池。"
  tags: [allocator, pool, refill]
  task_ids: [T03]
  evidence_status: 页图104核过数值；96字节附加量只保留原书符号，不声称已换算为整块数

- id: c02
  title: 同一个find分别遍历vector、list和deque
  type: case
  example_kind: worked_example
  source_chapter: §3.1，PDF116–117，3find.cpp
  source_quote: "只要给予不同的迭代器，find()便能够对不同的容器进行查找操作"
  summary: |
    相同数组被用来建立vector、list和deque。
    三次find以各容器的begin/end为范围，分别查找4、6、8。
    找到时解引用返回迭代器；未找到时用对应容器的end判断。
  bound_to: [算法和容器通过迭代器解耦, 查找结果与尾迭代器判定]
  outcome: "原书报告4 found、6 found、8 not found。"
  tags: [iterator, find, range]
  task_ids: [T04]
  evidence_status: OCR正文及代码输出可辨；数组完整初值未据损坏OCR复刻

- id: c03
  title: vector添加元素时大小与容量分别变化
  type: case
  example_kind: worked_example
  source_chapter: §4.2.5，PDF156–158，4vector-test.cpp
  source_quote: "vector<int> iv(2,9);"
  summary: |
    初始包含两个9；依次push_back 1、2、3、4、5。
    原书记录size从2增长到7，capacity依次经历2、4、8。
    随后的pop_back缩小size而保留capacity=8。
    此案例展示SGI实现的历史增长策略，不是所有std::vector必须翻倍的证明。
  bound_to: [vector三指针不变量, 扩容与元素生存期]
  outcome: "添加5后为9 9 1 2 3 4 5，size=7、capacity=8；三次pop后size=4、capacity=8。"
  tags: [vector, size, capacity]
  task_ids: [T05, T02]
  evidence_status: 页图157已核；该页find后的if(ivite)不是可移植的未找到判定，不能照抄

- id: c04
  title: vector擦除、批量插入与clear不等于释放容量
  type: case
  example_kind: worked_example
  source_chapter: §4.2.5–4.2.6，PDF157–158
  source_quote: "capacity=8"
  summary: |
    承接前例删去值1后，内容为9 9 2，size=3。
    在值2的位置之前插入三个7，内容变为9 9 7 7 7 2。
    本次容量够用，插入前后capacity仍为8。
    clear使size变0，历史测试中capacity保持8。
  bound_to: [已有空间内插入与搬移, 清空元素和释放储存的区分]
  outcome: "插入后size=6；clear后size=0、capacity=8。"
  tags: [vector, erase, insert, clear]
  task_ids: [T05, T02]
  evidence_status: OCR；PDF158变量iv/ivec混写需手工修正后才可作可运行示例

- id: c05
  title: list在值3之前插入99并保留原节点迭代器
  type: case
  example_kind: worked_example
  source_chapter: §4.3.5，PDF169–170，4list-test.cpp
  source_quote: "ilist.insert(ite,99);"
  summary: |
    list依次加入0、1、2、3、4，find取得指向3的迭代器。
    在该位置前插入99后，遍历得到0 1 2 99 3 4。
    原迭代器仍指向3；再删除值1的节点，列表为0 2 99 3 4。
  bound_to: [节点链接与元素位置, list插入和迭代器语义]
  outcome: "插入后size=6；原迭代器解引用仍为3。"
  tags: [list, node, insert]
  task_ids: [T06]
  evidence_status: OCR；示例中的ite!=0不能泛化成标准迭代器未找到判定

- id: c06
  title: list接合另一条列表后反转与排序
  type: case
  example_kind: worked_example
  source_chapter: §4.3.6，PDF176–177，图4-8a/b
  source_quote: "技术上很简单，只是节点间的指针移动而已"
  summary: |
    主列表为0 2 99 3 4，另一列表包含5 6 7 8 9。
    找到99，将第二列表splice到它之前，得到0 2 5 6 7 8 9 99 3 4。
    reverse改变链接顺序；sort产生递增次序。
    图解的内部transfer不是客户端公开接口。
  bound_to: [list节点区间迁移, 容器专属排序]
  outcome: "sort后为0 2 3 4 5 6 7 8 9 99。"
  tags: [list, splice, transfer, sort]
  task_ids: [T06]
  evidence_status: OCR正文；未逐箭头复核图4-8a的七次指针赋值

- id: c07
  title: deque两端插入示例与缓冲区单位冲突
  type: case
  example_kind: worked_example
  source_chapter: §4.4.3、§4.4.5，PDF183–184、189–190
  source_quote: "deque<int,alloc,32> ideq(20,9);"
  summary: |
    示例构造20个9，再按下标改成0至19。
    尾部追加0、1、2、3，头部依次插入99、98、97。
    最后size=27，头部顺序为97 98 99，随后原序列及尾部新增项。
    原书把第三参数32解释成32bytes；但同章buffer_size调用的源码在n非0时返回n，应核验它是元素数还是字节数。
  bound_to: [deque分段布局与两端插入, 代码和注释交叉核对]
  outcome: "元素顺序及size可按操作推演；32bytes注释与源码口径冲突，不作为通过的缓冲区规则。"
  tags: [deque, buffer, erratum-candidate]
  task_ids: [T07]
  evidence_status: 页图189确认原书确实写32bytes；布局单位须在needs-review或勘误记录处理

- id: c08
  title: vector上的建堆、入堆、出堆和堆排序
  type: case
  example_kind: worked_example
  source_chapter: §4.7.4，PDF218–219，4heap-test.cpp
  source_quote: "// 9. return but no remove."
  summary: |
    初始序列为0 1 2 3 4 8 9 3 5；make_heap建立最大堆。
    先push_back(7)，再push_heap把新末项纳入堆。
    pop_heap把原最大值移到末尾，随后pop_back才真正缩短vector。
    最后对剩余堆执行sort_heap。
  bound_to: [heap范围契约, 算法重排与容器删除的分离]
  outcome: "pop_heap后back为9；删除后sort_heap得到0 1 2 3 3 4 5 7 8。"
  tags: [heap, push-heap, pop-heap]
  task_ids: [T08, T13]
  evidence_status: OCR；内部堆数组排列是该实现示例，不应作为所有实现的唯一预期

- id: c09
  title: 红黑树逐个插入时的旋转和变色
  type: case
  example_kind: worked_example
  source_chapter: §5.2.7，PDF268–270，图5-19
  source_quote: "依序将10，7，8，15，5，6，11，13，12插入至RB-tree"
  summary: |
    原书以同一棵树逐个插入9个键，展示成长与调整。
    图中把只变色、单旋转、双旋转分别标出。
    此例可以作为复画节点、检查次序及颜色约束的A1材料。
    每一步具体颜色和父子关系必须从页图重建，不能从OCR的孤立数字猜出。
  bound_to: [RB-tree插入修复, 旋转保留中序关系]
  outcome: "原书提供逐步树形图；本提取未独立验证整幅图的所有节点关系。"
  tags: [rb-tree, rotation, recolor]
  task_ids: [T09]
  evidence_status: OCR图题与相邻正文；完整图追踪待页图验证，不可直接生成精确树形测试答案

- id: c10
  title: hashtable从53个bucket增长到97个
  type: case
  example_kind: worked_example
  source_chapter: §5.7.6，PDF302–305，5hashtable-test.cpp
  source_quote: "// 97, buckets个数"
  summary: |
    以50作为初始bucket请求值，SGI质数表选择53。
    依次插入59、63、108、2、53、55；2、108、55落入同一bucket。
    再insert_equal加入0至47，使元素总数达到54，超过53后触发重建。
    新bucket数量为97；旧的bucket索引与遍历次序随重散列改变。
  bound_to: [哈希碰撞与链地址, 负载触发重散列]
  outcome: "初始size=6时bucket[2]有3个节点；size=54时bucket_count=97。"
  tags: [hashtable, collision, rehash]
  task_ids: [T10]
  evidence_status: 页图303已核插入顺序与53/54/97；这是历史SGI策略，不是现代unordered容器规定

- id: c11
  title: copy右移重叠在原生指针与deque上表现不同
  type: case
  example_kind: worked_example
  source_chapter: §6.4.3，PDF354–357，6copy-overlap.cpp
  source_quote: "如果输出区间的起头与输入区间重叠，我们便不能使用copy"
  summary: |
    输入0至8，源范围为索引[2,7)，先演示向索引0开始的左移复制。
    再演示向索引4开始的右移重叠：原生指针分支借memmove在历史实现中碰巧符合期望。
    改用deque迭代器后，逐元素向前赋值覆盖了尚未读取的数据，出现不同结果。
    这组对照说明不能用某次实验成功放宽算法契约。
  bound_to: [copy重叠限制, traits分派, 复制方向]
  outcome: "历史deque右移示例打印0 1 2 3 2 3 2 3 2；右移应另核copy_backward前提。"
  tags: [copy, overlap, dispatch]
  task_ids: [T11, T04]
  evidence_status: OCR正文和输出；违规重叠只作历史反例，不作为可移植C++结果保证

- id: c12
  title: remove零值只压缩逻辑有效前缀
  type: case
  example_kind: worked_example
  source_chapter: §6.7.1 remove，PDF395
  source_quote: "这一算法并不真正从容器中删除那些元素"
  summary: |
    对0 1 0 2 0 3 0 4执行remove去掉0。
    保留下来的1、2、3、4依原相对次序被写入前4个位置。
    返回值指向第5个位置，容器自身大小保持8。
    需要容器erase才能真正缩短；尾部残余不应继续当结果遍历。
  bound_to: [逻辑移除与物理删除, 算法返回新尾]
  outcome: "有效范围为1 2 3 4；size不变。"
  tags: [remove, erase, logical-end]
  task_ids: [T12]
  evidence_status: OCR；不把历史int示例的尾部值推广到任意类型

- id: c13
  title: unique图解只折叠相邻的重复群
  type: case
  example_kind: worked_example
  source_chapter: §6.7.1 unique，PDF409，图6-6L
  source_quote: "unique只移除相邻的重复元素"
  summary: |
    图6-6L把重复群整理进新的有效前缀，并保留尾部残余。
    作者将它与remove的返回新尾及erase后续操作作比较。
    若目标是全局去重，需要先使相同值相邻；排序会改变原顺序，不能隐去此代价。
  bound_to: [相邻去重, 稳定压缩与返回新尾]
  outcome: "只保证有效前缀没有相邻重复；容器元素个数未改变。"
  tags: [unique, adjacent, logical-end]
  task_ids: [T12]
  evidence_status: OCR可核正文结论；图内完整数列未清晰识别，未据此制造数值样例

- id: c14
  title: 数值算法用1至5展示初值和折叠方向
  type: case
  example_kind: worked_example
  source_chapter: §6.3.1，PDF337–338，6numeric.cpp
  source_quote: "// 65, i.e. 10 + 1*1 + 2*2 + 3*3 + 4*4 + 5*5"
  summary: |
    序列1 2 3 4 5配合accumulate(init=0)得到15。
    以multiplies操作而仍给初值0时，最终结果是0，而非120。
    inner_product在平方和55上再加初值10，得到65。
    同一序列用partial_sum减法给出1 -1 -4 -8 -13，展示顺序折叠而非任意结合。
  bound_to: [数值算法初值, 运算次序与可调用策略]
  outcome: "默认累加15；inner_product初值10得65；partial_sum减法输出1 -1 -4 -8 -13。"
  tags: [numeric, accumulate, inner-product]
  task_ids: [T14]
  evidence_status: OCR；未逐字复刻函数名识别损坏部分，输出可由显式算式核算

- id: c15
  title: 相邻差分与部分和往返恢复
  type: case
  example_kind: worked_example
  source_chapter: §6.3.3、6.3.5，PDF340、343
  source_quote: "如果加法与减法的定义一如常规定义"
  summary: |
    输入1 2 3 4 5，adjacent_difference保留首项并记录后项减前项。
    差分为1 1 1 1 1，再执行partial_sum恢复原序列。
    反向先算部分和1 3 6 10 15，再差分也可恢复。
    作者把通常加减定义列为前提，不能对任意用户二元函数宣称互逆。
  bound_to: [差分表示与累积恢复, 数值操作的代数前提]
  outcome: "常规整数加减下恢复1 2 3 4 5。"
  tags: [adjacent-difference, partial-sum]
  task_ids: [T14]
  evidence_status: OCR；未对浮点舍入误差提供原书外的零误差保证

- id: c16
  title: sort分割图以枢轴2与16展示双向扫描
  type: case
  example_kind: worked_example
  source_chapter: §6.7.9，PDF433–434，图6-14a/b
  source_quote: "如果发现两个迭代器交错了，表示整个序列已经调整完毕"
  summary: |
    原书在相同类型数列上分别选枢轴2和16演示分割。
    first从左找不小于枢轴的项，last从右找不大于枢轴的项；未交错时交换。
    交错后返回右段的起始位置，左右各段并不因此完整排序。
    图中所有具体数值位置要回页图追踪；它只演示sort内部一步。
  bound_to: [双向分割, sort内部状态推演]
  outcome: "得到按枢轴划分的两个子区间；不是整个序列已经有序。"
  tags: [sort, partition, pivot]
  task_ids: [T13]
  evidence_status: OCR可核枢轴和过程；未逐格复算图中长数组，不据此断言唯一排列

- id: c17
  title: nth_element固定秩位置而不保证两侧有序
  type: case
  example_kind: worked_example
  source_chapter: §6.7.12，PDF449
  source_quote: "并且不保证维持原有的相对位置"
  summary: |
    输入22 30 30 17 33 40 17 23 22 12 20，nth为begin()+5。
    原书给出一种重排，其第六项为22，与全排序对应项相同。
    再按greater<int>处理时，第六项仍为22，但两侧按相反关系分隔。
    第六项原值40并不是固定枢轴合同；原书先说“小于原40”的解说不能推广为算法定义。
  bound_to: [选择算法秩合同, 与完全排序及partial_sort的区别]
  outcome: "begin()+5最终为22；两侧各自无需有序，精确排列不具有可移植保证。"
  tags: [nth-element, rank, selection]
  task_ids: [T13]
  evidence_status: OCR；只把可核秩与分区关系用于验证，原文说明误导单独保留

- id: c18
  title: 插入、反向及流配接器共同驱动copy
  type: case
  example_kind: worked_example
  source_chapter: §8.1.2，PDF467–468，8iterator-adapter.cpp
  source_quote: "front_insert_iterator会将assign操作改为push_front操作"
  summary: |
    从0 1 2 3 4 5建立deque，copy到ostream迭代器负责输出。
    front_inserter追加来源项1到头部，back_inserter把3加到尾部。
    找到原值5，在其前用inserter写入0 1 2，再通过反向迭代器输出。
    最后把流输入通过inserter接到容器头部；输入结束由流状态决定。
  bound_to: [输出赋值转插入, 遍历方向与输入源的配接]
  outcome: "插入后序列为1 0 1 2 3 4 0 1 2 5 3；反向输出3 5 2 1 0 4 3 2 1 0 1。"
  tags: [adapter, inserter, reverse, stream]
  task_ids: [T15]
  evidence_status: OCR；示例只向front插入单项，不把它误作多项插入保持源序的证明

- id: c19
  title: bind与compose组合成先加2再乘3
  type: case
  example_kind: worked_example
  source_chapter: §8.1.3，PDF469–470，8compose.cpp
  source_quote: "// 欲于每个元素v身上执行(v+2)*3"
  summary: |
    输入2 21 12 7 19 23；先把plus第二参数绑定2，再把multiplies第二参数绑定3。
    compose1把它们串成f(g(v))，transform把返回值写到输出迭代器。
    同一按值函数给for_each调用时，返回值被丢弃，原容器保持不变。
    原书将for_each笼统称为不能更改元素，不应作为一般C++规则保存；此例不变的具体原因是参数及返回语义。
  bound_to: [函数策略组合, 返回值消费与就地修改的区分]
  outcome: "transform输出12 69 42 27 63 75；按值for_each演示仍输出原序列。"
  tags: [functor, compose, transform, for-each]
  task_ids: [T14, T15]
  evidence_status: OCR；compose1属书中SGI扩展；历史nonmutating断言须纠正归因

- id: c20
  title: not1配合bind2nd表示不小于12
  type: case
  example_kind: worked_example
  source_chapter: §8.1.3、8.4，PDF469、488–492
  source_quote: "再加上否定操作"
  summary: |
    先将less的右参数绑定为12，得到输入x时计算x<12的一元谓词。
    再取逻辑否定，得到!(x<12)，可交给接受一元谓词的算法。
    示例说明按参数位置解释绑定，再解释否定，不能仅靠函数名猜含义。
  bound_to: [可配接仿函数, 参数绑定与谓词否定]
  outcome: "谓词为x>=12；该段未给具体输入序列与计数结果，故不补造计数。"
  tags: [functor, bind2nd, not1, predicate]
  task_ids: [T15, T14]
  evidence_status: OCR；这是历史适配器用法，现代替代另立补充来源
```

## 未清楚部分与供下游处理的限制

- 尚未重新编译原书程序；多数旧接口（`alloc`、三模板参数deque、`compose1`等）不适合直接放进现代标准库演示。
- 红黑树图5-19与排序长数组图，只能先作为有出处的图解候选；未把节点颜色或所有交换位置OCR成可靠结构数据。
- `deque` 的32bytes注释、`nth_element` 对原值40的描述、`for_each`不能改元素的泛称，都是已定位的冲突或误导候选，不能带入active规则。
- 未单独提取slist、AVL旋转、成员函数配接器、排列算法等所有程序。它们在书中存在；是否需要独立A1由后续任务覆盖审计决定。这里没有案例不表示其机制不存在或不可执行。
