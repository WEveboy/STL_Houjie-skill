# 输出评测机械断言判分 — stl-houjie

## E01

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.universal_growt expected=false; ✓json_equals:$.result.must_separate_s expected=true |
| new_skill | 2/2 | ✓json_equals:$.result.universal_growt expected=false; ✓json_equals:$.result.must_separate_s expected=true |

## E02

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.can_claim_verif expected=false; ✓json_equals:$.result.needs_reproduce expected=true |
| new_skill | 2/2 | ✓json_equals:$.result.can_claim_verif expected=false; ✓json_equals:$.result.needs_reproduce expected=true |

## E03

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.destroy_count expected=2; ✓json_equals:$.result.live_after_roll expected=0; ✓json_equals:$.result.deallocation_is expected=true |
| without_skill | 3/3 | ✓json_equals:$.result.destroy_count expected=2; ✓json_equals:$.result.live_after_roll expected=0; ✓json_equals:$.result.deallocation_is expected=true |

## E04

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.size_after_rese expected=0; ✓json_equals:$.result.copy_destinatio expected=false; ✓json_equals:$.result.reserve_constru expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.size_after_rese expected=0; ✓json_equals:$.result.copy_destinatio expected=false; ✓json_equals:$.result.reserve_constru expected=false |

## E05

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.level expected=2; ✓json_equals:$.result.class_bytes expected=128; ✓json_equals:$.result.free_list_index expected=15 |
| new_skill | 3/3 | ✓json_equals:$.result.level expected=2; ✓json_equals:$.result.class_bytes expected=128; ✓json_equals:$.result.free_list_index expected=15 |

## E06

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.level expected=1; ✓json_equals:$.result.zero_input_vali expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.level expected=1; ✓json_equals:$.result.zero_input_vali expected=false |

## E07

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.value_type expected="int"; ✓json_equals:$.result.reference expected="const int&"; ✓json_equals:$.result.list_std_sort_v expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.value_type expected="int"; ✓json_equals:$.result.reference expected="const int&"; ✓json_equals:$.result.list_std_sort_v expected=false |

## E08

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.negative_advanc expected=false; ✓json_equals:$.result.random_access_i expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.negative_advanc expected=false; ✓json_equals:$.result.random_access_i expected=false |

## E09

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.size expected=5; ✓json_equals:$.result.capacity expected=6; ✓json_equals:$.result.reallocated expected=true |
| without_skill | 2/3 | ✓json_equals:$.result.size expected=5; ✗json_equals:$.result.capacity expected=6; ✓json_equals:$.result.reallocated expected=true |

## E10

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.all_old_iterato expected=false; ✓json_equals:$.result.universal_doubl expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.all_old_iterato expected=false; ✓json_equals:$.result.universal_doubl expected=false |

## E11

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.A expected=[1]; ✓json_equals:$.result.B expected=[9, 2]; ✓json_equals:$.result.node_identity_p expected=true |
| new_skill | 3/3 | ✓json_equals:$.result.A expected=[1]; ✓json_equals:$.result.B expected=[9, 2]; ✓json_equals:$.result.node_identity_p expected=true |

## E12

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.ordinary_range_ expected=false; ✓json_equals:$.result.all_splice_call expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.ordinary_range_ expected=false; ✓json_equals:$.result.all_splice_call expected=false |

## E13

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.node_delta expected=-1; ✓json_equals:$.result.offset expected=6; ✓json_equals:$.result.needs_real_boun expected=true |
| new_skill | 3/3 | ✓json_equals:$.result.node_delta expected=-1; ✓json_equals:$.result.offset expected=6; ✓json_equals:$.result.needs_real_boun expected=true |

## E14

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.buffer_elements expected=32; ✓json_equals:$.result.is_32_bytes expected=false; ✓json_equals:$.result.modern_same_tem expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.buffer_elements expected=32; ✓json_equals:$.result.is_32_bytes expected=false; ✓json_equals:$.result.modern_same_tem expected=false |

