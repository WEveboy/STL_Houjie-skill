# 原则与计算规则候选池

独立视角：principle-extractor。来源均为用户扫描版，以下页码均为 **PDF 物理页**，不能按固定偏移换算印刷页码。

扫描范围：对 chapter-01 至 chapter-08（PDF33–500）逐页 OCR 作全域规则/公式/条件关键词扫描，回读命中页的相邻说明与所列代码。该工作是候选提取，不是逐行证明全部源码。主要回读页为73、82–113、121–148、154–162、166–179、180–202、209–219、235–246、261–282、285–317、330–365、367–375、395–417、425–450、453–464、465–500。PDF449、470页图另已目视核验，确认下述疑点实际存在于扫描原文。OCR 的尖括号、下划线、算术符号和公式会损坏；未看图的短引文只作候选证据，最终卡片仍需复核。

```yaml
- id: p01
  title: 以组件职责区分储存、遍历、计算与策略
  type: principle
  source_chapter: '§1.2，PDF38–39'
  source_quote: 'Algorithm 通过 Iterator 存取 Container 内容'
  summary: '把容器的数据布局与算法操作分开；通过迭代器契约衔接，仿函数提供策略，配置器供应储存。分析源码时先判定某段职责，而不是把所有逻辑归到容器名下。'
  tags: [architecture, generic-programming]
  task_ids: [T01]

- id: p02
  title: 半开区间与可达的尾位置
  type: principle
  source_chapter: '§1.9.5、§6.1.5，PDF73、330–333'
  source_quote: '迭代器所指的是“最后一个元素的下一位置”'
  summary: '以[first,last)描述访问范围；循环先比较尾位置再解引用。区间必须可由first按所需操作到达last；first==last是空范围。不能把源码解释中的last-1照搬到只支持递增的迭代器。'
  tags: [range, iterator, precondition]
  task_ids: [T04, T11, T12]

- id: p03
  title: 储存配置与对象构造分离
  type: principle
  source_chapter: '§2.2.2–2.2.3，PDF84–88'
  source_quote: '对象构造操作由 ::construct() 负责，对象析构操作由 ::destroy() 负责。'
  summary: '分别记录allocate/deallocate与construct/destroy。取得一块能容纳n个对象的储存，不等于n个对象已构造；销毁对象也不等于释放储存。它决定容器容量与实际元素数能够分离。'
  tags: [lifetime, allocator]
  task_ids: [T02]

- id: p04
  title: 未初始化内存算法的异常清理责任
  type: principle
  source_chapter: '§2.3，PDF106–113'
  source_quote: '必须能够将已产生的所有元素析构掉。'
  summary: 'uninitialized_copy/fill/fill_n针对未初始化储存构造对象。某次复制构造抛异常时，应销毁已成功构造的部分；调用者另负责释放所拥有的储存。不要把“回滚”解释成所有外部副作用或源对象状态都能回滚。'
  tags: [lifetime, exception, rollback]
  task_ids: [T02]

- id: p05
  title: SGI小区块配置分档公式
  type: calculation
  source_chapter: '§2.2.6–2.2.8，PDF95–99'
  source_quote: '内存需求量上调至8的倍数'
  summary: '该SGI第二级配置器管理8到128字节的16个档。只有n>128才转第一级；因此恰好128仍属小区块。叙述“小于128”遗漏等号，须以代码判断为准。'
  inputs: '正整数n，单位byte；本公式限1<=n<=128'
  formula: 'rounded=8*ceil(n/8); index=ceil(n/8)-1，索引0..15'
  units: byte
  output: '上调区块大小、free-list索引；n>128输出第一级配置器'
  missing_conditions: '0、负值、溢出、特殊对齐需求不能由此公式默认接受；现代配置器策略不由本实现决定。'
  tags: [allocator, sgi, rounding]
  task_ids: [T03]

- id: p06
  title: 小区块归还自由链表而非立即还给系统
  type: principle
  source_chapter: '§2.2.7–2.2.8，PDF97–101'
  source_quote: '就找出对应的 free list，将区块回收。'
  summary: '配置时弹出对应链表头，释放时把区块挂回对应头部；客户占用期间不再由自由链表指向。deallocate必须匹配原大小档，释放并不等于系统堆立即减少。此为历史SGI机制。'
  tags: [allocator, free-list]
  task_ids: [T03]

- id: p07
  title: 内存池能供多少块就回传多少块
  type: calculation
  source_chapter: '§2.2.9–2.2.10，PDF101–104'
  source_quote: '这个pass by reference的nobjs参数将被修改为实际能够供应的区块数。'
  summary: 'refill通常请求20块；chunk_alloc区分足量、不足20但至少一块、连一块都不足。第二种情形修改nobjs，不假定每次必有20块。'
  inputs: '已按8字节对齐的块大小size、请求块数nobjs、bytes_left、heap_size'
  formula: '足量条件bytes_left>=size*nobjs；部分供给时nobjs=floor(bytes_left/size)；新申请量=2*size*nobjs+ROUND_UP(heap_size>>4)'
  units: 'size/bytes_left/heap_size为byte，nobjs为块数'
  output: '供给区块数、池剩余范围、free-list补充情况'
  missing_conditions: 'OOM应变需继续追踪第一级配置器；书中排除多线程，不能据此保证并发安全。'
  tags: [allocator, memory-pool]
  task_ids: [T03]

- id: p08
  title: 五种迭代器关联型别与指针特化
  type: checklist
  source_chapter: '§3.3–3.4，PDF121–129'
  source_quote: '最常用到的迭代器相应型别有五种'
  summary: '核对value_type、difference_type、pointer、reference、iterator_category。iterator_traits把class的nested typedef与原生T*、const T*统一起来；const T*的value_type仍为T，const属性落实在reference/pointer。这是原书接口模型，现代迭代器应另核规范。'
  tags: [traits, iterator]
  task_ids: [T04]

- id: p09
  title: 按能力而不是容器名字选择迭代器操作
  type: principle
  source_chapter: '§3.4.5，PDF129–136'
  source_quote: '但是可用并不代表最佳！'
  summary: 'Input与Output用途不同，不要画成单一继承链。Forward支持重复前向遍历，Bidirectional增加后退，RandomAccess增加跳跃、距离和有序比较。泛型代码只能使用其声明能力提供的操作。'
  tags: [iterator, concept]
  task_ids: [T04]

- id: p10
  title: advance与distance的代价来自迭代器能力
  type: calculation
  source_chapter: '§3.4.5，PDF130–140'
  source_quote: '最好能够在编译期就选择正确的版本。'
  summary: 'tag dispatch把类型信息转成重载选择。随机存取可直接+=n和last-first；一般输入迭代器须逐步前进，双向才能按负数后退。'
  inputs: '合法有效范围、迭代器类别、位移n'
  formula: 'RandomAccess advance/distance为O(1)；逐步advance为O(abs(n))；一般distance为O(N)'
  units: '迭代器操作次数，不是实际秒数'
  output: '派送分支、目标位置或距离、操作复杂度'
  missing_conditions: 'Input/Forward不接受任意负位移；跨越有效范围不合法。'
  tags: [dispatch, complexity]
  task_ids: [T04]

- id: p11
  title: 类型性质只在满足语义时许可快速分支
  type: principle
  source_chapter: '§3.7、§6.4.3，PDF140–148、358–364'
  source_quote: '双底线前缀词意指这是SGI STL内部所用的东西，不在STL标准规范之内。'
  summary: '区分iterator_traits与SGI __type_traits，后者记录默认构造、复制、赋值、析构、POD等性质。历史保守默认会令自定义类走逐元素分支；不能为了快而随意把带资源对象标成trivial，也不能把这些内部类型名当公共标准接口。'
  tags: [traits, lifetime, optimization]
  task_ids: [T02, T04, T11]

- id: p12
  title: vector大小容量与三个边界
  type: calculation
  source_chapter: '§4.2.4，PDF155'
  source_quote: '一个vector的容量永远大于或等于其大小。'
  summary: '以已构造范围[start,finish)与储存范围[start,end_of_storage)区分元素和备用储存。备用容量不允许直接当成已存在的元素读写。'
  inputs: '同一合法SGI vector储存内的start、finish、end_of_storage'
  formula: 'size=finish-start; capacity=end_of_storage-start; 0<=size<=capacity'
  units: '元素数；字节数另乘sizeof(T)'
  output: '大小、容量、备用容量及是否需扩容'
  missing_conditions: '空指针相减在现代实现中需另作处理；本式是原书状态模型，不是任意裸指针代码的许可。'
  tags: [vector, invariant]
  task_ids: [T05]

- id: p13
  title: vector扩容后原引用和迭代器不能继续沿用
  type: principle
  source_chapter: '§4.2.5–4.2.6，PDF156–163'
  source_quote: '重新配置、元素移动、释放原空间'
  summary: '先分是否仍有备用容量，再看插入点之后的元素数量。重新配置会搬迁已有元素并释放旧区间，原地址失效；无重新配置时仍应核对插入/擦除位置影响，不能以“地址没变”概括全部有效性。倍增是此SGI实现策略。'
  tags: [vector, invalidation]
  task_ids: [T05]

- id: p14
  title: list节点地址稳定不等于任意操作都无条件有效
  type: principle
  source_chapter: '§4.3.3、§4.3.6，PDF166–179'
  source_quote: '只有“指向被删除元素”的那个迭代器失效'
  summary: '链表插入通过改链接而非搬移全部对象；擦除使被删节点对应迭代器失效。splice/transfer须另外核对位置不落在待转移范围等先决条件；merge须先有序。查找某节点的代价与已知位置插入的代价分开。'
  tags: [list, invalidation, precondition]
  task_ids: [T06]

- id: p15
  title: list的排序要用成员sort
  type: principle
  source_chapter: '§4.3.6、§6.7.9，PDF179、428'
  source_quote: 'list不能使用STL算法sort()，必须使用自己的sort() member function'
  summary: '通用sort需要RandomAccessIterator，list仅双向；链表成员排序利用节点转移及merge，避免强行模拟随机访问。slist的单向遍历也不满足通用sort所需能力。'
  tags: [list, sort, iterator]
  task_ids: [T06, T13]

- id: p16
  title: SGI deque缓冲区元素数规则
  type: calculation
  source_chapter: '§4.4.2–4.4.3，PDF181–186'
  source_quote: '如果sz不小于512，传回1'
  summary: 'deque由map指针表串接多个缓冲区；逻辑随机访问不保证全体对象物理连续。512字节和可指定第三模板参数都是该历史实现细节。'
  inputs: 'BufSiz、元素字节数sz=sizeof(T)>0'
  formula: 'B=BufSiz!=0?BufSiz:(sz<512?floor(512/sz):1)'
  units: 'B为元素数，sz为byte'
  output: '单缓冲元素数、跨缓冲位置'
  missing_conditions: '不能把SGI第三模板参数写成现代std::deque的标准接口。'
  tags: [deque, sgi]
  task_ids: [T07]

- id: p17
  title: deque跨缓冲位移须处理负数向下取整
  type: calculation
  source_chapter: '§4.4.3，PDF186–187'
  source_quote: '目标位置不在同一缓冲区内'
  summary: '迭代器保留cur/first/last/node，移动跨边界时同时更新所属节点和缓冲区边界。负offset不能简单依赖C++向零截断除法，否则回跳位置错误。'
  inputs: '缓冲容量B、当前缓冲内offset和位移n，目标在有效范围内'
  formula: 'u=offset+n; node_delta=floor(u/B); new_offset=u-node_delta*B'
  units: '元素位置及节点偏移'
  output: '新node、新缓冲内偏移；0<=new_offset<B'
  missing_conditions: '公式为对源码分支的数学重写；越界及map迁移后的迭代器有效性另查。'
  tags: [deque, iterator, floor-division]
  task_ids: [T07]

- id: p18
  title: 容器配接器限制可见操作
  type: principle
  source_chapter: '§4.5–4.8，PDF204–222'
  source_quote: 'stack所有元素的进出都必须符合“先进后出”的条件'
  summary: 'stack、queue、priority_queue通过封装底层容器暴露规定的访问策略，不能从底层容器存在迭代器推出配接器也公开迭代器。替换底层容器应核对所调用操作是否受支持。'
  tags: [adapter, container]
  task_ids: [T08]

- id: p19
  title: 隐式堆下标约定不能混用
  type: calculation
  source_chapter: '§4.7.1–4.7.2，PDF210–217'
  source_quote: 'SGI STL提供的heap并未使用这一小技巧。'
  summary: '概念图的1-based数组与源码0-based数组分别记录。max-heap只保证父子次序，不保证整个数组排序；下标规则依赖约定。'
  inputs: '0-based数组、有效节点i、总长度N'
  formula: 'parent=(i-1)//2 (i>0); left=2*i+1; right=2*i+2；子节点索引须<N'
  units: '数组下标'
  output: '父子位置及堆性质检查结果'
  missing_conditions: '1-based图中则为i//2、2*i、2*i+1，不能串用。'
  tags: [heap, indexing]
  task_ids: [T08, T13]

- id: p20
  title: 堆算法不代替容器增删元素
  type: principle
  source_chapter: '§4.7.2，PDF212–219'
  source_quote: '最大元素只是被置放于底部容器的最尾端，尚未被取走。'
  summary: 'push_heap前新元素已追加到尾部，先前区间应为堆；pop_heap把堆顶放到尾端并恢复前N-1的堆，容器大小不变，要另pop_back。sort_heap要求堆前提并产出有序区间，不能在任意输入上直接调用。'
  tags: [heap, precondition]
  task_ids: [T08, T13]

- id: p21
  title: 红黑树四项不变量
  type: checklist
  source_chapter: '§5.2，PDF246–250'
  source_quote: '如果节点为红，其子节点必须为黑。'
  summary: '核对节点颜色、根黑、红节点无红孩子、每节点到NULL路径黑节点数相同；NULL视黑。新增红节点减少黑高度变化，但若父红就需变色和旋转；根须最终置黑。旋转还要保持搜索树中序关系。'
  tags: [rb-tree, invariant]
  task_ids: [T09]

- id: p22
  title: 搜索树性能依赖平衡而非仅搜索次序
  type: principle
  source_chapter: '§5.1，PDF239–246'
  source_quote: '造成搜寻效率低落的情况'
  summary: '搜索树次序决定从哪边查；平衡条件限制路径深度。不能把普通未平衡BST的所有输入都称为对数时间；递增插入的退化是必要反例。'
  tags: [tree, complexity]
  task_ids: [T09]

- id: p23
  title: 有序容器的key不可随意修改
  type: principle
  source_chapter: '§5.3–5.4，PDF271–282'
  source_quote: 'pair的第一元素被视为键值，第二元素被视为实值'
  summary: 'set值同时作为键，map节点是pair<const Key,T>；改变键会破坏既定排序位置。mapped value与key的可修改性不同。比较关系决定树中等价，不应默认所有场景都由operator==决定。'
  tags: [set, map, ordering]
  task_ids: [T09]

- id: p24
  title: 关联式容器优先使用其成员查找
  type: principle
  source_chapter: '§5.3–5.4，PDF275、280'
  source_quote: '因为STL算法find()只是循序搜寻'
  summary: 'generic find按迭代器逐一遍历，不了解树结构；成员find使用索引结构。先区分相等比较语义，再比较操作复杂度；不可宣称所有成员函数都更快。'
  tags: [lookup, complexity]
  task_ids: [T09, T12]

- id: p25
  title: 哈希容器重建必须重新计算bucket
  type: calculation
  source_chapter: '§5.7，PDF290–300'
  source_quote: '不可能只是原封不动地拷贝而已'
  summary: 'bucket数量变化时每个节点的归属可能改变。SGI separate chaining允许负载因子超过1；它选预置质数表并不意味所有开链哈希表都必须使用质数。'
  inputs: '元素哈希值h、正bucket数b、元素数N'
  formula: 'bucket=h mod b; load_factor=N/b'
  units: 'bucket下标、元素/桶'
  output: '各bucket节点分配、负载因子及重建后的遍历关系'
  missing_conditions: 'next_size文字说大于，lower_bound代码为不小于；边界另核，不将文字直接用作选质数公式。'
  tags: [hash, rehash]
  task_ids: [T10]

- id: p26
  title: 字符串的哈希与相等不能混成指针比较
  type: principle
  source_chapter: '§5.8–5.9，PDF311–316'
  source_quote: '不能直接以const char*做比较。'
  summary: 'C字符串按内容判断相等应逐字符比较；地址相等与文本内容相等不同。原书也说明看起来有序的一次哈希遍历不能证明容器排序。核对键相等与哈希所用对象的语义保持一致。'
  tags: [hash, equality, c-string]
  task_ids: [T10]

- id: p27
  title: 复制目标须有可赋值对象或显式插入配接器
  type: principle
  source_chapter: '§6.4.3，PDF353–364'
  source_quote: '它会为输出区间内的元素赋予新值，而不是产生新的元素。'
  summary: 'copy不自动增长普通目标容器；目标区间必须有足够有效对象，或使用插入迭代器把赋值改成插入。仅reserve不创建目标元素。书中的memmove快速路径不能赋予所有重叠copy调用通用合法性。'
  tags: [copy, lifetime, precondition]
  task_ids: [T11]

- id: p28
  title: 复制方向与重叠危险分别核验
  type: principle
  source_chapter: '§6.4.3–6.4.4，PDF353–367'
  source_quote: 'copy_backward所接受的迭代器必须是BidirectionalIterators'
  summary: '向左移动有效对象用正向复制，向右移动需从后向前复制；copy_backward的result是目标尾位置而非起点。先用合法范围检查方向，再解释源码分支。原书展示某些指针调用“碰巧正确”，不可升级为现代标准保证。'
  tags: [copy, overlap, direction]
  task_ids: [T11]

- id: p29
  title: 有序集合算法按出现次数而非容器名字计算
  type: calculation
  source_chapter: '§6.5，PDF367–375'
  source_quote: '必须是有序区间，元素值允许重复出现。'
  summary: '输入可以是有序vector/list/multiset，不要求名为set；hash_set无排序保证。两个区间必须使用同一比较关系排列，输出需足够储存。'
  inputs: '按相同比较关系排序的两个有效区间；某等价值的出现次数m,n'
  formula: 'union=max(m,n); intersection=min(m,n); difference=max(m-n,0); symmetric_difference=abs(m-n)'
  units: '每个等价类的元素个数'
  output: '有序结果及新的输出尾位置'
  missing_conditions: 'PDF367将数学set描述成允许重复，疑误；候选只保留多重集合算法的次数口径，不传播该数学定义。'
  tags: [set-algorithms, multiplicity]
  task_ids: [T12]

- id: p30
  title: remove与unique返回逻辑新尾而非改变容器大小
  type: principle
  source_chapter: '§6.7.1，PDF395–410'
  source_quote: '这一算法并不真正从容器中删除那些元素'
  summary: 'remove压缩保留元素并返回new_end；unique只压缩相邻等价项，保留原相对次序。需要容器大小同步时再以成员erase删尾部。尾部仍在容器内但不应作结果值依赖；全部去重是否可先排序取决于能否改变原顺序。'
  tags: [remove, unique, logical-end]
  task_ids: [T12]

- id: p31
  title: 二分查找边界与比较方向
  type: principle
  source_chapter: '§6.7.2–6.7.4、6.7.10，PDF414–418、439–441'
  source_quote: '指向第一个“不小于value”的元素。'
  summary: 'lower_bound返回首个!comp(element,value)，upper_bound返回首个comp(value,element)，equal_range合成等价范围；所有区间须满足对应顺序前提。返回last时不能解引用。无匹配时equal_range两端相等，但不必是容器end。'
  tags: [bounds, binary-search, ordering]
  task_ids: [T12]

- id: p32
  title: 二分比较次数不等于迭代器移动次数
  type: principle
  source_chapter: '§6.7.2–6.7.3，PDF414–417'
  source_quote: '版本一的forward_iterator版本'
  summary: '原书分别提供forward与random-access分支。前者用distance/advance寻找中点，比较次数虽呈对数，移动仍可能线性；后者可常数时间跳到中点。说明复杂度必须指明统计的是比较还是移动。'
  tags: [binary-search, complexity, iterator]
  task_ids: [T04, T12]

- id: p33
  title: partial_sort只保证前k项有序
  type: principle
  source_chapter: '§6.7.8，PDF425–427'
  source_quote: '不保证有任何特定顺序。'
  summary: 'partial_sort将k=middle-first个最小元素放入有序前缀，其余部分无内部顺序保证。原书用k元素max-heap保留当前最小候选，最后对前缀sort_heap。不能用它承诺稳定性或后半段排序。'
  tags: [partial-sort, heap]
  task_ids: [T13]

- id: p34
  title: SGI内省排序的深度预算与小区间阈值
  type: calculation
  source_chapter: '§6.7.9，PDF428–438'
  source_quote: '当分割行为有恶化为二次行为的倾向时，能够自我侦测，转而改用Heap Sort'
  summary: '大区间分割、深度预算耗尽转堆、小区间最终插入排序。阈值16是该SGI选择，原书也说最佳阈值依设备而异。不可声称所有标准库必须采用此算法或参数。'
  inputs: 'RandomAccess有效区间、N、比较策略'
  formula: '初始深度预算=2*floor(log2(N))；SGI小区间阈值=16；预算每分割递减'
  units: '分割层数、元素数'
  output: '分割/堆回退/插入排序分支及所维护有序性'
  missing_conditions: 'N=0须先处理；PDF436注释40的算例疑把floor(log2(40))或5*2写乱，应以代码与数学式核验。'
  tags: [introsort, complexity, sgi]
  task_ids: [T13]

- id: p35
  title: nth_element保证次序统计量但不保证两侧内部排序
  type: principle
  source_chapter: '§6.7.12，PDF449–450（已核页图）'
  source_quote: '两个子区间内的元素次序则无任何保证'
  summary: 'nth值应等价于完整排序后的相同位置；两侧允许重复等价值。原文括号“更精确地说是不大于”会错误排除相等元素，同页22重复例即显出冲突。候选保留不排序两侧的作用，分区精确断言须另核源码/规范，不能照错句执行。'
  tags: [nth-element, partition, source-conflict]
  task_ids: [T13]

- id: p36
  title: merge必须有两段同一关系下的有序输入
  type: principle
  source_chapter: '§6.7.1、6.7.11，PDF391–392、442–448'
  source_quote: 'merge()也必须以less为比较函数'
  summary: 'merge输出到另一处，inplace_merge处理同一范围内相邻的两个有序子范围；不能把“inplace”理解为绝不分配辅助缓冲。原书区分有缓冲和无缓冲处理，并说明稳定性。'
  tags: [merge, ordering, stability]
  task_ids: [T12, T13]

- id: p37
  title: accumulate按序累计不要求交换律或结合律
  type: principle
  source_chapter: '§6.3.2，PDF338'
  source_quote: '式中的二元操作符不必满足交换律和结合律'
  summary: '以init起步，依输入次序计算acc=op(acc,*first)。不能将此左折叠任意改成平行重排；init类型与操作参数、返回值需共同核对。原书版本与现代move/执行策略差异应另注。'
  tags: [numeric, accumulate, fold]
  task_ids: [T14]

- id: p38
  title: 函数对象的可调用性与旧式可配接性不同
  type: checklist
  source_chapter: '第7章，PDF453–457'
  source_quote: '仿函数的相应型别主要用来表现函数参数型别和传回值型别。'
  summary: 'operator()提供调用行为；历史unary_function/binary_function提供argument_type/result_type等typedef帮助旧配接器取型别。不能把继承这两个旧类写成所有现代可调用对象的必要条件。'
  tags: [functor, adaptable, historical-api]
  task_ids: [T14, T15]

- id: p39
  title: 插入迭代器将赋值变成容器插入
  type: principle
  source_chapter: '§8.3.1，PDF475–477'
  source_quote: '在insert iterators的operator=操作符中调用底层容器的push_front()或push_back()或insert()'
  summary: '目标输出迭代器通过绑定容器改变赋值语义；递增与解引用返回适合算法语法的对象而非真的移动已有元素位置。front_inserter要求底层有push_front，不适用于vector；普通inserter需跟随插入结果更新位置。'
  tags: [insert-iterator, output, adapter]
  task_ids: [T11, T15]

- id: p40
  title: 反向迭代器的base是所表示元素后一位置
  type: principle
  source_chapter: '§8.3.2，PDF477–482'
  source_quote: '对逆向迭代器取值，就是将“对应之正向迭代器”后退一格而后取值'
  summary: 'reverse_iterator保存current；base()返回current，而operator*复制current后--再解引用。因此rbegin对应end，rend对应begin；至少须双向迭代器。不能解引用rend，也不能直接把base当当前元素。'
  tags: [reverse-iterator, off-by-one]
  task_ids: [T15]

- id: p41
  title: 流输入迭代器构造时可能读取
  type: principle
  source_chapter: '§8.3.3，PDF482–487'
  source_quote: '请在绝对必要的时刻才定义你所需要'
  summary: '书中绑定输入流的构造函数调用read；如果先构造迭代器后打印提示，可能先阻塞等待输入。++触发下一次提取，读取失败改变结束标记；流迭代器不可按多遍随机访问对象使用。'
  tags: [stream-iterator, input, side-effect]
  task_ids: [T15]

- id: p42
  title: 参数绑定与函数合成的顺序必须写成表达式
  type: principle
  source_chapter: '§8.4，PDF488–499'
  source_quote: '将value绑定为第二个参数'
  summary: 'bind1st(op,v)产生op(v,x)，bind2nd(op,v)产生op(x,v)，not1/not2否定返回值；compose1等为SGI扩展。使用非交换运算核验参数顺序，而不是用加法例子掩盖交换错误。旧API不能直接保证现代编译器可用。'
  tags: [bind, composition, adapter]
  task_ids: [T14, T15]

- id: p43
  title: for_each不修改示例不能泛化为禁止修改元素
  type: principle
  source_chapter: '§8.1.3，PDF469–470（已核页图）；对照PDF73源码'
  source_quote: '注意，for_each()是nonmutating algorithm.元素内容不能更改'
  summary: '保留为来源冲突候选。此例compose1对参数按值算(v+2)*3但不赋回，故容器不变；同书for_each循环仅调用f(*first)，不能推出f永不通过引用修改对象。不得把该句编成active规则，需测试及外部原始规范复核。'
  tags: [for-each, source-conflict, function-object]
  task_ids: [T14, T15]
```

## 未解决的来源与识别问题

1. p05 / p07的数字和对齐公式已按OCR代码与相邻解释互核，但最终可执行卡还应核对PDF96、97、103页图，尤其128的边界、ceil与索引零基。
2. PDF295/297的next_size叙述“大于”与lower_bound代码存在等号差异；不自行补成标准哈希增长策略。
3. PDF361测试4的目标`list<int> ilistd()`疑为函数声明或OCR丢参，其调用目标是否为空需核页图；不照抄运行。
4. PDF367关于数学集合允许重复的表述疑误；与多重集合算法契约隔离。
5. PDF436深度算例的数字存在疑点；p34给出代码所用数学式，未把注释数值当核验结果。
6. PDF449重复键分区和PDF470 for_each警告已确认非OCR错误，应在三重验证时列出冲突证据与最小反例，不能在候选阶段把它们默默纠正成作者原话。
7. 所有短引文仅用于定位，不是完整算法规范。线程安全、现代失效规则、比较器的完整严格弱序公理和新旧接口移除时间，需要独立现代来源；本候选池不凭常识冒充书中完整证明。
