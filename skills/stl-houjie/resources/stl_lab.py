"""Bounded, original teaching models, not a standard-library emulator.

Python 3.10+, standard library only. JSON input and output; no dynamic code.
"""
import json
import sys
from pathlib import Path
from stl_extensions import OPERATIONS as EXTRA_OPERATIONS
import experiment_audit

MAX_ITEMS = 256
MAX_STORAGE = 4096
MAX_INT = 1_000_000


def integer(value, name, low=-MAX_INT, high=MAX_INT):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{name} must be an integer in [{low},{high}]')
    return value


def fields(value, required, optional=()):
    if type(value) is not dict:
        raise ValueError('expected an object')
    missing = set(required) - set(value)
    extra = set(value) - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f'missing fields: {sorted(missing)}; unknown fields: {sorted(extra)}')


def integers(value, name='values'):
    if type(value) is not list or len(value) > MAX_ITEMS:
        raise ValueError(f'{name} must be an array of at most {MAX_ITEMS} integers')
    return [integer(x, f'{name}[{i}]') for i, x in enumerate(value)]


def max_heap(values):
    return all(values[(i - 1) // 2] >= values[i] for i in range(1, len(values)))


def pool_class(data):
    fields(data, ['op', 'bytes'])
    n = integer(data['bytes'], 'bytes', 1)
    if n > 128:
        return {'level': 1, 'requested_bytes': n, 'class_bytes': None, 'free_list_index': None}
    rounded = ((n + 7) // 8) * 8
    return {'level': 2, 'requested_bytes': n, 'class_bytes': rounded,
            'free_list_index': rounded // 8 - 1}


def vector_growth(data):
    fields(data, ['op', 'size', 'capacity', 'insertions'])
    size = integer(data['size'], 'size', 0, MAX_STORAGE)
    capacity = integer(data['capacity'], 'capacity', size, MAX_STORAGE)
    ops = data['insertions']
    if type(ops) is not list or len(ops) > MAX_ITEMS:
        raise ValueError('insertions must be a bounded array')
    trace = []
    for op in ops:
        fields(op, ['index', 'count'])
        at = integer(op['index'], 'index', 0, size)
        count = integer(op['count'], 'count', 0, MAX_STORAGE)
        if size + count > MAX_STORAGE:
            raise ValueError('result exceeds storage budget')
        before = size
        reallocated = size + count > capacity
        if reallocated:
            capacity = size + max(size, count)
            if capacity > MAX_STORAGE:
                raise ValueError('SGI teaching capacity exceeds storage budget')
        size += count
        trace.append({'index': at, 'count': count, 'old_size': before,
                      'size': size, 'capacity': capacity, 'reallocated': reallocated,
                      'suffix_length': before - at})
    return {'size': size, 'capacity': capacity, 'trace': trace,
            'policy': 'SGI teaching insert: old_size + max(old_size,count) on reallocation'}


def deque_step(data):
    fields(data, ['op', 'buffer_elements', 'offset', 'delta'])
    length = integer(data['buffer_elements'], 'buffer_elements', 1, MAX_STORAGE)
    offset = integer(data['offset'], 'offset', 0, length - 1)
    delta = integer(data['delta'], 'delta', -MAX_STORAGE, MAX_STORAGE)
    node_delta, new_offset = divmod(offset + delta, length)
    return {'node_delta': node_delta, 'offset': new_offset, 'buffer_elements': length,
            'note': 'relative arithmetic only; caller must separately prove container bounds'}


def heap_trace(data):
    fields(data, ['op', 'values', 'action'], ['value'])
    values = integers(data['values'])
    if not max_heap(values):
        raise ValueError('values must already satisfy the max-heap invariant')
    action = data['action']
    states = [values[:]]
    if action == 'push':
        if 'value' not in data or len(values) == MAX_ITEMS:
            raise ValueError('push requires value and available item budget')
        values.append(integer(data['value'], 'value'))
        states.append(values[:])
        child = len(values) - 1
        while child:
            parent = (child - 1) // 2
            if values[parent] >= values[child]:
                break
            values[parent], values[child] = values[child], values[parent]
            states.append(values[:])
            child = parent
        return {'values': values, 'active_heap_end': len(values), 'states': states}
    if action != 'pop' or 'value' in data:
        raise ValueError('action must be push with value, or pop without value')
    if not values:
        raise ValueError('cannot pop an empty heap')
    values[0], values[-1] = values[-1], values[0]
    end = len(values) - 1
    states.append(values[:])
    parent = 0
    while 2 * parent + 1 < end:
        child = 2 * parent + 1
        if child + 1 < end and values[child + 1] > values[child]:
            child += 1
        if values[parent] >= values[child]:
            break
        values[parent], values[child] = values[child], values[parent]
        states.append(values[:])
        parent = child
    return {'values': values, 'active_heap_end': end, 'popped': values[-1],
            'container_size': len(values), 'states': states}


def logical_end(data):
    fields(data, ['op', 'values', 'action'], ['value'])
    values = integers(data['values'])
    action = data['action']
    kept = []
    if action == 'remove':
        if 'value' not in data:
            raise ValueError('remove requires value')
        target = integer(data['value'], 'value')
        kept = [x for x in values if x != target]
    elif action == 'unique' and 'value' not in data:
        for x in values:
            if not kept or kept[-1] != x:
                kept.append(x)
    else:
        raise ValueError('action must be remove with value, or unique without value')
    return {'valid_prefix': kept, 'new_end': len(kept), 'container_size': len(values),
            'erasure_range': [len(kept), len(values)], 'tail': 'unspecified; not modeled'}


def bounds(data):
    fields(data, ['op', 'values', 'value'])
    values = integers(data['values'])
    target = integer(data['value'], 'value')
    if any(values[i] > values[i + 1] for i in range(len(values) - 1)):
        raise ValueError('values must be sorted in nondecreasing integer order')
    def boundary(upper):
        lo, hi = 0, len(values)
        while lo < hi:
            mid = (lo + hi) // 2
            if values[mid] < target or (upper and values[mid] == target):
                lo = mid + 1
            else:
                hi = mid
        return lo
    lo, hi = boundary(False), boundary(True)
    return {'lower': lo, 'upper': hi, 'equal_range': [lo, hi], 'found': lo != hi}


def hash_buckets(data):
    fields(data, ['op', 'values', 'bucket_count'], ['new_bucket_count'])
    values = integers(data['values'])
    count = integer(data['bucket_count'], 'bucket_count', 1, MAX_STORAGE)
    def build(n):
        buckets = [[] for _ in range(n)]
        for x in values:
            buckets[x % n].append(x)
        return buckets
    result = {'bucket_count': count, 'buckets': build(count),
              'load_factor': len(values) / count,
              'hash_policy': 'teaching integer modulo, normalized nonnegative remainder'}
    if 'new_bucket_count' in data:
        new = integer(data['new_bucket_count'], 'new_bucket_count', 1, MAX_STORAGE)
        result.update({'new_bucket_count': new, 'new_buckets': build(new),
                       'new_load_factor': len(values) / new})
    return result


def copy_plan(data):
    fields(data, ['op', 'values', 'first', 'last', 'result', 'direction'])
    values = integers(data['values'])
    first = integer(data['first'], 'first', 0, len(values))
    last = integer(data['last'], 'last', first, len(values))
    result = integer(data['result'], 'result', 0, len(values))
    n = last - first
    direction = data['direction']
    if direction == 'forward':
        start, stop = result, result + n
        if stop > len(values) or (n and first <= result < last):
            raise ValueError('copy needs enough live destination objects and result outside [first,last)')
        indices = range(n)
    elif direction == 'backward':
        start, stop = result - n, result
        if start < 0 or (n and first < result <= last):
            raise ValueError('copy_backward needs enough live destination objects and result outside (first,last]')
        indices = range(n - 1, -1, -1)
    else:
        raise ValueError('direction must be forward or backward')
    for i in indices:
        values[start + i] = values[first + i]
    return {'values': values, 'destination': [start, stop],
            'returned_index': stop if direction == 'forward' else start,
            'contract': 'same integer array; checked live destination and overlap preconditions'}


OPERATIONS = {'pool-class': pool_class, 'vector-growth': vector_growth,
              'deque-step': deque_step, 'heap-trace': heap_trace,
              'logical-end': logical_end, 'bounds': bounds,
              'hash-buckets': hash_buckets, 'copy-plan': copy_plan}
OPERATIONS.update(EXTRA_OPERATIONS)


def run(data):
    if type(data) is not dict or type(data.get('op')) is not str or data['op'] not in OPERATIONS:
        raise ValueError('op must name one of: ' + ', '.join(OPERATIONS))
    return {'status': 'ok', 'op': data['op'], 'result': OPERATIONS[data['op']](data),
            'scope': 'original bounded teaching model, not an STL implementation or static analyzer'}


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate JSON field: ' + key)
        obj[key] = value
    return obj


def load_json(path, max_bytes=65536):
    p = Path(path)
    if p.stat().st_size > max_bytes:
        raise ValueError('JSON file exceeds byte budget')
    return json.loads(p.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError('non-finite JSON number')))


def main():
    try:
        if sys.argv[1:] == ['demo']:
            examples = [
                {'op': 'pool-class', 'bytes': 30},
                {'op': 'vector-growth', 'size': 3, 'capacity': 4,
                 'insertions': [{'index': 1, 'count': 2}]},
                {'op': 'deque-step', 'buffer_elements': 8, 'offset': 1, 'delta': -3},
                {'op': 'heap-trace', 'values': [9, 7, 8, 2], 'action': 'pop'},
                {'op': 'logical-end', 'values': [1, 1, 2, 1], 'action': 'unique'},
                {'op': 'bounds', 'values': [1, 2, 2, 4], 'value': 2},
                {'op': 'hash-buckets', 'values': [1, 6, -1], 'bucket_count': 5,
                 'new_bucket_count': 7},
                {'op': 'copy-plan', 'values': [1, 2, 3, 4, 5], 'first': 0,
                 'last': 3, 'result': 5, 'direction': 'backward'}]
            answer = {'status': 'ok', 'version': '1.0.0', 'demos': [run(x) for x in examples]}
        elif len(sys.argv) == 3 and sys.argv[1] == 'run':
            answer = run(load_json(sys.argv[2]))
        elif len(sys.argv) == 2 and sys.argv[1] == 'operations':
            answer = {'status':'ok','version':'1.0.0','operations':list(OPERATIONS),
                      'workflow':['experiment INPUT.json --out NEW_DIRECTORY','audit DIRECTORY --recompute']}
        elif len(sys.argv)==5 and sys.argv[1]=='experiment' and sys.argv[3]=='--out':
            answer=experiment_audit.create(sys.argv[2],sys.argv[4],load_json,run)
        elif len(sys.argv) in [3,4] and sys.argv[1]=='audit':
            if len(sys.argv)==4 and sys.argv[3]!='--recompute':raise ValueError('unknown audit option')
            answer=experiment_audit.audit(sys.argv[2],len(sys.argv)==4,load_json,run)
        else:
            raise ValueError('usage: stl_lab.py demo | operations | run INPUT.json | experiment INPUT.json --out NEW_DIRECTORY | audit DIRECTORY [--recompute]')
        print(json.dumps(answer, ensure_ascii=False, allow_nan=False))
        return 1 if answer.get('status')=='audit_failed' else 0
    except (ValueError, OSError, RecursionError) as exc:
        print(json.dumps({'status': 'input_error', 'message': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
