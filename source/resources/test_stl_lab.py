import bisect
import heapq
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import stl_lab as lab


class TeachingModels(unittest.TestCase):
    def result(self, **kwargs):
        return lab.run(kwargs)['result']

    def test_pool_classes_exhaustive(self):
        for n in range(1, 129):
            r = self.result(op='pool-class', bytes=n)
            self.assertEqual(r['class_bytes'], next(x for x in range(8, 129, 8) if x >= n))
            self.assertEqual(r['free_list_index'], (n - 1) // 8)
        self.assertEqual(self.result(op='pool-class', bytes=129)['level'], 1)
        for n in [0, -1, True, 1.5, 1000001]:
            with self.assertRaises(ValueError):
                self.result(op='pool-class', bytes=n)

    def test_vector_growth(self):
        r = self.result(op='vector-growth', size=0, capacity=0,
                        insertions=[{'index': 0, 'count': 1}, {'index': 0, 'count': 1},
                                    {'index': 1, 'count': 3}, {'index': 5, 'count': 0}])
        self.assertEqual([x['capacity'] for x in r['trace']], [1, 2, 5, 5])
        self.assertEqual(r['size'], 5)
        r = self.result(op='vector-growth', size=2, capacity=8,
                        insertions=[{'index': 1, 'count': 2}])
        self.assertFalse(r['trace'][0]['reallocated'])
        for change in [{'index': 3, 'count': 1}, {'index': 0, 'count': -1},
                       {'index': True, 'count': 1}, {'index': 0, 'count': 4096}]:
            with self.assertRaises(ValueError):
                self.result(op='vector-growth', size=2, capacity=2, insertions=[change])

    def test_deque_relative_arithmetic(self):
        for width in range(1, 10):
            for at in range(width):
                for delta in range(-19, 20):
                    r = self.result(op='deque-step', buffer_elements=width, offset=at, delta=delta)
                    self.assertEqual(r['node_delta'] * width + r['offset'], at + delta)
                    self.assertTrue(0 <= r['offset'] < width)
        with self.assertRaises(ValueError):
            self.result(op='deque-step', buffer_elements=0, offset=0, delta=0)
        with self.assertRaises(ValueError):
            self.result(op='deque-step', buffer_elements=8, offset=8, delta=0)

    def test_heap_with_independent_heapq(self):
        for raw in [[], [1], [2, 2, 1], [8, 3, -1, 4, 7]]:
            ref = [-x for x in raw]
            heapq.heapify(ref)
            initial = [-x for x in ref]
            for value in [-10, 0, 10]:
                r = self.result(op='heap-trace', values=initial, action='push', value=value)
                self.assertTrue(lab.max_heap(r['values']))
                self.assertEqual(sorted(r['values']), sorted(raw + [value]))
                self.assertEqual(r['values'][0], max(raw + [value]))
            if raw:
                r = self.result(op='heap-trace', values=initial, action='pop')
                self.assertEqual(r['popped'], -heapq.heappop(ref))
                self.assertEqual(len(r['values']), len(raw))
                self.assertEqual(sorted(r['values'][:-1]), sorted(-x for x in ref))
                self.assertTrue(lab.max_heap(r['values'][:-1]))
        for values in [[], [1, 2]]:
            with self.assertRaises(ValueError):
                self.result(op='heap-trace', values=values, action='pop')
        with self.assertRaises(ValueError):
            self.result(op='heap-trace', values=[1], action='pop', value=2)

    def test_logical_end_with_reference_groupby(self):
        for values in [[], [1], [1, 1, 2, 1], [0, 0, 0]]:
            r = self.result(op='logical-end', values=values, action='unique')
            self.assertEqual(r['valid_prefix'], [x for x, _ in itertools.groupby(values)])
            r = self.result(op='logical-end', values=values, action='remove', value=0)
            self.assertEqual(r['valid_prefix'], list(filter(lambda x: x != 0, values)))
            self.assertEqual(r['container_size'], len(values))
        with self.assertRaises(ValueError):
            self.result(op='logical-end', values=[1], action='remove')
        with self.assertRaises(ValueError):
            self.result(op='logical-end', values=[1], action='unique', value=1)

    def test_bounds_against_bisect(self):
        for n in range(7):
            for values in itertools.combinations_with_replacement(range(3), n):
                for value in range(-1, 4):
                    r = self.result(op='bounds', values=list(values), value=value)
                    self.assertEqual(r['equal_range'], [bisect.bisect_left(values, value),
                                                        bisect.bisect_right(values, value)])
        with self.assertRaises(ValueError):
            self.result(op='bounds', values=[2, 1], value=1)
        with self.assertRaises(ValueError):
            self.result(op='bounds', values=[True], value=1)

    def test_hash_rebucket(self):
        values = [-10, -1, 0, 1, 6, 6]
        r = self.result(op='hash-buckets', values=values, bucket_count=5, new_bucket_count=7)
        for count, buckets in [(5, r['buckets']), (7, r['new_buckets'])]:
            self.assertEqual(sorted(x for bucket in buckets for x in bucket), sorted(values))
            for i, bucket in enumerate(buckets):
                self.assertTrue(all((x - i) % count == 0 for x in bucket))
        self.assertEqual(self.result(op='hash-buckets', values=[], bucket_count=1)['buckets'], [[]])
        with self.assertRaises(ValueError):
            self.result(op='hash-buckets', values=[1], bucket_count=0)

    def test_copy_legal_shifts_and_boundaries(self):
        values = [1, 2, 3, 4, 5]
        self.assertEqual(self.result(op='copy-plan', values=values, first=2, last=5,
                                     result=0, direction='forward')['values'], [3, 4, 5, 4, 5])
        self.assertEqual(self.result(op='copy-plan', values=values, first=0, last=3,
                                     result=5, direction='backward')['values'], [1, 2, 1, 2, 3])
        self.assertEqual(self.result(op='copy-plan', values=[], first=0, last=0,
                                     result=0, direction='forward')['values'], [])
        for first, last, result, direction in [(0, 3, 1, 'forward'), (0, 3, 0, 'forward'),
                                                (1, 4, 3, 'backward'), (1, 4, 4, 'backward'),
                                                (3, 2, 0, 'forward'), (0, 3, 4, 'forward'),
                                                (0, 3, 1, 'backward')]:
            with self.assertRaises(ValueError):
                self.result(op='copy-plan', values=values, first=first, last=last,
                            result=result, direction=direction)

    def test_input_schema_and_budget(self):
        for data in [{}, {'op': []}, {'op': 'missing'}, {'op': 'pool-class', 'bytes': 1, 'extra': 2},
                     {'op': 'bounds', 'values': [0] * 257, 'value': 0}]:
            with self.assertRaises(ValueError):
                lab.run(data)
        with self.assertRaises(ValueError):
            json.loads('{"op":"x","op":"y"}', object_pairs_hook=lab.unique_object)

    def test_cli_single_json_and_bad_inputs(self):
        script = str(Path(lab.__file__).resolve())
        p = subprocess.run([sys.executable, script, 'demo'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(len(json.loads(p.stdout)['demos']), 8)
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'input.json'
            source.write_text('\ufeff{"op":"pool-class","bytes":8}', encoding='utf-8')
            p = subprocess.run([sys.executable, script, 'run', str(source)], capture_output=True, text=True)
            self.assertEqual(json.loads(p.stdout)['result']['class_bytes'], 8)
            for text in ['{"op":"pool-class","bytes":NaN}', '{"op":"pool-class","op":"bounds"}',
                         '[]', '{"op":"pool-class","bytes":true}', 'x' * 65537]:
                source.write_text(text, encoding='utf-8')
                p = subprocess.run([sys.executable, script, 'run', str(source)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2)
                self.assertEqual(json.loads(p.stdout)['status'], 'input_error')


if __name__ == '__main__':
    unittest.main(verbosity=2)
