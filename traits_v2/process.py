from typing import (List,Mapping,Optional,Dict,Any,Tuple)

import os 

def next_chuck(lines: List[str], cursor: int) -> Tuple[int,int,bool]:
    """
        return Tuple[int,int,int] (chunk_si, chunk_ei, valid)
    """
    while 0<=cursor < len(lines):
        while cursor < len(lines) and len(lines[cursor]) == 0:
            cursor+=1
        starti = cursor
        while cursor < len(lines) and len(lines[cursor]) > 0:
            cursor+=1
        if cursor > starti:
            return (starti, cursor, True)
        else:
            return (-1,-1,False)
    return (-1,-1,False)

def parse_2d_table(l3: List[str]) -> List[dict[str,Any]]:
    res:List[dict[str,Any]]=[]
    if len(l3) == 0:
        return res
    l3key=[item.strip().strip('{').strip('}') for item in l3[0].split('|')]
    for ls in l3[1:]:
        l3item=[item.strip() for item in ls.split('|')]
        l3dict={}
        for idx in range(len(l3item)):
            l3dict[l3key[idx]] = l3item[idx]
        res.append(l3dict)
    return res

def parse_grid_to_dict(lgrid: List[str]) -> Dict[str,Any]:
    res:dict[str,Any]={
        'grid': [],
        'maps': {
            'origins': {},
            'classes': {}
        }
    }
    if len(lgrid) == 0:
        return res
    d2grid=[ls.split('|') for ls in lgrid]
    m,n=len(d2grid),len(d2grid[0])
    for i in range(m):
        for j in range(n):
            d2grid[i][j]=d2grid[i][j].strip()
    res['grid'] = d2grid
    
    def split_unit(unit_i: str) -> List[str]:
        return [unit_each for unit_each in unit_i.split('/') if len(unit_each) > 0]
    originsRes=dict[str,List[str]]()
    classesRes=dict[str,List[str]]()
    for i in range(1, m):
        originsRes[d2grid[i][0]] = []
        for j in range(1, n):
            if len(d2grid[i][j]) > 0:
                if d2grid[i][0] not in originsRes:
                    originsRes[d2grid[i][0]] = []
                originsRes[d2grid[i][0]].extend(split_unit(d2grid[i][j]))
        originsRes[d2grid[i][0]] = list(set(originsRes[d2grid[i][0]]))
    for j in range(1,n):
        classesRes[d2grid[0][j]]= []
        for i in range(1,m):
            if len(d2grid[i][j]) > 0:
                if d2grid[0][j] not in classesRes:
                    classesRes[d2grid[0][j]] = []
                classesRes[d2grid[0][j]].extend(split_unit(d2grid[i][j]))
        originsRes[d2grid[0][j]] = list(set(classesRes[d2grid[0][j]]))
    res['maps']['origins'] = originsRes
    res['maps']['classes'] = classesRes
    return res

def can_parse_to_2d_table(setof:str, curl2:str, curl3:str) -> bool:
    def mergedict(d1:dict, d2:dict={}) -> dict:
        d1copy=d1.copy()
        for k2,v2 in d2.items():
            if k2 in d1copy and type(v2)==type(d1copy[k2])==list:
                d1k2copy=list(d1copy[k2]).copy()
                d1k2copy.extend(v2)
                d1copy[k2]=d1k2copy
            else:
                d1copy[k2]=v2
        return d1copy
    comap={
        'timeline': ['date'],
        'units': None,
        'traits': ['origins','classes'],
    }
    set2map={
        's14': mergedict(comap, {
            'opening encounters': ['normal encounters', 'hacked encounters'],
        }),
        's13': mergedict(comap, {
            'traits': ['team-up'],
            'opening encounters': ['opening encounters'],
        }),
        's12': mergedict(comap, {
            'portal': ['augments', 'champions', 'anvils', 'gold', 'loot', 'charms'],
        }),
        's11': mergedict(comap, {
            
        }),
        's10': mergedict(comap, {
            'portal': ['champions', 'fight', 'headliner', 'loot', 'gold', 'augments', 'anvils']
        }),
        's9.5': mergedict(comap, {}),
        's9': mergedict(comap, {
            'portal': ['bandle city', 'bilgewater', 'demacia', 'freljord', 'ionia', 'ixtal', 'noxus', 'piltover', 'shadow isles', 'shurima', 'targon', 'void', 'zaun']
        }),
        's8.5': mergedict(comap, {}),
        's8': mergedict(comap, {}),
        's7.5': mergedict(comap, {}),
        's7': mergedict(comap, {}),
        's6.5': mergedict(comap, {}),
        's6': mergedict(comap, {}),
        's5.5': mergedict(comap, {}),
        's5': mergedict(comap, {}),
        's4.5': mergedict(comap, {}),
        's4': mergedict(comap, {}),
        's3.5': mergedict(comap, {}),
        's3': mergedict(comap, {}),
        's2': mergedict(comap, {}),
        's1': mergedict(comap, {}),
    }
    return setof in set2map and curl2 in set2map[setof] and curl3 in set2map[setof][curl2]

def process_tft() -> Dict[str,Any]:
    sdict:dict[str,Any]={}
    for seti in ['1','2','3','3.5','4','4.5','5','5.5','6','6.5','7','7.5','8','8.5','9','9.5','10','11','12','13','14']:
        setof=f's{seti}'
        setfilename=f'data/set/{setof}.txt'
        if not os.path.exists(setfilename) or \
            not os.path.isfile(setfilename):
            continue
        with open(setfilename,'r',encoding='utf-8') as setfile:
            lines=[line.strip() for line in setfile.readlines()]
            sdict[setof] = {}
            sdict[setof]['name'] = lines[0].removeprefix('# ')
            lines=lines[1:]
            linei=0
            curl2=''
            while 0 <= linei < len(lines):
                (starti, linei, ok) = next_chuck(lines, linei)
                if ok:
                    if starti < len(lines) and lines[starti].startswith('## '):
                        curl2=lines[starti].removeprefix('## ').lower()
                        sdict[setof][curl2] = {}
                        starti+=1
                    if starti < len(lines) and lines[starti].startswith('### '):
                        curl3=lines[starti].removeprefix('### ').lower()
                        if can_parse_to_2d_table(setof, curl2, curl3):
                            sdict[setof][curl2][curl3] = \
                                parse_2d_table(lines[starti+1:linei])
                        elif curl3 == 'synergygrid':
                            sdict[setof][curl2][curl3] = \
                                parse_grid_to_dict(lines[starti+1:linei])
                        else:
                            sdict[setof][curl2][curl3] = lines[starti+1:linei]

    return sdict

from json import dumps, loads
tftinfo=dumps(process_tft(), ensure_ascii=True,indent='    ')
with open('data/output/tft_set_all.json', 'w+') as tftfile:
    tftfile.write(tftinfo)
    tftfile.close()