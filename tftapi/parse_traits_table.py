from typing import Any

from meta_data import settraits, setchampions, setitems

from meta_func import select_traits, select_champions, component_cmp_key
from meta_func import select_traits_legal, count_traits_style, select_item_emblems
from meta_func import spatula_in_compositions
from meta_func import Grid2d

# def parse_stats(statsd: dict[str,str], descs:str) -> str:
#     for _,sval in statsd.items():
#         pass
#     return ''

def get_traits_table(setof: str) -> tuple[Grid2d, Grid2d]:
    setorigins=[]
    setclasses=[]

    emblems:dict[str,Any]={}
    for emb in setitems(setof):
        if not select_item_emblems(setof, emb):
            continue
        if 'isEmblem' in emb:
            # key chosen
            embkey=''
            embkeyraw,embnameraw=str(emb['key']),str(emb['name'])
            if embkeyraw.endswith('Emblem') or embkeyraw.endswith('EmblemItem'):
                embkey=embkeyraw.removesuffix('Emblem').removesuffix('EmblemItem')
            elif embnameraw.endswith(' Emblem') or embnameraw.endswith(' EmblemItem'):
                embkey=embnameraw.removesuffix(' Emblem').removesuffix(' EmblemItem')
            # key chosen special
            if setof in ['set10','set8','set5'] and emb['affectedTraitKey'] != embkey:
                embkey=emb['affectedTraitKey']
            
            # composi chosen
            embcomposi=[]
            # craftable
            if spatula_in_compositions(emb):
                embcomposi = sorted(emb['compositions'], key=component_cmp_key)
            # uncraftable
            elif 'compositions' not in emb:
                embcomposi = ['uncraftable']
            emblems[embkey] = embcomposi
        elif 'affectedTraitKey' in emb and 'compositions' in emb: # fix set1,set2,set3,set4,set3.5,set4.5
            emblems[emb['affectedTraitKey']] = sorted(emb['compositions'], key=component_cmp_key)


    trt2chp:dict[str,set[str]]={}
    chmps=[(chp['key'], chp['traits']) for chp in setchampions(setof) if select_champions(setof, chp)]
    for chp in chmps:
        for trtofchp in chp[1]:
            if trtofchp in trt2chp:
                trt2chp[trtofchp].add(chp[0])
            else:
                trt2chp[trtofchp] = set([chp[0]])

    for trt in settraits(setof):
        if not select_traits(setof, trt):
            continue

        activestr0='/'.join([str(styleof['min']) for styleof in trt['styles'] if 'min' in styleof ])
        activestr1='/'.join([statkey for statkey in trt['stats']])
        activestr=activestr0 if len(activestr0) > len(activestr1) else activestr1
        trtdetail={
            'name': trt['key'],
            # 'desc': parse_stats(trt['stats'], trt['desc']),
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

    return (
        Grid2d(origins2d, row0=["{{origin_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"]),
        Grid2d(classes2d, row0=["{{class_name}}", "{{unit_active}}", "{{unit_count}}", "{{emblem}}", "{{desc}}"]),
    )

def get_unique_table(setof: str) -> Grid2d:
    trt1chp:dict[str,list[str]]={} # trait_name -> champion_name_list
    chpcost:dict[str,int]={}       # champion_name -> champion_cost
    for chp in setchampions(setof):
        chpcost[chp['key']] = min(chp['cost'])
        if select_champions(setof, chp) and \
            'traits' in chp:
            for trt0 in chp['traits']:
                if trt0 not in trt1chp:
                    trt1chp[trt0] = []
                trt1chp[trt0].append(chp['key'])

    setunique = []
    for trt in settraits(setof):
        if select_traits_legal(setof, trt) and \
            count_traits_style(trt) == 1:
            setunique.append({
                'trait_name': trt['key'],
                'champion_cost': '/'.join([str(chpcost[chpname]) for chpname in trt1chp[trt['key']]]) if trt['key'] in trt1chp else '',
                'champion_names': '/'.join(trt1chp[trt['key']]) if trt['key'] in trt1chp else '',
            })
    
    return Grid2d(
            grid2d=[
                [uqch['trait_name'], uqch['champion_names'], uqch['champion_cost']]
                for uqch in setunique
            ], 
            row0=['{{name}}', '{{champion}}', '{{cost}}'],
        )

if __name__ == '__main__':
    # for setof in setlist:
    #     origintbl, classtbl= get_traits_table(setof)
    #     uniquetbl = get_unique_table(setof)
    #     with open(f'tfttraits/table/{setof}.txt', 'w+') as tblfile:
    #         tblfile.write(str(origintbl))
    #         tblfile.write('\n\n')
    #         tblfile.write(str(classtbl))
    #         tblfile.write('\n\n')
    #         tblfile.write(str(uniquetbl))
    #         tblfile.close()
    pass