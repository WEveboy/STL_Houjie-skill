# 框架与程序机制候选

提取器：framework-extractor，独立候选，不在此进行三重验证或晋级。输入为 BOOK_OVERVIEW.md 与八章 OCR，定位一律为 PDF 的 1-based 物理页。按八章逐页叙述及机制信号扫描，重点回读机制解释、分支和源代码注释；这不是全部代码行的人工审计。部分长段输出曾截断，已围绕候选补读；纯代码页、全部宏组合与每个重载仍需后续按选中能力核对。没有把 OCR 的可检索性当作来源准确性通过。

已目视核对 PDF184、333 的疑点：184 的“32/sizeof(int)=4”与同页20/8、次页8元素图注不一致，确在原扫描正文；333 的“尾端以外的任何位置”表述确在原扫描，不能据此许可任意越界指针。其余引文是 OCR 归一化的短句，最终 R 段使用前仍宜与页图逐条核对。

```yaml
- id: f01
  title: 六组件协作的依赖追踪
  type: framework
  source_chapter: "§1.2，PDF37–39；§6.2，PDF332–336"
  source_quote: "Container 通过 Allocator 取得数据储存空间"
  summary: |
    把一次STL调用分解为储存、访问、操作策略和接口改造四种职责。
    容器向配置器取得储存，算法经迭代器读取或写入元素。
    函数对象提供策略，配接器使接口能够接合。
    对未知源码先找到各职责的承担者，再追踪实际调用链。
    这能避免把模板实例化的所有细节误认成一个不可拆分的算法。
  inputs: [具体调用, 容器类型, 迭代器类型, 可调用策略, 实现版本]
  outputs: [组件依赖图, 调用链, 规格与实现的区分]
  steps: [标注六组件角色, 从公开接口向内追踪, 记录委托边与版本限定]
  missing_conditions: "未知库须另取源码；本书不提供所有现代实现的映射。"
  tags: [architecture, source-reading]
  task_ids: [T01]
- id: f02
  title: 从客户端观察回到实现的阅读闭环
  type: procedure
  source_chapter: "§4.2.5 PDF156；§4.3.5 PDF169；§4.4.5 PDF189；§6.4.3 PDF360–364"
  source_quote: "以客户端程序代码为引导，观察其所得结果并实证源代码，是一个良好的学习路径。"
  summary: |
    先用具体客户端调用确定观察问题，而非无目标地逐行读模板。
    选定size、capacity、节点或分派函数等可观察状态。
    沿源码解释每次状态变化，再用输出验证解释。
    需要给内部函数加输出时保留可恢复的副本。
    单个实现的观察结果仍须保留版本与类型前提。
  inputs: [最小客户端, 所研究的源码版本, 待观察状态]
  outputs: [状态序列, 对应源码分支, 预期与观测差异]
  steps: [确定观察点, 推演分支, 运行最小程序, 核对差异]
  missing_conditions: "书中旧工具链实验不能替代当前宿主的实跑。"
  tags: [source-reading, experiment]
  task_ids: [T01, T05, T07, T11]
- id: f03
  title: 储存配置与对象生灭的分阶段管理
  type: procedure
  source_chapter: "§2.2.2–2.2.3，PDF84–88"
  source_quote: "为了精密分工，STL allocator 决定将这两阶段操作区分开来。"
  summary: |
    将取得字节储存、构造对象、析构对象和归还储存分别记录。
    配置成功不表示对象已经存在，析构也不表示储存已归还。
    容器的备用容量依赖这种区分。
    通过construct/destroy与allocate/deallocate的对应关系审查生命周期。
    区间析构还按元素性质分派，不能对未知对象直接跳过析构。
  inputs: [储存范围, 已构造对象范围, 类型性质, 操作顺序]
  outputs: [生存期账本, 构造与销毁配对, 储存释放位置]
  steps: [标记原始储存, 标记构造成功范围, 在退出路径析构, 最后归还储存]
  missing_conditions: "书中若省略异常代码，完整异常保证需另核对真实实现。"
  tags: [lifetime, allocator]
  task_ids: [T02]
- id: f04
  title: SGI双层配置器的分流与回收
  type: procedure
  source_chapter: "§2.2.4–2.2.8，PDF88–99"
  source_quote: "内存需求量上调至 8 的倍数"
  summary: |
    对申请量先按阈值分流，再计算小区块所属档位。
    大区块交第一级配置器，小区块从相应自由链表弹出。
    链表为空时转到补充流程，释放小区块则放回所属链表。
    空闲块复用其内存保存下一个空闲块指针。
    该路径解释重复小额申请的管理方式，不是现代配置器的统一规范。
  inputs: [申请字节数, 自由链表状态, 分档参数]
  outputs: [所选配置级别, 分档与链表变化, 返回区块]
  steps: [比较128字节阈值, 按8字节上调, 弹出或补充, 按原大小回收]
  missing_conditions: "需保留n>0前提；多线程和特殊对齐不由该简化模型覆盖。"
  tags: [allocator, free-list]
  task_ids: [T03]
- id: f05
  title: refill与内存池的逐级求援
  type: procedure
  source_chapter: "§2.2.9–2.2.10，PDF101–105"
  source_quote: "如果水量不足以提供 20 个区块，但还足够供应一个以上的区块"
  summary: |
    自由链表缺货后，先尝试从内存池取得一批同档区块。
    池余量够整批则按批提供，只够部分则修订实际区块数。
    连一个都不够时把可用零头编入适当链表，再向heap求援。
    heap申请失败时检查较大空闲块，最后交给第一级内存不足机制。
    返回一个给客户，其余串成自由链表；这两个去向不能混为池余量。
  inputs: [区块大小, 期望区块数, 池边界, 各档空闲链表, heap申请结果]
  outputs: [实际供给数, 客户区块, 链表与池的新状态]
  steps: [计算池余量, 整批或部分供给, 编入零头, 补池或回退]
  missing_conditions: "递归、失败与线程路径必须按目标版本核对。"
  tags: [allocator, memory-pool]
  task_ids: [T03]
- id: f06
  title: 内存不足处理例程的重试协议
  type: troubleshooting
  source_chapter: "§2.2.5，PDF91–94"
  source_quote: "设计“内存不足处理例程”是客端的责任"
  summary: |
    第一级配置请求失败后，不直接假定所有内存都不可用。
    若客户设置了处理例程，先调用它，再重试配置。
    未设置处理例程则按该实现的异常或终止策略退出。
    要区分operator new使用的new-handler与SGI在malloc之上仿真的机制。
    重试是否有进展取决于处理例程，不能承诺一定成功。
  inputs: [失败的配置, 已设置的处理例程, 编译期异常配置]
  outputs: [重试轨迹, 成功区块或明确失败]
  steps: [判定是否有处理例程, 无则失败, 有则调用后重试]
  missing_conditions: "无法释放资源的处理例程可能无进展；现代实现须重新查证。"
  tags: [allocator, failure-handling]
  task_ids: [T02, T03]
- id: f07
  title: 未初始化区间构造与回滚
  type: procedure
  source_chapter: "§2.3，PDF106–114"
  source_quote: "必须能够将已产生的所有元素析构掉。"
  summary: |
    先确认输出范围是待构造的原始储存而非普通赋值目标。
    用输入区间或给定初值在目标位置构造对象。
    已成功构造的前缀必须可追踪，以便后续构造失败时回滚。
    原书以POD性质分派到批量或逐元素路径。
    源码节录明确省略异常处理时，只能提取回滚契约，不能说节录已实现完整保证。
  inputs: [原始储存, 输入范围或初值, 类型性质, 构造成功边界]
  outputs: [构造完成范围或清理后的失败状态]
  steps: [检查目标状态, 选择分派路径, 逐项更新成功边界, 失败则析构前缀]
  missing_conditions: "异常清理代码在书中多处省略；生成容器实现须补审。"
  tags: [lifetime, exception-safety]
  task_ids: [T02]
- id: f08
  title: 用traits统一类迭代器和原生指针
  type: procedure
  source_chapter: "§3.3–3.4，PDF121–128"
  source_quote: "好处是 traits 可以拥有特化版本"
  summary: |
    算法需要关联型别时，单靠表达式参数推导不总能取得返回类型。
    类迭代器可提供嵌套型别，原生指针却不能这样声明。
    加入traits间接层，普通情况提取嵌套型别，指针情况使用偏特化。
    指向const的指针还需区分value_type与引用的const性质。
    这样算法可保持同一查询接口，同时接纳两种迭代器表示。
  inputs: [迭代器类型, 所需关联型别, 指针或类的分类]
  outputs: [关联型别表, 采用的泛化或特化路径]
  steps: [列出所需型别, 查嵌套定义, 检查指针特化, 验证const分离]
  missing_conditions: "需按该时代迭代器约定解释；现代traits推导规则另查。"
  tags: [traits, generic-programming]
  task_ids: [T04]
- id: f09
  title: 迭代器能力驱动的tag dispatch
  type: procedure
  source_chapter: "§3.4.5，PDF129–140"
  source_quote: "最好能够在编译期就选择正确的版本。"
  summary: |
    把前进、后退和随机跳跃能力分为类别，不按具体容器名分派。
    traits提供类别型别，空标签对象作为重载选择参数。
    通用前进使用循环，双向类型可处理负距离，随机存取可直接跳跃。
    传入更强类别时，继承关系让较弱实现可作为回退。
    需同时说明功能可用和操作次数，不能把能编译当作最佳路径。
  inputs: [迭代器类别, 位移或距离任务, 可达范围]
  outputs: [所选重载, 位移结果, 操作次数量级]
  steps: [核对最低能力, 获取category, 重载决议, 推演目标状态]
  missing_conditions: "单向类型的负位移和不可达区间不能照常执行。"
  tags: [iterator, dispatch]
  task_ids: [T04]
- id: f10
  title: 类型性质驱动的安全优化分派
  type: procedure
  source_chapter: "§3.7，PDF140–149；§6.4.3，PDF358–364"
  source_quote: "在编译时期完成函数派送决定"
  summary: |
    从当前操作真正需要的性质出发，例如析构或赋值是否平凡。
    读取该实现记录的类型标签，选择保守路径或优化路径。
    用户自定义类型未登记时，旧SGI倾向采用保守分支。
    不得从类看起来简单推导出可以随意字节复制。
    原书的内部__type_traits与现代标准类型特征要分开使用。
  inputs: [操作种类, 类型性质证据, 该实现的traits]
  outputs: [分派路径, 优化前提, 保守回退]
  steps: [识别操作语义, 核对对应标签, 选择分支, 验证对象行为]
  missing_conditions: "不能按本书示例擅自向现代std命名空间添加任意特化。"
  tags: [traits, optimization]
  task_ids: [T02, T04, T11]
- id: f11
  title: vector三指针状态与扩容事务
  type: procedure
  source_chapter: "§4.2.4–4.2.6，PDF155–164"
  source_quote: "容量的扩张必须经历“重新配置、元素移动、释放原空间”等过程"
  summary: |
    用start、finish与end_of_storage区分有效对象和备用容量。
    尾插先判断是否有备用槽；有则构造并前移finish。
    无备用槽时申请更大连续储存，转移元素，再释放旧储存。
    插入多个元素另按尾段长度与插入量分支。
    把失效的旧地址与仍有效的新位置明确列出来。
  inputs: [size, capacity, 插入位置与数量, 旧对象范围]
  outputs: [新size与capacity, 构造和赋值范围, 失效说明]
  steps: [列三边界, 分流是否扩容, 分配构造或就地移动, 更新边界]
  missing_conditions: "扩容倍率是SGI实现策略；异常保证须审目标版本与元素类型。"
  tags: [vector, reallocation]
  task_ids: [T05]
- id: f12
  title: 环状list的哨兵与节点接合
  type: procedure
  source_chapter: "§4.3，PDF166–179"
  source_quote: "这个操作为其它的复杂操作如 splice, sort, merge 等奠定良好的基础。"
  summary: |
    把list对象、节点和节点中的值分开，空白哨兵统一首尾边界。
    迭代器沿prev/next移动，而不是把节点地址做数组算术。
    插入先构造节点，再更新邻接边；删除先摘链再析构归还。
    transfer以重连边界搬移一段节点，splice等公开操作委托它完成。
    输出应同时保留节点身份与元素顺序，区分移动节点和复制元素。
  inputs: [节点及邻接关系, 哨兵, 插入点, 迁移半开范围]
  outputs: [新链接图, 元素顺序, 仍有效的节点身份]
  steps: [定位边界, 保存邻接点, 执行重连, 核对双向环与哨兵]
  missing_conditions: "自接合重叠及跨容器条件需按具体公开重载逐项核对。"
  tags: [list, splice]
  task_ids: [T06]
- id: f13
  title: 分段deque的逻辑位置映射
  type: procedure
  source_chapter: "§4.4.2–4.4.4，PDF181–188"
  source_quote: "维持其“整体连续”假象的任务，落在了迭代器的身上。"
  summary: |
    将逻辑连续序列映射为map中的缓冲区指针与区内位置。
    迭代器保存cur、first、last和node，使跨缓冲移动可重设边界。
    前进或后退到边缘时切换缓冲区，随机位移需计算跨越的区数。
    map本身可能扩容，它不同于元素储存，也不是关联容器map。
    字节数、元素数和区内偏移必须分别记单位。
  inputs: [缓冲区元素数, map位置, 区内偏移, 位移]
  outputs: [目标区与偏移, 迭代器四字段, 跨区轨迹]
  steps: [统一容量单位, 计算逻辑偏移, 切换node, 重设区间边界]
  missing_conditions: "PDF184有原书局部算式不一致，应据明确sizeof前提重算，不照抄4。"
  tags: [deque, iterator]
  task_ids: [T07]
- id: f14
  title: deque端点增长与map扩充的分离
  type: procedure
  source_chapter: "§4.4.5–4.4.6，PDF189–203"
  source_quote: "先配置一整块新的缓冲区，再设妥新元素内容，然后更改迭代器 finish 的状态"
  summary: |
    端点插入先检查当前缓冲区是否仍有可用位置。
    辅助路径先保证map能容纳新增缓冲区，再配置缓冲区并构造元素。
    端点删除在合适条件下释放空缓冲区，清空仍保留初始布局所需缓冲区。
    中间插入和删除要分析搬动方向与两侧距离。
    不能把不搬整个元素区误解为永远没有内部管理结构重配置。
  inputs: [端点状态, map可用槽, 缓冲区状态, 操作位置]
  outputs: [缓冲区与map变化, start和finish状态, 元素移动范围]
  steps: [判断普通或辅助路径, 保证map空间, 构造或销毁, 更新端点]
  missing_conditions: "现代deque失效规则不能仅从本书简化状态推断。"
  tags: [deque, storage]
  task_ids: [T07]
- id: f15
  title: 用底层容器接口构成受限容器
  type: framework
  source_chapter: "§4.5–4.6 PDF204–208；§4.8 PDF220–222；§8.2 PDF474"
  source_quote: "修改某物接口，形成另一种风貌"
  summary: |
    先确定所需访问纪律，再选择能提供必要操作的底层容器。
    stack暴露栈顶操作，queue分离入队和出队两端。
    priority_queue再加入heap维护，而不是简单更名一个顺序容器。
    检查每个公开操作如何委托到底层及维护规则。
    不暴露任意遍历与修改有助于维持其访问纪律。
  inputs: [访问纪律, 底层容器操作集合, 比较策略]
  outputs: [公开到内部操作映射, 适用底层容器, 不变量]
  steps: [列公开契约, 核对底层接口, 追踪委托, 验证访问顺序]
  missing_conditions: "不是任意容器都满足底层操作要求。"
  tags: [adapter, container]
  task_ids: [T08]
- id: f16
  title: 隐式heap的上溯与下溯
  type: procedure
  source_chapter: "§4.7，PDF209–218"
  source_quote: "新加人的元素一定要放在最下一层作为叶节点"
  summary: |
    使用数组位置表达完全二叉树，以比较策略定义父子优先关系。
    push_heap假设新元素已经置于末尾，通过上溯恢复堆序。
    pop_heap把根放到范围末尾，再调整剩余前缀。
    make_heap从内部节点逐次调整；sort_heap反复缩小有效堆范围。
    堆操作和容器长度变化分开，pop_heap本身不删除元素。
  inputs: [随机存取区间, 比较器, 已有堆与末元素状态]
  outputs: [有效堆范围, 数组状态, 取出的末尾元素]
  steps: [核对前置堆序, 选择上溯或下溯, 更新洞与父子位置, 核对堆序]
  missing_conditions: "图解1-based索引与SGI代码0-based索引不能混算。"
  tags: [heap, priority-queue]
  task_ids: [T08, T13]
- id: f17
  title: 二叉搜索树旋转与红黑插入修复
  type: procedure
  source_chapter: "§5.1–5.2，PDF239–270"
  source_quote: "当新节点根据二叉搜索树的规则到达其插入点"
  summary: |
    先按键比较找到插入位置，再检查颜色与黑高约束。
    依父、伯父和祖父关系选择变色、单旋或双旋。
    旋转必须保持中序关系，并更新父链和根连接。
    SGI额外使用header保存根、最小和最大节点的入口。
    修复结束后同时核对查找顺序、颜色约束和header，不只画出似乎平衡的树。
  inputs: [键比较器, 树节点与颜色, 插入键, header状态]
  outputs: [插入路径, 修复轨迹, 中序与黑高检查]
  steps: [搜索插入点, 放入红节点, 按亲属颜色修复, 更新根与header]
  missing_conditions: "原书本节主要讲插入与查找；完整红黑删除修复不可由此假装完成。"
  tags: [rb-tree, invariant]
  task_ids: [T09]
- id: f18
  title: set与map的键提取和唯一性封装
  type: procedure
  source_chapter: "§5.3–5.6，PDF271–284"
  source_quote: "map 元素的键值关系到 map 元素的排列规则。"
  summary: |
    先区别整个存储值与参与排序的键。
    set以值为键，map从pair中提取键，映射值可独立变化。
    unique与equal两种插入入口分别表达键唯一和允许重复。
    公开容器主要委托树接口，但不能向外开放破坏键序的任意修改。
    分析调用时要区分查找、插入和下标访问是否会产生新节点。
  inputs: [值类型, 键提取方式, 比较器, 唯一性要求]
  outputs: [键值映射, 实际树入口, 是否新增节点]
  steps: [识别键与值, 选唯一或重复插入, 追踪委托, 核对键序]
  missing_conditions: "不得将必须用红黑树写成标准的唯一允许实现。"
  tags: [map, set, key-policy]
  task_ids: [T09]
- id: f19
  title: 开链hashtable的定位与重散列
  type: procedure
  source_chapter: "§5.7–5.11，PDF285–322"
  source_quote: "不可能只是原封不动地拷贝而已"
  summary: |
    从值提取键，经hash再按bucket数取模决定链表位置。
    在目标链中用相等策略查找，唯一插入与重复插入走不同入口。
    容量策略要求重建时，重新计算每个节点在新桶数下的位置。
    迭代器先沿链前进，链尾后再扫描后继bucket。
    桶遍历顺序与输入偶然吻合不能证明有序。
  inputs: [键提取器, hash, 相等策略, bucket数, 节点和插入量]
  outputs: [桶链状态, 负载, 重散列映射, 遍历次序]
  steps: [取键并定位, 核对链上相等, 判断扩桶, 重接节点到新桶]
  missing_conditions: "素数表与阈值为SGI策略；不能把旧hash_map直接当现代unordered_map规范。"
  tags: [hashtable, rehash]
  task_ids: [T10]
- id: f20
  title: 从具体数组查找到泛型算法
  type: framework
  source_chapter: "§6.1.5–6.2，PDF330–336"
  source_quote: "把操作对象的型别加以抽象化"
  summary: |
    先识别算法真正使用的操作，而不是它最初服务的容器。
    将数组大小改写为首尾范围，将指针改写为支持所需操作的迭代器。
    失败以last表示，从而跨容器保持一致的停止语义。
    参数名表达算法要求的最低迭代器类别。
    泛化应保留可达性和有效范围前提，不能由模板替调用者保证。
  inputs: [具体算法, 操作清单, 输入区间, 元素比较]
  outputs: [最低能力契约, 泛型接口, 未找到的返回语义]
  steps: [列实际操作, 抽象类型与范围, 确定最低类别, 核对空范围与未找到]
  missing_conditions: "PDF333关于任意尾外指针的表述过宽，采用明确one-past示例边界。"
  tags: [generic-programming, algorithm]
  task_ids: [T01, T04, T12]
- id: f21
  title: 数值算法的有序折叠与状态传递
  type: procedure
  source_chapter: "§6.3，PDF337–343"
  source_quote: "所有运算行为的顺序都有明确设定"
  summary: |
    accumulate从初值开始按序合并，不能擅自交换或重排计算。
    inner_product先计算成对操作，再累积到状态。
    partial_sum输出前缀状态，adjacent_difference输出相邻变化。
    分开检查空范围、输出空间和允许就地执行的情况。
    通过非交换运算的小例子可暴露错误的折叠方向。
  inputs: [输入区间, 初值, 二元操作, 输出范围]
  outputs: [每步累积状态, 输出序列, 返回迭代器]
  steps: [确定初值和操作顺序, 逐元素推进, 写出状态, 核对空输入]
  missing_conditions: "浮点与自定义操作不可仅凭加法直觉重排；power为SGI扩展。"
  tags: [numeric, fold]
  task_ids: [T14]
- id: f22
  title: copy的生命周期、重叠与分派审查
  type: procedure
  source_chapter: "§6.4.3–6.4.4，PDF353–366"
  source_quote: "它会为输出区间内的元素赋予新值，而不是产生新的元素。"
  summary: |
    先确认目标已有可赋值对象或使用能把赋值转为插入的输出配接器。
    核对源与目标范围、容量和前进或后退方向的重叠前提。
    再追踪类迭代器、原生指针和trivial赋值标签的分派。
    类型优化与合法调用条件是两层问题。
    某次memmove路径看似成功不能反向证明越过契约的copy调用合法。
  inputs: [源范围, 目标起点或尾点, 目标对象状态, 类型与迭代器]
  outputs: [合法性判断, 正确方向或插入配接器, 分派路径]
  steps: [检查目标对象, 标重叠关系, 选copy或copy_backward, 再分析优化]
  missing_conditions: "现代接口的精确重叠禁区及类型要求需另核对标准来源。"
  tags: [copy, overlap, lifetime]
  task_ids: [T11]
- id: f23
  title: 有序多重集合的双游标合并
  type: procedure
  source_chapter: "§6.5，PDF367–376"
  source_quote: "必须是有序区间"
  summary: |
    先确认两输入使用同一排序准则，再用双游标比较当前元素。
    按并、交、差、对称差决定写出哪边并推进哪边。
    相同值可重复，四种运算分别有不同的重数结果。
    输出可以是普通可写区间，也可经插入迭代器增长。
    不能因为容器名字带set就假定hash容器满足输入条件。
  inputs: [两个有序范围, 同一比较准则, 集合运算种类, 输出迭代器]
  outputs: [结果序列, 重数规则, 双游标轨迹]
  steps: [核对有序性, 逐步比较推进, 处理剩余尾段, 核对重复计数]
  missing_conditions: "原书把允许重复的广义集合与数学集合混说，交付应明确多重集合语义。"
  tags: [set-algorithm, merge]
  task_ids: [T12]
- id: f24
  title: remove与unique的逻辑压缩后物理删除
  type: procedure
  source_chapter: "§6.7.1，PDF395–396、409–413"
  source_quote: "容器大小并未改变"
  summary: |
    remove把要保留的元素稳定压到前缀，返回新逻辑尾界。
    unique只压缩相邻重复组，不是自动全局去重。
    两者不自行缩小容器，若需物理删除再调用容器的erase。
    输出解释应只依赖新逻辑区间，不把尾段残余值当稳定结果。
    若要求全局去重而又保留原序，不能无条件先排序。
  inputs: [可写前向范围, 删除谓词或等价判断, 是否要求物理缩容]
  outputs: [有效前缀, 新尾界, 后续erase范围]
  steps: [明确筛选或相邻去重, 推演保留前缀, 返回new_end, 必要时erase]
  missing_conditions: "尾段内容不作依赖；不能把算法remove与list成员remove混淆。"
  tags: [remove, unique, erase]
  task_ids: [T12]
- id: f25
  title: reverse与rotate的能力分支
  type: procedure
  source_chapter: "§6.7.1，PDF399–404"
  source_quote: "rotate() 可以交换两个长度不同的区间"
  summary: |
    reverse通过双向遍历交换端点，随机存取另有可选实现。
    rotate把两个相邻半开范围换位，保持各段内部次序。
    按前向、双向和随机存取能力采用不同分派算法。
    middle作为分界而非待交换的单个值，必须明确它属于同一范围。
    用不等长两段测试可区分rotate与swap_ranges。
  inputs: [同一范围的first/middle/last, 迭代器类别]
  outputs: [重排结果, 分派路径, 空段处理]
  steps: [核对分界, 选择类别路径, 推演元素交换, 验证两段次序]
  missing_conditions: "原书旧版rotate接口与现代返回值差异需另查。"
  tags: [rotate, iterator]
  task_ids: [T12, T13]
- id: f26
  title: 二分边界定位与比较等价
  type: procedure
  source_chapter: "§6.7.2–6.7.4 PDF414–418；§6.7.10 PDF439–441"
  source_quote: "在不破坏排序状态的原则下，可插入 value 的第一个位置"
  summary: |
    lower_bound与upper_bound寻找两种不同的插入边界。
    binary_search在下界位置检查比较意义上的等价，equal_range返回两边界。
    每轮依据中间元素缩小候选区间，并区分空范围和不存在的目标。
    对前向迭代器需要distance/advance，对随机存取可直接定位。
    比较次数与移动次数要分别分析，不能把二分字样自动解释为所有成本对数。
  inputs: [符合比较准则的有序范围, 目标值, 比较器, 迭代器类别]
  outputs: [下界上界, 是否存在, 比较与移动轨迹]
  steps: [核对有序前提, 确定边界谓词, 反复缩小范围, 检查等价与返回值]
  missing_conditions: "本书用有序范围解释；现代更精细partitioned前提应另注明。"
  tags: [binary-search, bounds]
  task_ids: [T12]
- id: f27
  title: 字典序相邻排列的局部修复
  type: procedure
  source_chapter: "§6.7.5–6.7.6，PDF419–421"
  source_quote: "再将之后的所有元素颠倒排列"
  summary: |
    从右向左寻找可以增加的枢轴，尾段此时已处于极值顺序。
    从尾段选择刚好更大的候选交换，再逆转尾段得到最小后缀。
    prev_permutation使用相反比较方向。
    若找不到枢轴，说明已到字典序终点，并按实现处理整个范围。
    返回bool与变换后的序列须一起解释，不能只报是否存在。
  inputs: [双向可写范围, 比较准则]
  outputs: [相邻排列, bool状态, 枢轴与后缀轨迹]
  steps: [找枢轴, 找交换候选, 交换, 逆转尾段或处理终点]
  missing_conditions: "须核对重复元素和终点分支；不把排列误称为任意组合。"
  tags: [permutation, sequence]
  task_ids: [T13]
- id: f28
  title: partial_sort的有界候选堆
  type: procedure
  source_chapter: "§6.7.8，PDF425–427"
  source_quote: "首先界定出区间 [first,middle)，并把它组织成一个 max-heap"
  summary: |
    需要前k个最小元素有序时，只维护k个候选而不排序全体。
    先把候选区构成最大堆，使当前候选中的最大值便于替换。
    扫描其余元素，遇更小者替换堆顶并修复。
    最后把候选堆排序得到有序前缀。
    剩余尾段的内部顺序不在该任务保证中。
  inputs: [随机存取范围, middle或k, 比较器]
  outputs: [有序前k项, 候选替换轨迹, 未保证尾段说明]
  steps: [建立k项堆, 扫描尾部, 必要时替换修复, 排序候选堆]
  missing_conditions: "k=0、k=n及copy版本输出容量需分开核对。"
  tags: [partial-sort, heap]
  task_ids: [T13]
- id: f29
  title: SGI sort的IntroSort回退控制
  type: procedure
  source_chapter: "§6.7.9，PDF428–438"
  source_quote: "转而改用 Heap Sort"
  summary: |
    大范围采用三点中值枢轴与分割，减少问题规模。
    同时维护深度预算，遇退化风险时改用堆排序路径。
    小范围停止继续分割，最后以插入排序完成整理。
    解释unguarded分支时必须指出已成立的边界保障，而非删除检查本身更快。
    阈值与具体混合实现必须限定为所读SGI版本。
  inputs: [可写随机存取范围, 比较器, 阈值, 深度预算]
  outputs: [分割树, 回退位置, 最终有序结果, 复杂度分支]
  steps: [核对迭代器能力, 三点选枢轴分割, 递减深度预算, 堆回退或插入收尾]
  missing_conditions: "不能向list调用通用sort；原书各版本算法差异需保留。"
  tags: [introsort, complexity]
  task_ids: [T13]
- id: f30
  title: inplace_merge的缓冲区自适应归并
  type: procedure
  source_chapter: "§6.7.11、6.7.13，PDF442–448、451–452"
  source_quote: "在没有缓冲区或缓冲区不足的情况下，也可以运作。"
  summary: |
    先确认相邻的两个子范围各自有序。
    缓冲区足够容纳其中一段时，借副本进行稳定归并。
    不足时选择切分点、旋转中间两段，再递归合并。
    方向选择关系到覆盖风险和稳定性，需要保留等价元素来自哪段。
    Merge Sort可把此归并作为分治后重新组合的步骤。
  inputs: [相邻有序子范围, 比较器, 可用缓冲区大小]
  outputs: [归并序列, 稳定性轨迹, 缓冲与旋转分支]
  steps: [核对两段有序, 选可容纳段, 缓冲归并或切分旋转, 递归核对]
  missing_conditions: "书中为篇幅聚焦部分实现；未展示分支须回源码，不能宣称全分支已证。"
  tags: [merge, buffer]
  task_ids: [T13]
- id: f31
  title: nth_element的单侧分割选择
  type: procedure
  source_chapter: "§6.7.12，PDF449–450"
  source_quote: "但对于两个子区间内的元素次序则无任何保证"
  summary: |
    目标是某个秩位置的值与完整排序一致，而不是排序前缀。
    分割后根据nth落在哪一侧，只继续处理该侧。
    待处理区间足够小时用插入排序收尾。
    核对nth两侧的比较关系与多重集合保持，不能要求同一个具体排列。
    与partial_sort的区别在于是否要求前缀内部有序。
  inputs: [随机存取范围, nth位置, 比较器]
  outputs: [目标秩值, 两侧分区, 未保证的内部次序]
  steps: [核对nth范围, 分割, 保留目标侧, 小范围收尾并检验后置条件]
  missing_conditions: "书中“更精确地说是不大于”等措辞需谨慎，使用双侧比较定义而非误抄。"
  tags: [selection, nth-element]
  task_ids: [T13]
- id: f32
  title: 可调用对象的策略注入
  type: framework
  source_chapter: "第7章，PDF453–464"
  source_quote: "它扮演一种“策略”角色"
  summary: |
    保持算法遍历和数据移动流程，使用可调用对象替换局部操作。
    区分算法需要的一元谓词、二元比较和二元累积操作。
    函数对象通过operator()暴露行为，也可携带状态。
    旧配接器通过关联型别了解参数和返回型别。
    直接可调用与能够被旧式配接器包装不是同一个条件。
  inputs: [算法的调用签名, 目标策略, 状态与复制语义]
  outputs: [可调用对象契约, 调用轨迹, 是否能被所选配接器使用]
  steps: [列算法调用形式, 对齐操作数与返回值, 接入对象, 核对状态副本]
  missing_conditions: "不把继承unary_function等历史约定推广成现代可调用对象的必须条件。"
  tags: [functor, policy]
  task_ids: [T14]
- id: f33
  title: 插入迭代器把赋值转成容器增长
  type: procedure
  source_chapter: "§8.1.2、8.3.1，PDF466、475–477"
  source_quote: "将一般迭代器的赋值操作转变为插入操作"
  summary: |
    普通输出迭代器的赋值需要有效目标对象，插入迭代器则把赋值改为容器操作。
    back、front与position三种方式分别映射到不同插入入口。
    算法仍按输出迭代器接口推进，实际增长由配接器处理。
    前端插入可能逆转到达次序，位置插入还需正确维护后继插入点。
    目标容器必须真正具备相应的底层插入操作。
  inputs: [输入序列, 目标容器, 插入方向或位置]
  outputs: [增长后容器, 插入次序, 适用性判断]
  steps: [选择插入策略, 包装容器, 追踪赋值到插入映射, 核对最终顺序]
  missing_conditions: "不能对不具push_front的容器使用front插入器。"
  tags: [adapter, output-iterator]
  task_ids: [T11, T15]
- id: f34
  title: 逆向迭代器的半开边界转换
  type: procedure
  source_chapter: "§8.3.2，PDF477–482"
  source_quote: "其逻辑位置改变了"
  summary: |
    正向范围反转后，反向起点保存正向end，反向终点保存正向begin。
    解引用反向迭代器需要取base前一个元素。
    递增反向迭代器则后退其底层迭代器。
    比较、差和下标的方向也随之转换，不能只倒置循环条件。
    这种偏移保证半开区间反向后仍可沿用同一算法。
  inputs: [双向范围, base位置, 反向位移]
  outputs: [对应元素, 反向范围, base与逻辑位置对照]
  steps: [交换首尾角色, 标出base与前一元素, 反向推进, 核对空范围]
  missing_conditions: "单向迭代器不能直接逆向包装；rend不可解引用。"
  tags: [reverse-iterator, range]
  task_ids: [T15]
- id: f35
  title: 流迭代器的惰性读取与输出转发
  type: procedure
  source_chapter: "§8.3.3，PDF482–487"
  source_quote: "只要客户端定义一个 istream_iterator 并绑定"
  summary: |
    输入迭代器维护流与缓存值，绑定时即可能发生第一次读取。
    解引用取得当前缓存，递增触发后续提取。
    默认构造的输入迭代器用作流结束标记，失败流决定终止。
    输出迭代器把赋值转发为流插入，递增无需移动存储位置。
    将这些行为展开后，copy能复用同一循环连接流与容器。
  inputs: [流状态, 元素类型, 结束标记, 输出分隔符]
  outputs: [消费顺序, 停止位置, 写出的文本或容器]
  steps: [确定绑定与首读, 追踪解引用和递增, 检查流结束, 转发输出]
  missing_conditions: "输入流不是多趟范围；交互流绑定时机影响阻塞行为。"
  tags: [stream-iterator, io]
  task_ids: [T15]
- id: f36
  title: 函数配接器的存储与延迟组合
  type: procedure
  source_chapter: "§8.1.3、8.4，PDF468–473、488–500"
  source_quote: "内藏了一个 member object"
  summary: |
    配接器在构造时保存被包装操作及绑定参数，而不是立即完成所有运算。
    算法日后调用operator()，才执行绑定、否定或复合函数。
    原生函数指针的包装用于补齐旧式可配接接口，成员函数包装还需区别对象和指针。
    画出内外operator()调用链，可检验绑定的是哪一参数、否定的是哪一结果。
    同时核对对象副本和成员函数接收者，不能只看表面表达式。
  inputs: [内层操作, 绑定参数, 组合次序, 调用对象或指针]
  outputs: [等价展开表达式, 调用链, 类型与状态契约]
  steps: [列保存成员, 展开外层调用, 按参数位传递, 核对最终返回]
  missing_conditions: "compose为SGI扩展；旧bind/ptr_fun/mem_fun接口不是现代可移植性保证。"
  tags: [function-adapter, composition]
  task_ids: [T14, T15]
```

