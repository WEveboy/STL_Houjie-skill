"""Original bounded invariant and sequence models added after the base draft."""
from collections import Counter

MAX_ITEMS = 256

def fields(data, required, optional=()):
    if type(data) is not dict or set(required)-set(data) or set(data)-set(required)-set(optional):
        raise ValueError('missing or unknown fields')

def ints(values):
    if type(values) is not list or len(values)>MAX_ITEMS or any(type(v) is not int or abs(v)>1_000_000 for v in values):
        raise ValueError('expected at most 256 bounded integers')
    return values[:]

def set_operations(data):
    fields(data,['op','left','right','action'])
    left,right=ints(data['left']),ints(data['right'])
    if left!=sorted(left) or right!=sorted(right):raise ValueError('both ranges must be nondecreasing')
    action=data['action']
    if action not in ['union','intersection','difference','symmetric-difference']:
        raise ValueError('unknown set operation')
    # Two cursors mirror the range contract; Counter is used only to report counts.
    i=j=0;out=[]
    while i<len(left) and j<len(right):
        a,b=left[i],right[j]
        if a<b:
            if action in ['union','difference','symmetric-difference']:out.append(a)
            i+=1
        elif b<a:
            if action in ['union','symmetric-difference']:out.append(b)
            j+=1
        else:
            if action in ['union','intersection']:out.append(a)
            i+=1;j+=1
    if action in ['union','difference','symmetric-difference']:out.extend(left[i:])
    if action in ['union','symmetric-difference']:out.extend(right[j:])
    return {'values':out,'size':len(out),'multiplicities':dict(sorted(Counter(out).items())),
            'policy':'ordered integer multisets; duplicates retained by multiplicity'}

def range_transform(data):
    fields(data,['op','values','action'],['middle'])
    values=ints(data['values']);action=data['action']
    if action=='rotate':
        middle=data.get('middle')
        if type(middle) is not int or not 0<=middle<=len(values):raise ValueError('rotate requires a valid middle offset')
        result=values[middle:]+values[:middle]
        return {'values':result,'returned_index':len(values)-middle}
    if 'middle' in data:raise ValueError('middle is only valid for rotate')
    if action=='reverse':return {'values':values[::-1]}
    if action not in ['next-permutation','prev-permutation']:raise ValueError('unknown range transform')
    increasing=action=='next-permutation'
    before=(lambda a,b:a<b) if increasing else (lambda a,b:a>b)
    pivot=len(values)-2
    while pivot>=0 and not before(values[pivot],values[pivot+1]):pivot-=1
    if pivot<0:return {'values':values[::-1],'has_adjacent':False,'pivot':None}
    successor=len(values)-1
    while not before(values[pivot],values[successor]):successor-=1
    values[pivot],values[successor]=values[successor],values[pivot]
    values[pivot+1:]=values[pivot+1:][::-1]
    return {'values':values,'has_adjacent':True,'pivot':pivot}

def tree_check(data):
    fields(data,['op','root','nodes'])
    raw=data['nodes']
    if type(raw) is not list or len(raw)>MAX_ITEMS:raise ValueError('nodes exceeds 256 node budget')
    def identity(value):
        if value is None:return None
        if type(value) is not str or not value or len(value)>64:raise ValueError('node IDs must be nonempty strings of at most 64 characters')
        return value
    nodes={}
    for item in raw:
        fields(item,['id','key','color','left','right'])
        name=identity(item['id'])
        if name is None or name in nodes:raise ValueError('null or duplicate node ID')
        if type(item['key']) is not int or abs(item['key'])>1_000_000:raise ValueError('invalid integer key')
        if item['color'] not in ['B','R']:raise ValueError('color must be B or R')
        nodes[name]=dict(item,left=identity(item['left']),right=identity(item['right']))
    root=identity(data['root'])
    if root is None:
        if nodes:raise ValueError('nonempty nodes require a root')
        return {'valid':True,'node_count':0,'height':0,'black_height':1,'violations':[],
                'convention':'strict unique BST keys; NULL leaf contributes one black node'}
    if root not in nodes:raise ValueError('root is missing')
    indegree={k:0 for k in nodes}
    for node in nodes.values():
        for child in [node['left'],node['right']]:
            if child is not None:
                if child not in nodes:raise ValueError('missing child: '+child)
                indegree[child]+=1
                if indegree[child]>1:raise ValueError('a node has more than one incoming edge')
    if indegree[root]:raise ValueError('root has an incoming edge')
    visiting=set();seen=set();violations=[]
    def visit(name,lo,hi):
        if name is None:return 1,0
        if name in visiting:raise ValueError('cycle in tree')
        if name in seen:raise ValueError('shared child')
        visiting.add(name);node=nodes[name];key=node['key']
        if (lo is not None and key<=lo) or (hi is not None and key>=hi):
            violations.append({'node':name,'kind':'bst-order'})
        if node['color']=='R':
            for child in [node['left'],node['right']]:
                if child is not None and nodes[child]['color']=='R':
                    violations.append({'node':name,'kind':'red-parent-red-child','child':child})
        left_bh,left_h=visit(node['left'],lo,key)
        right_bh,right_h=visit(node['right'],key,hi)
        if left_bh is None or right_bh is None or left_bh!=right_bh:
            if left_bh is not None and right_bh is not None:violations.append({'node':name,'kind':'black-height','left':left_bh,'right':right_bh})
            bh=None
        else:bh=left_bh+(node['color']=='B')
        visiting.remove(name);seen.add(name)
        return bh,1+max(left_h,right_h)
    bh,height=visit(root,None,None)
    if len(seen)!=len(nodes):raise ValueError('unreachable nodes or disconnected cycle')
    if nodes[root]['color']!='B':violations.insert(0,{'node':root,'kind':'root-not-black'})
    return {'valid':not violations,'node_count':len(nodes),'height':height,'black_height':bh,
            'violations':violations,'convention':'strict unique BST keys; NULL leaf contributes one black node'}

OPERATIONS={'set-ops':set_operations,'range-transform':range_transform,'tree-check':tree_check}
