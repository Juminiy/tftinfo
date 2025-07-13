from get_env import setlist

from json import loads

from parse_grid import select_traits, select_champions, write_grid

from typing import Any,Dict

from json import dumps,loads

from functools import cmp_to_key

from tftdata import setdata
traitsall:Dict[str,Any]={}

for setof in setlist:
    setnum=setof.removeprefix('set')

    traitsall[setof]={
        'origins': [],
        'classes': []
    }

    traits=setdata[setof]['traits']

    champions=setdata[setof]['champions']
    chmps=[(chp['name'], chp['traits']) for chp in champions['champions'] if select_champions(setof, chp)]

    items=setdata[setof]['items']

    def item_cmp_fn(s1:str,s2:str) -> int:
        if s1 in ['Spatula', 'FryingPan']:
            return -1
        elif s2 in ['Spatula', 'FryingPan']:
            return 1
        return 0
    emblems={str(emb['key']).removesuffix('Emblem'): sorted(emb['compositions'], key=cmp_to_key(item_cmp_fn))
             for emb in items['items'] 
             if str(emb['key']).endswith('Emblem') and 
             ('compositions' in emb) and 
             (len(emb['compositions']) == 2) and 
             ('isEmblem' in emb) and 
             ('isHidden' not in emb) and 
             ('Spatula' in emb['compositions'] or 'FryingPan' in emb['compositions']) 
            }

    trt2chp:dict[str,set[str]]={}
    for chp in chmps:
        for trtofchp in chp[1]:
            if trtofchp in trt2chp:
                trt2chp[trtofchp].add(chp[0])
            else:
                trt2chp[trtofchp] = set([chp[0]])

    for trt in traits['traits']:
        if not select_traits(setof, trt):
            continue

        activestr='/'.join([str(styleof['min']) for styleof in trt['styles'] if 'min' in styleof ])
        trtdetail={
            'name': trt['name'],
            'desc': trt['desc'],
            'unit_active': activestr,
            'unit_count': len(trt2chp[trt['key']]) if trt['key'] in trt2chp else 0,
            'emblem': '+'.join(emblems[trt['key']]) if trt['key'] in emblems else '',
        }
        
        match trt['type']:
            case 'ORIGIN':
                traitsall[setof]['origins'].append(trtdetail)
            case 'CLASS':
                traitsall[setof]['classes'].append(trtdetail)
    
    with open(f'tfttraits/{setof}.json', 'w+') as trtfile:
        trtfile.write(dumps(traitsall[setof], ensure_ascii=True, indent='    '))
        trtfile.close()

    # write grid
    trtsz=len(traitsall[setof]['origins'])
    clssz=len(traitsall[setof]['classes'])
    origins2d=[]
    classes2d=[]
    for i in range(trtsz):
        trtv=traitsall[setof]['origins'][i]
        origins2d.append([str(trtv['name']), str(trtv['unit_active']), str(trtv['unit_count']), str(trtv['emblem']), ''])
    for i in range(clssz):
        clsv=traitsall[setof]['classes'][i]
        classes2d.append([str(clsv['name']), str(clsv['unit_active']), str(clsv['unit_count']), str(clsv['emblem']), ''])
    origins2d.sort(key=lambda ls: ls[0])
    classes2d.sort(key=lambda ls: ls[0])
    origins2d.insert(0, ["{{origin_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"])
    classes2d.insert(0, ["{{class_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"])

    with open(f'tfttraits/{setof}.txt', 'w+') as trtfile:
        trtfile.write('\n'.join(write_grid(origins2d)))
        trtfile.write('\n\n')
        trtfile.write('\n'.join(write_grid(classes2d)))
        trtfile.close()