## 范围和待核验

- 正文八章均纳入逐页机制信号扫描；候选解释主要回读页：37–39、84–114、116–141、152–203、204–218、220–234、239–270、271–284、285–322、330–343、353–376、395–420、425–452、453–500。历史授权介绍、全部编译器组态宏、纯源码重载行没有逐行核验，不作为“完整源码审计”声称。
- 原书内存基本工具的部分节录省略异常处理；后续不能直接复制这些节录作为生产级容器。
- 第4章list::sort的具体64计数器过程、红黑树删除修复、算法家族各个重载的全部实现细节，需要按最终能力范围补读；没有在当前候选中虚构独立完整步骤。
- f17是“插入与不变量”候选，不包含原文没有详细讲解的完整删除修复。f30区分书中说明的自适应机制与未完整展示的源码分支。
- f11关于“所有旧迭代器失效”限定于重配置，不能扩展到每一次push_back；f14不自行推导现代deque完整失效规则。
- f22需要把书中实现观察与标准契约分开：memmove路径对某些重叠例子返回预期结果，不使违反接口前置条件的调用合法。
- 暂未把算法表每一条函数各立一张卡；对可共用的“需求→最低迭代能力→范围/对象前提→返回与状态”分析框架由f20承载；要对某个未展开算法交付完整执行器，仍须定位其正文和源码。
