from env import setlist

from typing import Any

from meta_data import setdata

from meta_func import select_traits, select_champions, emblem_cmp_key, grid_fix_write
from meta_func import select_traits_legal, count_traits_style

def parse_stats(statsd: dict[str,str], descs:str) -> str:
    for _,sval in statsd.items():
        pass
    return ''

def get_traits_table(setof: str) -> tuple[str,str]:
    setorigins=[]
    setclasses=[]

    traits=setdata[setof]['traits']

    champions=setdata[setof]['champions']
    chmps=[(chp['name'], chp['traits']) for chp in champions['champions'] if select_champions(setof, chp)]

    items=setdata[setof]['items']
    emblems:dict[str,Any]={}
    for emb in items['items']:
        if 'isHidden' in emb:
            continue
        if 'isEmblem' in emb:
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
        elif 'affectedTraitKey' in emb and 'compositions' in emb: # fix set1,set2,set3,set4,set3.5,set4.5
            emblems[emb['affectedTraitKey']] = sorted(emb['compositions'], key=emblem_cmp_key)


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
                setorigins.append(trtdetail)
            case 'CLASS':
                setclasses.append(trtdetail)
    
    # write grid
    trtsz=len(setorigins)
    clssz=len(setclasses)
    origins2d=[]
    classes2d=[]
    for i in range(trtsz):
        trtv=setorigins[i]
        origins2d.append([str(trtv['name']), str(trtv['unit_active']), str(trtv['unit_count']), str(trtv['emblem']), ''])
    for i in range(clssz):
        clsv=setclasses[i]
        classes2d.append([str(clsv['name']), str(clsv['unit_active']), str(clsv['unit_count']), str(clsv['emblem']), ''])
    origins2d.sort(key=lambda ls: ls[0])
    classes2d.sort(key=lambda ls: ls[0])
    origins2d.insert(0, ["{{origin_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"])
    classes2d.insert(0, ["{{class_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"])

    return (grid_fix_write(origins2d),grid_fix_write(classes2d))

def get_unique_table(setof: str) -> str:
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

    setunique = []
    for trt in setdata[setof]['traits']['traits']:
        if select_traits_legal(setof, trt) and \
            count_traits_style(trt) == 1:
            setunique.append({
                'trait_name': trt['name'],
                'champion_cost': '/'.join([str(chpcost[chpname]) for chpname in trt1chp[trt['key']]]) if trt['key'] in trt1chp else '',
                'champion_names': '/'.join(trt1chp[trt['key']]) if trt['key'] in trt1chp else '',
            })
    
    return grid_fix_write(
            grid2d=[
                [uqch['trait_name'], uqch['champion_names'], uqch['champion_cost']]
                for uqch in setunique
            ], 
            row0=['{{name}}', '{{champion}}', '{{cost}}'])

for setof in setlist:
    origintbl, classtbl= get_traits_table(setof)
    uniquetbl = get_unique_table(setof)
    with open(f'tfttraits/table/{setof}.txt', 'w+') as tblfile:
        tblfile.write(origintbl)
        tblfile.write('\n\n')
        tblfile.write(classtbl)
        tblfile.write('\n\n')
        tblfile.write(uniquetbl)
        tblfile.close()