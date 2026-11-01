# 能力索引（完整版）

| capability_id | 标题 | 重要度 | 意图 | 关键词 | 能力卡 |
|---|---|---|---|---|---|
| cap.stl-houjie.source-reading | 从现象回到源码的版本化阅读 | high | 从现象回到源码的版本化阅读 | source-reading、阅读STL头文件、分析某库的内部调用、解释实现版本差异、source tracing、SGI源码。 | capabilities/source-reading.md |
| cap.stl-houjie.object-lifetime | 把原始储存与对象生存期分开核验 | critical | 把原始储存与对象生存期分开核验 | object-lifetime、allocator、placement new、未初始化内存、uninitialized_copy、fill、异常回滚或reserve后的对象数。 | capabilities/object-lifetime.md |
| cap.stl-houjie.pool-allocation | 推演SGI小区块分档与补池 | high | 推演SGI小区块分档与补池 | pool-allocation、SGI alloc、free list、内存池、ROUND_UP、128字节阈值或refill追踪。 | capabilities/pool-allocation.md |
| cap.stl-houjie.iterator-dispatch | 按迭代器能力检查traits与分派 | critical | 按迭代器能力检查traits与分派 | iterator-dispatch、iterator_traits、五种关联型别、tag dispatch、advance、distance、list能否sort或deque是否连续。 | capabilities/iterator-dispatch.md |
| cap.stl-houjie.vector-state | 以size/capacity和生存期推演vector | critical | 以size/capacity和生存期推演vector | vector-state、vector扩容、三指针、reserve、resize、insert、erase | capabilities/vector-state.md |
| cap.stl-houjie.linked-sequences | 按节点不变量追踪list和slist | high | 按节点不变量追踪list和slist | linked-sequences、list splice、transfer、哨兵、节点插入删除、list::sort、slist前驱与链接。 | capabilities/linked-sequences.md |
| cap.stl-houjie.deque-navigation | 推演deque跨缓冲位置 | high | 推演deque跨缓冲位置 | deque-navigation、deque的map、cur、first、last、node、分段连续 | capabilities/deque-navigation.md |
| cap.stl-houjie.heap-adapters | 保持heap不变量并区分配接器操作 | high | 保持heap不变量并区分配接器操作 | heap-adapters、push_heap、pop_heap、make_heap、sort_heap、priority_queue、stack | capabilities/heap-adapters.md |
| cap.stl-houjie.ordered-associative | 核对有序树、键与比较等价 | high | 核对有序树、键与比较等价 | ordered-associative、RB-tree、红黑插入修复、旋转、set、map、multiset | capabilities/ordered-associative.md |
| cap.stl-houjie.hash-table | 把哈希定位、相等与重散列分开 | high | 把哈希定位、相等与重散列分开 | hash-table、hashtable、bucket、碰撞链、rehash、resize、hash_map | capabilities/hash-table.md |
| cap.stl-houjie.copy-contract | 复制前核对目标生存期与重叠方向 | critical | 复制前核对目标生存期与重叠方向 | copy-contract、copy、copy_backward、重叠右移左移、reserve后复制、memmove优化或目标为空。 | capabilities/copy-contract.md |
| cap.stl-houjie.logical-end | 把remove和unique的逻辑尾转为容器操作 | critical | 把remove和unique的逻辑尾转为容器操作 | logical-end、erase-remove、remove没变size、unique没有全局去重、返回new_end后的尾部。 | capabilities/logical-end.md |
| cap.stl-houjie.ordered-ranges | 检查有序范围的边界与多重集合规则 | critical | 检查有序范围的边界与多重集合规则 | ordered-ranges、lower_bound、upper_bound、equal_range、binary_search、set_union、intersection | capabilities/ordered-ranges.md |
| cap.stl-houjie.sorting-selection | 按所需次序选择排序、选择与归并 | high | 按所需次序选择排序、选择与归并 | sorting-selection、sort、stable_sort、partial_sort、nth_element、inplace_merge、IntroSort深度回退 | capabilities/sorting-selection.md |
| cap.stl-houjie.numeric-functors | 跟踪数值折叠与函数对象状态 | high | 跟踪数值折叠与函数对象状态 | numeric-functors、accumulate、inner_product、partial_sum、adjacent_difference、初值、函数对象状态 | capabilities/numeric-functors.md |
| cap.stl-houjie.iterator-adapters | 把迭代器赋值、方向和流副作用写清 | high | 把迭代器赋值、方向和流副作用写清 | iterator-adapters、back_inserter、front_inserter、inserter、reverse_iterator::base、istream_iterator、ostream_iterator与copy。 | capabilities/iterator-adapters.md |
| cap.stl-houjie.callable-adapters | 将绑定和函数合成展开成表达式 | high | 将绑定和函数合成展开成表达式 | callable-adapters、bind1st、bind2nd、not1、compose、ptr_fun、mem_fun | capabilities/callable-adapters.md |
| cap.stl-houjie.range-reordering | 在合法范围内推演逆转、旋转和排列 | high | 在合法范围内推演逆转、旋转和排列 | range-reordering、reverse、rotate、next_permutation、prev_permutation、循环移动、字典序下一个排列与重复值。 | capabilities/range-reordering.md |