## E15

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.size expected=4; ✓json_equals:$.result.heap_size expected=3; ✓json_equals:$.result.last_value expected=9 |
| new_skill | 3/3 | ✓json_equals:$.result.size expected=4; ✓json_equals:$.result.heap_size expected=3; ✓json_equals:$.result.last_value expected=9 |

## E16

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.empty_pop_valid expected=false; ✓json_equals:$.result.stack_public_ra expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.empty_pop_valid expected=false; ✓json_equals:$.result.stack_public_ra expected=false |

## E17

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 2/2 | ✓json_equals:$.result.rb_invariants_v expected=true; ✓json_equals:$.result.rotation_preser expected=true |
| without_skill | 2/2 | ✓json_equals:$.result.rb_invariants_v expected=true; ✓json_equals:$.result.rotation_preser expected=true |

## E18

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.comparison_equi expected=true; ✓json_equals:$.result.in_place_key_mu expected=false; ✓json_equals:$.result.bst_order_guara expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.comparison_equi expected=true; ✓json_equals:$.result.in_place_key_mu expected=false; ✓json_equals:$.result.bst_order_guara expected=false |

## E19

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.old_indices expected=[1, 1, 1]; ✓json_equals:$.result.new_indices expected=[1, 6, 4]; ✓json_equals:$.result.element_count expected=3 |
| without_skill | 3/3 | ✓json_equals:$.result.old_indices expected=[1, 1, 1]; ✓json_equals:$.result.new_indices expected=[1, 6, 4]; ✓json_equals:$.result.element_count expected=3 |

## E20

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 2/2 | ✓json_equals:$.result.pointer_equalit expected=false; ✓json_equals:$.result.one_traversal_p expected=false |
| without_skill | 2/2 | ✓json_equals:$.result.pointer_equalit expected=false; ✓json_equals:$.result.one_traversal_p expected=false |

## E21

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.valid expected=true; ✓json_equals:$.result.values expected=[1, 2, 1, 2, 3]; ✓json_equals:$.result.return_index expected=2 |
| new_skill | 3/3 | ✓json_equals:$.result.valid expected=true; ✓json_equals:$.result.values expected=[1, 2, 1, 2, 3]; ✓json_equals:$.result.return_index expected=2 |

## E22

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.valid expected=false; ✓json_equals:$.result.optimization_wa expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.valid expected=false; ✓json_equals:$.result.optimization_wa expected=false |

## E23

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 4/4 | ✓json_equals:$.result.valid_prefix expected=[1, 2, 3]; ✓json_equals:$.result.new_end expected=3; ✓json_equals:$.result.size_before_era expected=6; ✓json_equals:$.result.size_after_eras expected=3 |
| without_skill | 4/4 | ✓json_equals:$.result.valid_prefix expected=[1, 2, 3]; ✓json_equals:$.result.new_end expected=3; ✓json_equals:$.result.size_before_era expected=6; ✓json_equals:$.result.size_after_eras expected=3 |

## E24

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 4/4 | ✓json_equals:$.result.valid_prefix expected=[1, 2, 1]; ✓json_equals:$.result.size expected=5; ✓json_equals:$.result.global_deduplic expected=false; ✓json_equals:$.result.tail_values_gua expected=false |
| without_skill | 4/4 | ✓json_equals:$.result.valid_prefix expected=[1, 2, 1]; ✓json_equals:$.result.size expected=5; ✓json_equals:$.result.global_deduplic expected=false; ✓json_equals:$.result.tail_values_gua expected=false |

## E25

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.lower expected=1; ✓json_equals:$.result.upper expected=3; ✓json_equals:$.result.equal_range expected=[1, 3] |
| without_skill | 3/3 | ✓json_equals:$.result.lower expected=1; ✓json_equals:$.result.upper expected=3; ✓json_equals:$.result.equal_range expected=[1, 3] |

## E26

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.input_partition expected=false; ✓json_equals:$.result.list_movement_l expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.input_partition expected=false; ✓json_equals:$.result.list_movement_l expected=false |

