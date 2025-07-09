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

def get_origins_classes(l3: List[str]) -> List[dict[str,Any]]:
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

def get_grid_dict(lgrid: List[str]) -> Dict[str,Any]:
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

def process_tft() -> Dict[str,Any]:
    sdict:dict[str,Any]={}
    for seti in ['1','2','3','3.5','4','4.5','5','5.5','6','6.5','7','7.5','8','8.5','9','9.5','10','11','12','13','14']:
        setof=f's{seti}'
        setfilename=f'{setof}.txt'
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
                        if curl3 in ['origins', 'classes', 'date']:
                            sdict[setof][curl2][curl3] = \
                                get_origins_classes(lines[starti+1:linei])
                        elif curl3 == 'synergygrid':
                            sdict[setof][curl2][curl3] = \
                                get_grid_dict(lines[starti+1:linei])
                        else:
                            sdict[setof][curl2][curl3] = lines[starti+1:linei]

    return sdict

from json import dumps, loads
tftinfo=dumps(
    process_tft(),
    ensure_ascii=True,
    indent='    ',
)
with open('s_all.json', 'w+') as tftfile:
    tftfile.write(tftinfo)
    tftfile.close()

def find_hard_traits() -> Dict[str,Any]:
    def parse_unit_active(actv: str) -> int:
        actvs = [aci if aci[0].isdigit() else aci[1:] for aci in actv.split('/') if len(aci)> 0]
        return int(actvs[len(actvs)-1])

    def process_count(bond_of: dict, max_active_gt:int=9, emblem_cnt_gt:int=2, setof:str='?') -> Tuple[Dict[str,Any], bool]: 
        actvunit = parse_unit_active(bond_of['unit_active'])
        unitcnt = int(bond_of['unit_count']) if str(bond_of['unit_count']).isdigit() else actvunit
        emcraftable = bool(str(bond_of['emblem']).count('+') > 0)
        if (actvunit >= max_active_gt and actvunit-unitcnt >= emblem_cnt_gt) or (actvunit-unitcnt >= emblem_cnt_gt+1):
            return (
                {
                    'max_unit_active': actvunit,
                    'emblem_count': actvunit-unitcnt-(1 if setof=='s10' else 0),
                    'emblem_craftable': emcraftable,
                }, True
            )
        # elif not emcraftable and actvunit-unitcnt>0:
        #     return (
        #         {
        #             'max_unit_active': actvunit,
        #             'current_unit': unitcnt,
        #             'emblem_craftable': emcraftable,
        #             'bond_impossible': True,
        #         },True
        #     )
        else:
            return ({}, False)

    info=process_tft()
    hard_traits:dict[str,Any]={}
    for setof, setinfo in info.items():
        # active_count >= 9 or emblem >= 2
        hard_traits[setof]={}
        # traits.origins
        for originof in setinfo['traits']['origins']:
            stat,ok=process_count(originof, setof=setof)
            if ok:
                hard_traits[setof][originof['origin_name']] = stat
        # traits.classes
        for classof in setinfo['traits']['classes']:
            stat,ok= process_count(classof, setof=setof)
            if ok:
                hard_traits[setof][classof['class_name']] = stat
    return hard_traits

hard_traits_info=dumps(find_hard_traits(), ensure_ascii=True, indent='    ')
with open('s_hard_traits.json', 'w+') as htfile:
    htfile.write(hard_traits_info)
    htfile.close()