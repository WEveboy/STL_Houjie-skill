# 反例与失败边界候选池

独立视角：counter-example-extractor。未建立FTS索引，按该提取器的降级路径，对chapter-01至chapter-08（PDF33–500）逐页OCR扫描“注意／不能／前提／失败／失效／未可预期”等警告与条件，回读相关段落及相邻页。主要核对段落为PDF82–108、159–179、205–219、241、271–282、293–316、330–365、367–409、414–417、428–443、475–497。范围是警告候选扫描，不等于逐行核验全部程序与证明。OCR运算符可能损坏，所有位置均用物理PDF页；短引文最终进入能力卡前应再次对照页图。

以下是**书中明确指出的技术失败情形或边界**，不是作者个人失败经历，也不是由我们替作者补写的自我反思。`mechanism`与`warning_signs`是对所引段落的解释与可检查化，非新增作者原话。

```yaml
- id: ce01
  title: 混用标准allocator与SGI alloc接口
  type: counter-example
  source_chapter: '§2.2，PDF82–89'
  source_quote: '则不能采用标准写法'
  failure_mode: '把以类型参数工作的标准allocator接口直接套到原书SGI字节配置器，或反过来。'
  mechanism: '两者的模板参数及配置单位不同；原书simple_alloc另作元素大小包装。'
  warning_signs: ['把alloc写成allocator<T>的同名替代', '没有区分元素数与字节数']
  bound_to: [allocator-contract, source-version]
  tags: [counter-example, allocator, historical-api]
  task_ids: [T01, T02, T03]

- id: ce02
  title: 构造异常后遗漏已成功构造的部分
  type: counter-example
  source_chapter: '§2.3，PDF106–108'
  source_quote: '必须能够将已产生的所有元素析构掉。'
  failure_mode: '批量构造在中途抛异常，先前构造成功的对象仍存活而清理路径已退出。'
  mechanism: '未初始化算法在raw storage上逐个开始对象生存期，须跟踪已构造边界供异常处理销毁；储存释放由其拥有者另负责。'
  warning_signs: ['仅在正常返回分支析构', 'catch中直接释放储存而未销毁已构造对象']
  bound_to: [object-lifetime, uninitialized-algorithms, vector-growth]
  tags: [counter-example, exception, lifetime]
  task_ids: [T02, T05]

- id: ce03
  title: 内存不足处理未设置或无实际释放能力
  type: counter-example
  source_chapter: '§2.2.5，PDF93–94'
  source_quote: '设计“内存不足处理例程”是客端的责任'
  failure_mode: '把分配器内的重试机制误解为无条件保证分配成功。'
  mechanism: '第一级malloc失败后依赖客端设置的处理器；未设置则异常或终止，设置后仍须能够改善内存情况。'
  warning_signs: ['认为存在oom循环就永不失败', '没有记录分配失败出口']
  bound_to: [allocator-oom, memory-pool]
  tags: [counter-example, allocation, failure-path]
  task_ids: [T03]

- id: ce04
  title: vector扩容后继续使用原迭代器
  type: counter-example
  source_chapter: '§4.2.5，PDF159–160'
  source_quote: '指向原vector的所有迭代器就都失效了。'
  failure_mode: '保存旧begin或元素地址，扩容之后仍用它访问容器。'
  mechanism: '动态增长另配较大连续区间、迁移元素并释放原储存，不是保证在原尾端接续空间。'
  warning_signs: ['push_back或insert触发重新配置', '通过旧地址判断或继续递增']
  bound_to: [vector-growth, iterator-validity]
  tags: [counter-example, vector, invalidation]
  task_ids: [T05]

- id: ce05
  title: 把list擦除节点的迭代器仍视为有效
  type: counter-example
  source_chapter: '§4.3.3，PDF166–167'
  source_quote: '只有“指向被删除元素”的那个迭代器失效'
  failure_mode: '把链表插入时迭代器稳定的性质套到已删除节点。'
  mechanism: '链接调整不会搬迁其他节点，但erase销毁并释放目标节点；指向其他节点和指向目标节点须分别判断。'
  warning_signs: ['erase后继续解引用或递增同一个旧迭代器', '用“list永不失效”作结论']
  bound_to: [list-nodes, iterator-validity]
  tags: [counter-example, list, invalidation]
  task_ids: [T06]

- id: ce06
  title: list splice位置落入被转移范围
  type: counter-example
  source_chapter: '§4.3.6，PDF175–178'
  source_quote: 'position不能位于[first,last)之内'
  failure_mode: '同一链表中转移一段节点时，目标位置落在该段内部。'
  mechanism: 'transfer通过重接端点链接移动区段，内部目标将破坏所假设的端点关系；必须按重载分别核对前提。'
  warning_signs: ['只凭“允许同一list”省略范围检查', 'position与源区间归属未记录']
  bound_to: [list-transfer, list-splice]
  tags: [counter-example, list, precondition]
  task_ids: [T06]

- id: ce07
  title: 对无随机访问能力的容器调用通用sort
  type: counter-example
  source_chapter: '§4.3.6、§6.7.9，PDF179、428、436'
  source_quote: 'sort()只适用于RandomAccessIterator'
  failure_mode: '因为list能遍历就认为它能作为通用sort的输入。'
  mechanism: 'sort源码需要差值、跳跃和有序迭代器比较；list仅双向，slist仅前向，应使用相应成员排序。'
  warning_signs: ['sort(list.begin(),list.end())', '在Forward迭代器上使用last-first或first+n']
  bound_to: [iterator-contract, sort-selection]
  tags: [counter-example, sort, iterator-category]
  task_ids: [T04, T06, T13]

- id: ce08
  title: 将deque逻辑连续误当作所有对象物理连续
  type: counter-example
  source_chapter: '§4.4.2–4.4.3，PDF181–186'
  source_quote: '各种指针运算如加、减、前进、后退都不能直观视之。'
  failure_mode: '以单一裸指针跨过deque缓冲区，或假定其迭代器只存cur。'
  mechanism: '随机访问能力由cur/first/last/node协调实现，跨缓冲时必须切换节点和边界。'
  warning_signs: ['把&d[0]后面的储存当作整个deque数组', '跨缓冲后未更新所属节点']
  bound_to: [deque-layout, iterator-arithmetic]
  tags: [counter-example, deque, layout]
  task_ids: [T07]

- id: ce09
  title: 给容器配接器强加遍历或任意排序接口
  type: counter-example
  source_chapter: '§4.5–4.8、§8.3.2，PDF205–208、222、478'
  source_quote: 'queue不允许有遍历行为。'
  failure_mode: '因底层deque/vector有begin/end，就认为stack、queue、priority_queue也应直接暴露这些接口。'
  mechanism: '配接器限制进出次序及访问方式，任意访问可能绕开它的行为契约；其公开接口不同于底层容器。'
  warning_signs: ['对stack.begin()或priority_queue.begin()写通用算法', '未核底层操作要求就替换容器类型']
  bound_to: [container-adapters, composition]
  tags: [counter-example, adapter, interface]
  task_ids: [T08, T15]

- id: ce10
  title: 没有先追加元素或建立堆就调用堆维护算法
  type: counter-example
  source_chapter: '§4.7.2，PDF211–219'
  source_quote: '新元素已经插入到底部容器的最尾端。'
  failure_mode: '把push_heap当作自动分配/插入，或直接在任意无序区间上调用sort_heap。'
  mechanism: 'push_heap只维护最后元素加入既有堆后的次序；sort_heap依赖已有堆性质。满载固定array没有可追加位置。'
  warning_signs: ['push_heap前容器size不变', '未检查[first,last-1)是否为堆', '忽略比较策略一致性']
  bound_to: [heap-contract, priority-queue]
  tags: [counter-example, heap, precondition]
  task_ids: [T08, T13]

- id: ce11
  title: pop_heap后忘记缩小容器
  type: counter-example
  source_chapter: '§4.7.2，PDF215'
  source_quote: '最大元素只是被置放于底部容器的最尾端，尚未被取走。'
  failure_mode: '认为pop_heap已经删除最大元素，随后继续以全区间作为堆。'
  mechanism: '算法仅重排并把最大值移至尾端；仍要取back并pop_back或缩短逻辑堆区间。'
  warning_signs: ['操作后size仍N但把N个位置都当成堆', '结果最大值仍在数组中却称已擦除']
  bound_to: [heap-pop, priority-queue]
  tags: [counter-example, heap, logical-range]
  task_ids: [T08, T13]

- id: ce12
  title: 无平衡条件的搜索树退化
  type: counter-example
  source_chapter: '§5.1，PDF239–241'
  source_quote: '二叉搜索树可能会失去平衡，造成搜寻效率低落'
  failure_mode: '仅检查左小右大就保证所有查找O(log N)。'
  mechanism: '输入次序及增删可能产生很深的路径，退化为链状；平衡条件才限制高度。'
  warning_signs: ['连续单调插入', '没有高度或平衡不变量检查']
  bound_to: [tree-invariants, rb-tree]
  tags: [counter-example, tree, complexity]
  task_ids: [T09]

- id: ce13
  title: 随意修改有序容器中的键
  type: counter-example
  source_chapter: '§5.3–5.4，PDF271、276–282'
  source_quote: '如果任意改变set元素值，会严重破坏set组织。'
  failure_mode: '把set元素或map的key当作可任意修改的普通值。'
  mechanism: '节点位置由键决定，原位改键可能违背搜索树排序关系；map的mapped value不是key。'
  warning_signs: ['试图通过set iterator改值', '混淆pair.first与pair.second的可写性']
  bound_to: [ordered-key-contract, map-access]
  tags: [counter-example, key, invariant]
  task_ids: [T09]

- id: ce14
  title: C字符串键使用地址相等代替内容相等
  type: counter-example
  source_chapter: '§5.8–5.9，PDF311–316'
  source_quote: '不能直接以const char*做比较。'
  failure_mode: '希望按文字合并或查找键，却直接用默认指针相等。'
  mechanism: '两个不同缓冲区可含相同字符；比较地址无法表达文本等价。原书要求专门设计EqualKey。'
  warning_signs: ['键类型const char*且相等函数仍默认', '同内容的不同缓冲被认作不同键']
  bound_to: [hash-equality, key-semantics]
  tags: [counter-example, hash, string-key]
  task_ids: [T10]

- id: ce15
  title: 单次哈希遍历看似有序就推导排序保证
  type: counter-example
  source_chapter: '§5.8，PDF312–313'
  source_quote: '就呈现出未排序的状态了。'
  failure_mode: '用一次递增输出证明hash_set自动排序。'
  mechanism: '某些整数与bucket分配巧合形成递增外观，改变输入及散列分布即可消除；契约不能由一次输出升级。'
  warning_signs: ['没有检查底层结构就称哈希容器有序', '测试只用极小的顺序整数']
  bound_to: [hash-iteration, evidence-boundary]
  tags: [counter-example, hash, false-inference]
  task_ids: [T10]

- id: ce16
  title: 未满足合法区间与迭代器能力前提
  type: counter-example
  source_chapter: '§6.1.5，PDF330–333'
  source_quote: '却不保证能够在编译时期就被捕捉出来。'
  failure_mode: '传入无效迭代器或无法从first递增到last的范围，依靠“能编译”证明调用有效。'
  mechanism: '模板语法检查不等于运行期对象有效性与区间可达性；算法读取、写入、后退和跳跃各需要相应能力。'
  warning_signs: ['first和last来自不同无关联区间', '把OutputIterator交给find', '解引用end']
  bound_to: [range-contract, iterator-category]
  tags: [counter-example, iterator, precondition]
  task_ids: [T04, T11, T12]

- id: ce17
  title: 只有第二起点的双范围算法读过第二序列尾端
  type: counter-example
  source_chapter: '§6.4.2、§6.7.1，PDF347、352、408'
  source_quote: '如果第二序列的元素个数比第一序列少，会发生未可预期的行为'
  failure_mode: '旧式equal/mismatch/transform等只收到第二起点，却把长度更短的第二序列交给它。'
  mechanism: '第一范围控制循环次数，算法没有第二尾位置就无法检测短缺；比较完全相等还需要先核长度。'
  warning_signs: ['只有first2没有last2', '把前缀相等误作整个序列相等']
  bound_to: [algorithm-range-length, equality-check]
  tags: [counter-example, range, bounds]
  task_ids: [T11, T12, T14]

- id: ce18
  title: copy写入空目标或容量不足的目标
  type: counter-example
  source_chapter: '§6.4.3，PDF357'
  source_quote: 'copy不能直接用来将元素插入空容器中。'
  failure_mode: '对空容器begin使用普通copy，期望自动增长目标容器。'
  mechanism: '普通输出迭代器赋值只覆盖已有对象；用成员insert或插入迭代器才把写入变成增元素。'
  warning_signs: ['目标size为0', '只reserve未resize却向begin复制', '目标有效元素数小于源范围长度']
  bound_to: [copy-output, insert-iterator, object-lifetime]
  tags: [counter-example, copy, output-capacity]
  task_ids: [T02, T11, T15]

- id: ce19
  title: 重叠区间的复制方向错误
  type: counter-example
  source_chapter: '§6.4.3–6.4.4，PDF354–367'
  source_quote: '本例结果错误，因为调用的算法不再使用memmove()执行实际复制操作'
  failure_mode: '向右重叠移动仍逐项从前向后copy；或反向情形错误使用copy_backward。'
  mechanism: '先覆盖了后续尚未读取的源元素，产生连锁错误。某SGI指针快速路径的memmove偶然避免破坏，不能证明该调用在所有实现中合法。'
  warning_signs: ['result落在源范围中间且位于源起点右侧', '用vector测试正确后直接推广到deque', '把实现现象写成标准保证']
  bound_to: [copy-overlap, copy-direction, source-version]
  tags: [counter-example, copy, overlap]
  task_ids: [T11]

- id: ce20
  title: 将无序hash容器直接交给有序集合算法
  type: counter-example
  source_chapter: '§6.5、§6.7.1，PDF367、370、372、375、388–392'
  source_quote: '却不可以应用于本节的四个算法。'
  failure_mode: '因为容器名含set，就认为可直接做set_union等算法。'
  mechanism: '双指针合并逻辑依赖两个范围在同一比较关系下有序；hash_set不提供该关系下的排序保证。'
  warning_signs: ['源范围未验证有序', '排序用less而合并用不同关系', '只检查容器名字']
  bound_to: [set-algorithms, merge, bounds-search]
  tags: [counter-example, sorted-range, hash]
  task_ids: [T10, T12]

- id: ce21
  title: 向Compare参数传入任意二元布尔函数
  type: counter-example
  source_chapter: '§6.7.1 includes，PDF388–390'
  source_quote: '并非随便一个二元运算就可拿来作为comp的参数。'
  failure_mode: '只检查签名能返回bool，就把任意关系作为有序算法Compare。'
  mechanism: '算法常以两个方向都不成立表示等价；无适当排序关系时case分支失去原语义。'
  warning_signs: ['使用非严格关系<=充当less', '未检查排序关系与范围实际顺序一致性']
  bound_to: [comparator-contract, set-algorithms, ordered-tree]
  tags: [counter-example, compare, semantics]
  task_ids: [T09, T12, T13]

- id: ce22
  title: remove或unique之后仍把原end之前全部当结果
  type: counter-example
  source_chapter: '§6.7.1，PDF395–410'
  source_quote: '容器大小并未改变'
  failure_mode: '调用算法后忽略返回的新尾，认为物理容器已经删除元素。'
  mechanism: '算法覆盖并压缩有效前缀，尾部仍有残余对象；需采用返回范围，或用容器成员erase删除尾部。'
  warning_signs: ['算法返回值未使用', '仍打印完整容器并把残余当错算', 'size未变却称删除已完成']
  bound_to: [logical-end, erase-remove, unique]
  tags: [counter-example, remove, unique]
  task_ids: [T12]

- id: ce23
  title: 把unique当作未经组织的全局去重
  type: counter-example
  source_chapter: '§6.7.1 unique，PDF409'
  source_quote: 'unique只移除相邻的重复元素'
  failure_mode: '序列1,2,1调用unique后期望只剩1,2。'
  mechanism: '该算法只比较相邻组；使等价元素相邻后才能借它压缩所有重复。是否允许先排序必须由任务的原顺序要求决定。'
  warning_signs: ['重复元素之间夹有其他值', '去重任务同时要求保持原全局顺序却先排序']
  bound_to: [unique, ordering, task-contract]
  tags: [counter-example, unique, adjacency]
  task_ids: [T12]

- id: ce24
  title: 从inplace_merge名字推出零辅助空间
  type: counter-example
  source_chapter: '§6.7.11，PDF442–443'
  source_quote: '本算法会使用额外的内存空间（暂时缓冲区）'
  failure_mode: '以函数名宣称实现不配置缓冲，或未先把相邻两段分别排好序。'
  mechanism: 'inplace指输出位置回到原范围，并不自动承诺常数额外空间；原书还分别讨论足量缓冲、不足缓冲和无缓冲分支。'
  warning_signs: ['没有区分输出位置与空间复杂度', '两子范围仅拼接但本身未排序']
  bound_to: [inplace-merge, complexity, sorted-range]
  tags: [counter-example, merge, auxiliary-space]
  task_ids: [T12, T13]

- id: ce25
  title: 无push_front接口却使用front_inserter
  type: counter-example
  source_chapter: '§8.3.1，PDF475–477'
  source_quote: '该迭代器不适用于vector，因为vector没有提供push_front函数'
  failure_mode: '把所有插入配接器当作对所有容器通用。'
  mechanism: '配接器operator=最终调用底层特定成员函数；外观相同不改变所需接口。'
  warning_signs: ['front_inserter(vector)', '只核output_iterator语法而未核底层容器操作']
  bound_to: [insert-iterator, adapter-contract]
  tags: [counter-example, adapter, interface]
  task_ids: [T15]

- id: ce26
  title: 把reverse iterator的base当成当前元素
  type: counter-example
  source_chapter: '§8.3.2，PDF478–481'
  source_quote: '并不是一个潜伏的错误，而是一个刻意为之的特征'
  failure_mode: '认为*r等于*r.base()，或用只有单向能力的slist迭代器反向遍历。'
  mechanism: '为保持半开区间对称，base保存的是当前反向元素对应的正向后一位置；解引用时先--副本。'
  warning_signs: ['rbegin().base()==end()时仍直接解引用base', '从rend解引用', 'Forward迭代器上要求--']
  bound_to: [reverse-iterator, iterator-category, range-contract]
  tags: [counter-example, reverse, off-by-one]
  task_ids: [T15]

- id: ce27
  title: 输入迭代器构造早于提示语而提前等待
  type: counter-example
  source_chapter: '§8.3.3，PDF482–483'
  source_quote: '会停留在(A)等待一个输入，然后才执行(B)出现提示信息。'
  failure_mode: '以为istream_iterator构造只是保存流引用，把提示语放在构造之后。'
  mechanism: '原书实现构造时调用read提取第一笔资料，可能先阻塞；把构造推迟到真正需要输入的位置。'
  warning_signs: ['程序无提示却已等待键入', '流迭代器构造隐藏在早期初始化']
  bound_to: [stream-iterator, side-effect-order]
  tags: [counter-example, stream, initialization]
  task_ids: [T15]

- id: ce28
  title: SGI扩展配接器误当成所有标准库接口
  type: counter-example
  source_chapter: '§8.4.3，PDF493'
  source_quote: '本节的两个配接器并未纳入STL标准，是SGI STL的私产品'
  failure_mode: '把compose1/compose2直接用于目标标准库而不查可用性。'
  mechanism: '源码剖析材料包含标准接口及SGI扩展；学习其设计不能推出所有编译器均提供同名组件。'
  warning_signs: ['未记录目标库及版本', '示例编译失败后仅猜头文件']
  bound_to: [function-adapters, source-version]
  tags: [counter-example, extension, portability]
  task_ids: [T01, T15]
```

## 审计附注：与作者警告分开

PDF449关于nth_element的“更精确地说是不大于”和PDF470关于for_each“元素内容不能更改”，此前已在原则视角用页图核实其文字确实存在，属于**我们发现的来源冲突／过度概括**，不列入上面的“作者正确警告”候选，也不称为作者承认错误。三重验证须分别处理，详细记录见principles.md的p35与p43。不再扩展全书勘误。

本视角未把“array不适合remove”的原书取舍泛化为禁止在固定数组上压缩逻辑范围；也未把旧式函数指针配接限制泛化为现代callable规则。所有现代标准扩展、接口移除年代及标准级重叠合法性，应由主流程另核原始规范；这里只保留书中明示失败机制。