## E27

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 2/2 | ✓json_equals:$.result.algorithm expected="partial_sort"; ✓json_equals:$.result.nth_sides_sorte expected=false |
| new_skill | 2/2 | ✓json_equals:$.result.algorithm expected="partial_sort"; ✓json_equals:$.result.nth_sides_sorte expected=false |

## E28

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 2/2 | ✓json_equals:$.result.strict_cross_pa expected=false; ✓json_equals:$.result.original_nth_va expected=false |
| without_skill | 2/2 | ✓json_equals:$.result.strict_cross_pa expected=false; ✓json_equals:$.result.original_nth_va expected=false |

## E29

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.accumulate expected=4; ✓json_equals:$.result.for_each_can_mu expected=true; ✓json_equals:$.result.values expected=[11, 12, 13] |
| new_skill | 3/3 | ✓json_equals:$.result.accumulate expected=4; ✓json_equals:$.result.for_each_can_mu expected=true; ✓json_equals:$.result.values expected=[11, 12, 13] |

## E30

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.empty_result expected=10; ✓json_equals:$.result.arbitrary_reord expected=false; ✓json_equals:$.result.for_each_return expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.empty_result expected=10; ✓json_equals:$.result.arbitrary_reord expected=false; ✓json_equals:$.result.for_each_return expected=false |

## E31

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.dereferenced expected=20; ✓json_equals:$.result.base_index expected=2; ✓json_equals:$.result.copied expected=[30, 20, 10] |
| without_skill | 3/3 | ✓json_equals:$.result.dereferenced expected=20; ✓json_equals:$.result.base_index expected=2; ✓json_equals:$.result.copied expected=[30, 20, 10] |

## E32

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.rend_dereferenc expected=false; ✓json_equals:$.result.vector_front_in expected=false; ✓json_equals:$.result.construction_gu expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.rend_dereferenc expected=false; ✓json_equals:$.result.vector_front_in expected=false; ✓json_equals:$.result.construction_gu expected=false |

## E33

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.bind_first expected=-7; ✓json_equals:$.result.bind_second expected=7; ✓json_equals:$.result.composed expected=18 |
| without_skill | 3/3 | ✓json_equals:$.result.bind_first expected=-7; ✓json_equals:$.result.bind_second expected=7; ✓json_equals:$.result.composed expected=18 |

## E34

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 2/2 | ✓json_equals:$.result.old_api_univers expected=false; ✓json_equals:$.result.equivalence_gua expected=false |
| without_skill | 2/2 | ✓json_equals:$.result.old_api_univers expected=false; ✓json_equals:$.result.equivalence_gua expected=false |

## E35

| 变体 | 断言通过 | 明细 |
|---|---|---|
| new_skill | 3/3 | ✓json_equals:$.result.rotated expected=[3, 4, 5, 1, 2]; ✓json_equals:$.result.next expected=[2, 1, 3]; ✓json_equals:$.result.has_next expected=true |
| without_skill | 3/3 | ✓json_equals:$.result.rotated expected=[3, 4, 5, 1, 2]; ✓json_equals:$.result.next expected=[2, 1, 3]; ✓json_equals:$.result.has_next expected=true |

## E36

| 变体 | 断言通过 | 明细 |
|---|---|---|
| without_skill | 3/3 | ✓json_equals:$.result.has_next expected=false; ✓json_equals:$.result.values expected=[1, 2, 3]; ✓json_equals:$.result.forward_reverse expected=false |
| new_skill | 3/3 | ✓json_equals:$.result.has_next expected=false; ✓json_equals:$.result.values expected=[1, 2, 3]; ✓json_equals:$.result.forward_reverse expected=false |

## 汇总（全部断言通过的 case 比例）

- new_skill: 36/36；完成 36/36（缺失计入分母）
- without_skill: 35/36；完成 36/36（缺失计入分母）

状态：COMPLETE

> 机械断言先于 LLM judge；A/B 盲评与分歧样本人工复核另行进行，此处不自动宣布非劣。
