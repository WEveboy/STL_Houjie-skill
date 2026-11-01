import copy
from collections import Counter
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import stl_lab as lab
import experiment_audit as audit

def result(**data):return lab.run(data)['result']
def node(name,key,color='B',left=None,right=None):return dict(id=name,key=key,color=color,left=left,right=right)

class ExtendedModels(unittest.TestCase):
    def test_multiset_against_independent_counts(self):
        for a in [[],[1],[1,1,2],[-1,0,0,3]]:
            for b in [[],[1,1],[0,2,2]]:
                ca,cb=Counter(a),Counter(b)
                expected={'union':ca|cb,'intersection':ca&cb,'difference':ca-cb,
                          'symmetric-difference':(ca-cb)+(cb-ca)}
                for action,counts in expected.items():
                    r=result(op='set-ops',left=a,right=b,action=action)
                    self.assertEqual(Counter(r['values']),counts)
                    self.assertEqual(r['values'],sorted(r['values']))
    def test_multiset_bad_conditions(self):
        for change in [{'left':[2,1]},{'right':[True]},{'action':'merge'}, {'left':[0]*257}]:
            data=dict(op='set-ops',left=[],right=[],action='union');data.update(change)
            with self.assertRaises(ValueError):lab.run(data)
    def test_permutations_against_exhaustive_order(self):
        for raw in [[],[1],[1,1],[1,2,3],[0,0,1,2],[-1,0,1,1]]:
            ordered=sorted(set(itertools.permutations(raw)))
            for i,values in enumerate(ordered):
                for action,step in [('next-permutation',1),('prev-permutation',-1)]:
                    r=result(op='range-transform',values=list(values),action=action)
                    self.assertEqual(r['values'],list(ordered[(i+step)%len(ordered)]))
                    self.assertEqual(r['has_adjacent'],0<=i+step<len(ordered))
    def test_rotate_and_reverse_invariants(self):
        for n in range(9):
            values=list(range(n))
            for k in range(n+1):
                r=result(op='range-transform',values=values,action='rotate',middle=k)
                self.assertEqual(r['values'],[values[(i+k)%n] for i in range(n)])
                self.assertEqual(r['returned_index'],n-k)
            r=result(op='range-transform',values=values,action='reverse')
            self.assertEqual(r['values'],list(reversed(values)))
        for kw in [{'action':'rotate','middle':True},{'action':'rotate','middle':4},
                   {'action':'reverse','middle':0},{'action':'unknown'}]:
            with self.assertRaises(ValueError):result(op='range-transform',values=[1,2],**kw)
    def valid_tree(self):
        return dict(op='tree-check',root='r',nodes=[node('r',10,'B','l','h'),node('l',5,'R'),node('h',15,'R')])
    def test_rb_valid_and_empty(self):
        r=lab.run(self.valid_tree())['result']
        self.assertTrue(r['valid']);self.assertEqual(r['black_height'],2);self.assertEqual(r['height'],2)
        self.assertEqual(result(op='tree-check',root=None,nodes=[])['black_height'],1)
    def test_rb_distinct_violation_modes(self):
        d=self.valid_tree();d['nodes'][0]['color']='R'
        violations=lab.run(d)['result']['violations']
        self.assertIn('root-not-black',[x['kind'] for x in violations])
        self.assertIn('red-parent-red-child',[x['kind'] for x in violations])
        d=self.valid_tree();d['nodes'][1]['color']='B'
        r=lab.run(d)['result'];self.assertFalse(r['valid']);self.assertIsNone(r['black_height'])
        self.assertIn('black-height',[x['kind'] for x in r['violations']])
        d=self.valid_tree();d['nodes'][1]['key']=20
        self.assertIn('bst-order',[x['kind'] for x in lab.run(d)['result']['violations']])
    def test_tree_structural_rejection(self):
        samples=[]
        d=self.valid_tree();d['nodes'][0]['left']='missing';samples.append(d)
        d=self.valid_tree();d['nodes'][0]['right']='l';samples.append(d)
        d=self.valid_tree();d['nodes'][1]['left']='r';samples.append(d)
        d=self.valid_tree();d['nodes'].append(node('orphan',99));samples.append(d)
        d=self.valid_tree();d['nodes'].append(node('l',99));samples.append(d)
        d=self.valid_tree();d['nodes'][1]['key']=True;samples.append(d)
        samples.append(dict(op='tree-check',root=None,nodes=[node('a',1)]))
        for data in samples:
            with self.assertRaises(ValueError):lab.run(data)

class ExperimentWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.input=self.root/'source.json';self.out=self.root/'experiment'
        self.data=dict(op='set-ops',left=[1,1,12],right=[1,3],action='union')
        self.input.write_bytes(audit.encoded(self.data))
    def tearDown(self):self.temp.cleanup()
    def create(self):return audit.create(self.input,self.out,lab.load_json,lab.run)
    def check(self,recompute=True):return audit.audit(self.out,recompute,lab.load_json,lab.run)
    def rewrite(self,name,value,rehash=False):
        p=self.out/name;p.write_bytes(audit.encoded(value))
        if rehash:
            manifest=lab.load_json(self.out/'manifest.json')
            manifest['files'][name]=audit.sha(p.read_bytes())
            (self.out/'manifest.json').write_bytes(audit.encoded(manifest))
    def test_archive_recompute_and_refuse_overwrite(self):
        self.assertEqual(self.create()['status'],'archived')
        self.assertEqual(self.check()['status'],'ok')
        with self.assertRaises(ValueError):self.create()
    def test_raw_tamper_detected(self):
        self.create();self.rewrite('result.json',{'status':'ok','result':{}})
        self.assertIn('hash:result.json',self.check()['failures'])
    def test_coordinated_result_manifest_tamper_needs_recompute(self):
        self.create();r=lab.load_json(self.out/'result.json');r['result']['values']=[999]
        self.rewrite('result.json',r,True)
        self.assertEqual(self.check(False)['status'],'ok')
        self.assertIn('recomputed-result',self.check()['failures'])
    def test_type_tamper_cannot_equal_boolean_with_integer(self):
        self.input.write_bytes(audit.encoded(dict(op='tree-check',root=None,nodes=[])))
        self.create();r=lab.load_json(self.out/'result.json');r['result']['valid']=1
        self.rewrite('result.json',r,True)
        self.assertIn('recomputed-result',self.check()['failures'])
    def test_event_order_and_time_rejected_after_rehash(self):
        self.create();events=lab.load_json(self.out/'events.json');events[1]['sequence']=0
        self.rewrite('events.json',events,True)
        self.assertIn('events-sequence',self.check()['failures'])
        events[1]['sequence']=1;events[1]['utc']='bad-time';self.rewrite('events.json',events,True)
        self.assertIn('events-time',self.check()['failures'])
    def test_invalid_input_does_not_create_archive(self):
        self.input.write_bytes(b'{"op":"pool-class","bytes":0}')
        with self.assertRaises(ValueError):self.create()
        self.assertFalse(self.out.exists())
    def test_manifest_and_code_contract(self):
        self.create();m=lab.load_json(self.out/'manifest.json');m['code']={}
        (self.out/'manifest.json').write_bytes(audit.encoded(m))
        self.assertIn('code-fingerprint',self.check()['failures'])
        m['files']['../escape']='x';(self.out/'manifest.json').write_bytes(audit.encoded(m))
        with self.assertRaises(ValueError):self.check()
    def test_large_legal_output_can_be_audited(self):
        self.input.write_bytes(audit.encoded(dict(op='hash-buckets',values=[1],bucket_count=4096,new_bucket_count=4096)))
        self.create();self.assertEqual(self.check()['status'],'ok')
    def test_cli_exit_codes_and_operation_list(self):
        script=Path(lab.__file__).resolve()
        def cli(*args):return subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True)
        p=cli('operations');self.assertEqual(len(json.loads(p.stdout)['operations']),11)
        self.assertEqual(cli('experiment',self.input,'--out',self.out).returncode,0)
        self.assertEqual(cli('audit',self.out,'--recompute').returncode,0)
        self.rewrite('result.json',{'tampered':True})
        p=cli('audit',self.out,'--recompute');self.assertEqual(p.returncode,1)
        self.assertEqual(json.loads(p.stdout)['status'],'audit_failed')
        self.assertEqual(cli('audit',self.out,'--unknown').returncode,2)

if __name__=='__main__':unittest.main(verbosity=2)
