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
    emblems:dict[str,Any]={}
    for emb in items['items']:
        if ('isEmblem' in emb) and ('isHidden' not in emb):
            embkeyraw,embnameraw,embkey=str(emb['key']),str(emb['name']),''
            if embkeyraw.endswith('Emblem') or embkeyraw.endswith('EmblemItem'):
                embkey=embkeyraw.removesuffix('Emblem').removesuffix('EmblemItem')
            elif embnameraw.endswith(' Emblem') or embnameraw.endswith(' EmblemItem'):
                embkey=embnameraw.removesuffix(' Emblem').removesuffix(' EmblemItem')
            embcomposi=[]
            # craftable
            if ('compositions' in emb) and (len(emb['compositions']) == 2) and \
                ('Spatula' in emb['compositions'] or 'FryingPan' in emb['compositions']):
                embcomposi = sorted(emb['compositions'], key=emblem_cmp_key)
            # uncraftable
            elif 'compositions' not in emb:
                embcomposi = ['uncraftable']
            emblems[embkey] = embcomposi


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

        activestr0='/'.join([str(styleof['min']) for styleof in trt['styles'] if 'min' in styleof ])
        activestr1='/'.join([statkey for statkey in trt['stats']])
        activestr=activestr0 if len(activestr0) > len(activestr1) else activestr1
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
    trt1chp:dict[str,list[str]]={} # trait_name -> champion_name_list
    chpcost:dict[str,int]={}       # champion_name -> champion_cost
    for chp in setdata[setof]['champions']['champions']:
        chpcost[chp['name']] = min(chp['cost'])
        if select_champions(setof, chp) and \
            'traits' in chp:
            for trt0 in chp['traits']:
                if trt0 not in trt1chp:
                    trt1chp[trt0] = []
                trt1chp[trt0].append(chp['name'])

    traitsall[setof]['unique'] = []
    for trt in setdata[setof]['traits']['traits']:
        if select_traits_legal(setof, trt) and \
            count_traits_style(trt) == 1:
            traitsall[setof]['unique'].append({
                'trait_name': trt['name'],
                'champion_cost': '/'.join([str(chpcost[chpname]) for chpname in trt1chp[trt['key']]]) if trt['key'] in trt1chp else '',
                'champion_names': '/'.join(trt1chp[trt['key']]) if trt['key'] in trt1chp else '',
            })
    
    with open(f'tfttraits/table/{setof}.txt', 'a+') as stfile:
        stfile.write('\n\n')
        stfile.write(grid_fix_write(grid2d=[
            [uqch['trait_name'], uqch['champion_names'], uqch['champion_cost']]
            for uqch in traitsall[setof]['unique']
        ], row0=['{{name}}', '{{champion}}', '{{cost}}']))
        stfile.close()
