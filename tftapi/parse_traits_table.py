from env import setlist

from typing import Any,Dict

from json import dumps

from meta_data import setdata

from meta_func import select_traits, select_champions, emblem_cmp_key, grid_fix_write
from meta_func import select_traits_legal, count_traits_style

def parse_stats(statsd: dict[str,str], descs:str) -> str:
    for _,sval in statsd.items():
        pass
    return ''

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
    emblems={str(emb['key']).removesuffix('Emblem'): sorted(emb['compositions'], key=emblem_cmp_key)
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
            'desc': parse_stats(trt['stats'], trt['desc']),
            'unit_active': activestr,
            'unit_count': len(trt2chp[trt['key']]) if trt['key'] in trt2chp else 0,
            'emblem': '+'.join(emblems[trt['key']]) if trt['key'] in emblems else '',
        }
        
        match trt['type']:
            case 'ORIGIN':
                traitsall[setof]['origins'].append(trtdetail)
            case 'CLASS':
                traitsall[setof]['classes'].append(trtdetail)
    
    # with open(f'tfttraits/{setof}.json', 'w+') as trtfile:
    #     trtfile.write(dumps(traitsall[setof], ensure_ascii=True, indent='    '))
    #     trtfile.close()

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

    with open(f'tfttraits/table/{setof}.txt', 'w+') as trtfile:
        trtfile.write(grid_fix_write(origins2d))
        trtfile.write('\n\n')
        trtfile.write(grid_fix_write(classes2d))
        trtfile.close()

# get unique bond
for setof in setlist:
    trt1chp={
        chp['traits'][0]: chp['name']
        for chp in setdata[setof]['champions']['champions'] if select_champions(setof, chp) and 'traits' in chp and len(chp['traits'])==1
    }

    for trt in setdata[setof]['traits']['traits']:
        if select_traits_legal(setof, trt) and \
            count_traits_style(trt) == 1:
            if 'unique' not in traitsall[setof]:
                traitsall[setof]['unique'] = []
            traitsall[setof]['unique'].append({
                'name': trt['name'],
                'champion': trt1chp[trt['key']] if trt['key'] in trt1chp else '',
            })
    # print(traitsall[setof]['unique'] if 'unique' in traitsall[setof] else 'None')
