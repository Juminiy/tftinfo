from get_env import setlist

from json import dumps,loads

def two_champions_slash(ch1: str, ch2: str) -> str:
    if len(ch1) > 0:
        return ch1+'/'+ch2
    else:
        return ch2

def select_traits(setof:str, trt:dict) -> bool:
    max_active_val=0
    for styleof in trt['styles']:
        if 'min' in styleof:
            max_active_val = max(max_active_val, styleof['min'])
        if 'max' in styleof:
            max_active_val = max(max_active_val, styleof['max'])    

    cursetnum=setof.removeprefix('set').removesuffix('.5')
    if setof in ['set14','set13','set12','set11']:
        return str(trt['ingameKey']).startswith(f'TFT{cursetnum}_') and \
            max_active_val > 1 and \
            'isHidden' not in trt
    elif setof in ['set10','set9','set8','set7','set6','set5']:
        return str(trt['ingameKey']).startswith(f'Set{cursetnum}_') and \
            max_active_val > 1 and \
            'isHidden' not in trt
    elif setof in ['set9.5','set8.5','set7.5','set6.5','set5.5','set4.5']:
        return str(trt['ingameKey']).startswith((f'Set{cursetnum}_', f'Set{cursetnum}b_')) and \
            max_active_val > 1 and \
            'isHidden' not in trt
    elif setof in ['set4','set3.5','set3','set2','set1']:
        return (str(trt['ingameKey']).startswith((f'Set{cursetnum}_')) or not str(trt['ingameKey']).startswith('Set')) and \
            max_active_val > 1 and \
            'isHidden' not in trt
    return False

def select_champions(setof:str, chp:dict) -> bool:
    cursetnum=setof.removeprefix('set').removesuffix('.5')
    if setof.endswith('.5'):
        return str(chp['ingameKey']).startswith((f'TFT{cursetnum}_', 'TFT9b_','TFT8b_','TFT7b_','TFT6b_','TFT4b_')) and \
                'isHidden' not in chp
    elif setof == 'set1':
        return str(chp['ingameKey']).startswith('TFT_') and \
                'isHidden' not in chp
    else:
        return str(chp['ingameKey']).startswith(f'TFT{cursetnum}_') and \
                'isHidden' not in chp

def write_grid(grid2d: list[list[str]]) -> list[str]:
    szs:list[int]=[]
    for j in range(len(grid2d[0])):
        mxsz=0
        for i in range(len(grid2d)):
            mxsz=max(mxsz, len(grid2d[i][j]))
        szs.append(mxsz)
    
    res:list[str]=[]
    for i in range(len(grid2d)):
        resv=''
        for j in range(len(grid2d[i])):
            resv+= (f'{grid2d[i][j]:<{szs[j]}}'+(' | ' if j<len(grid2d[i])-1 else ''))
        res.append(resv)
    return res

from tftdata import setdata
for setof in setlist:
    setnum=setof.removeprefix('set')
    
    # select traits
    traits=setdata[setof]['traits']
    origin_key:list[str]=[]
    class_key:list[str]=[]
    key2name:dict[str,str]={}
    for trt in traits['traits']:
        if not select_traits(setof, trt):
            continue
        match trt['type']:
            case 'ORIGIN':
                origin_key.append(trt['key'])
            case 'CLASS':
                class_key.append(trt['key'])
        key2name[trt['key']]=trt['name']
    origin_key.sort()
    class_key.sort()
    
    # select champions
    champions=setdata[setof]['champions']
    chmps=[(chp['name'], chp['traits']) for chp in champions['champions'] if select_champions(setof, chp)]
    
    # champions grid
    grid2d=[['']*(len(class_key)) for _ in range(len(origin_key))]
    for chp in chmps:
        chpname=chp[0]
        chptrt=chp[1]
        for chpori in [ori for ori in chptrt if ori in origin_key]:
            for chpcls in [chpcls for chpcls in chptrt if chpcls in class_key]:
                oriidx,clsidx=origin_key.index(chpori),class_key.index(chpcls)
                grid2d[oriidx][clsidx]=two_champions_slash(grid2d[oriidx][clsidx], chpname)
    
    # first row is classls
    grid2d.insert(0, [key2name[clskey] for clskey in class_key])

    # header fix
    originlsfix=[key2name[orikey] for orikey in origin_key]
    originlsfix.insert(0, 'Origins\\Classes')
    # first col is originls
    for i in range(len(grid2d)):
        grid2d[i].insert(0, originlsfix[i])
    
    with open(f'tftgrid/{setof}.json', 'w+') as setgridf:
        setgridf.write(dumps(grid2d, ensure_ascii=True, indent='    '))
        setgridf.close()
    with open(f'tftgrid/{setof}.txt', 'w+') as setgridf:
        setgridf.write('\n'.join(write_grid(grid2d)))
        setgridf.close()