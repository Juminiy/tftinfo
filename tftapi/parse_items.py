from env import setlist

from typing import Any,Dict

from json import dumps

from meta_data import setdata, components_nickname, attributes_nickname, allstats, components_nickname_priority
from meta_data import craft2radiant_name_set5dot5, craft2radiant_name

from meta_func import emblem_cmp_key, grid_fix_write
from meta_func import no_radiant_set

# from colorama import Fore, Style

def parse_attr(fulldesc: str) -> list[str]:
    if len(fulldesc) == 0:
        return []
    descs:list[str]=[]
    def forsplitby(splitfor: list[str]):
        for desci in splitfor:
            descls= desci.split(' ')
            for wordcnt in [1,2,3]:
                if len(descls) > wordcnt:
                    bfr,aft=' '.join(descls[:wordcnt]),' '.join(descls[wordcnt:])
                    if bfr in attributes_nickname:
                        descs.append(aft+attributes_nickname[bfr])
                    if aft in attributes_nickname:
                        descs.append(bfr+attributes_nickname[aft])

    for sepby in ['<br>', ', ', '\r\n']:
        if sepby in fulldesc:
            forsplitby(fulldesc.split(sepby))
            break
    if len(descs) == 0:
        forsplitby([fulldesc])
        if fulldesc.find('All Stats') != -1:
            descs.extend([ fulldesc.split(' ')[0] + statof for statof in allstats])
    # if len(descs) == 0:
    #     print(fulldesc)
    return descs

itemTyp:Dict[str,Any] = {}

# dump itemTyp
for setof in setlist:
    itemTyp[setof]={
        'comp': [], # Components
        'craf': [], # Craftable
        'embl': [], # Emblems
        'radi': [], # Radiant
        'arti': [], # Artifacts
        'supp': [], # Support
        'spec': [], # Special
    }
    items=setdata[setof]['items']
    for itemof in items['items']:
        if 'isHidden' in itemof:
            continue
        if 'isFromItem' in itemof:
            itemTyp[setof]['comp'].append({
                'name': itemof['key'],
                'attr': itemof['shortDesc'],
            })
        elif 'isNormal' in itemof and \
            'compositions' in itemof and len(itemof['compositions']) == 2 and \
                'Spatula' not in itemof['compositions'] and \
                'FryingPan' not in itemof['compositions']:
            itemTyp[setof]['craf'].append({
                'name': itemof['key'],
                'compositions': '+'.join(sorted([components_nickname[compof] for compof in itemof['compositions']], key=lambda nickof: components_nickname_priority[nickof])),
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        elif 'isEmblem' in itemof and \
            'affectedTraitKey' in itemof:
            itemTyp[setof]['embl'].append({
                'name': itemof['key'],
                'compositions': '+'.join([components_nickname[compof] for compof in sorted(itemof['compositions'], key=emblem_cmp_key)]) 
                                if 'compositions' in itemof and len(itemof['compositions']) == 2
                                else '',
                'gain_trait': itemof['affectedTraitKey'],
                'add_attrs': itemof['desc'],
            })
        elif 'isRadiant' in itemof:
            itemTyp[setof]['radi'].append({
                'name': itemof['key'],
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        elif 'isArtifact' in itemof:
            itemTyp[setof]['arti'].append({
                'name': itemof['key'],
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        elif 'isSupport' in itemof:
            itemTyp[setof]['supp'].append({
                'name': itemof['key'],
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        else:
            itemTyp[setof]['spec'].append({
                'name': itemof['key'],
                'attrs': itemof['desc'],
            })

    with open(f'tftitems/{setof}.json', 'w+') as itemsfile:
        itemsfile.write(dumps(itemTyp[setof], ensure_ascii=True, indent='    '))
        itemsfile.close()



# compare radiant and craftable
crafRadiComp:Dict[str,Any]={}
for setof in setlist:
    if no_radiant_set(setof):
        continue
    crafRadiComp[setof]=[]
    radiants, craftable = itemTyp[setof]['radi'], itemTyp[setof]['craf']
    radnames=[raitem['name'] for raitem in radiants]

    def found_by_namemap(craftitem: dict) -> bool:
        craft2rad=craft2radiant_name if setof != 'set5.5' else craft2radiant_name_set5dot5
        if craftitem['name'] in craft2rad and \
            craft2rad[craftitem['name']] in radnames:
            crafRadiComp[setof].append({
                'craftable': craftitem,
                'radiant': radiants[radnames.index(craft2rad[craftitem['name']])],
            })
            return True
        return False

    for craft in craftable:
        if str(craft['compositions']).find('spatula') != -1 or \
            str(craft['compositions']).find('pan') != -1:
            continue

        foundrad=found_by_namemap(craft)
        if foundrad:
            continue
        
        for radiant in radiants:
            if str(radiant['name']).removeprefix('Radiant').removesuffix('Radiant').removeprefix('Radient').removesuffix('Radient') == \
                craft['name']:
                crafRadiComp[setof].append({
                    'craftable': craft,
                    'radiant': radiant,
                })
                foundrad=True
                break
        
        if not foundrad:
            craftname=craft['name']
            # print(f'{Fore.RED}{setof} {Fore.GREEN}{craftname}{Style.RESET_ALL} NOT FOUND Radiant OR Radient')
    with open(f'tftitems/craft-vs-radiant/{setof}.json', 'w+') as compfile:
        compfile.write(dumps(crafRadiComp[setof], ensure_ascii=True, indent='    '))
        compfile.close()



# parse items grid
for setof in setlist:
    comps=sorted([components_nickname[comp['name']] for comp in itemTyp[setof]['comp']], key=lambda nickof: components_nickname_priority[nickof])
    crafts=itemTyp[setof]['craf']
    emblems=itemTyp[setof]['embl']

    grid2d=[['']*len(comps) for _ in range(len(comps))]

    for craf in crafts:
        compnickitems=str(craf['compositions']).split('+')
        if len(compnickitems) != 2:
            continue
        c1idx,c2idx=comps.index(compnickitems[0]),comps.index(compnickitems[1])
        grid2d[min(c1idx, c2idx)][max(c1idx, c2idx)] = craf['name']

    for embl in emblems:
        compnickitems=str(embl['compositions']).split('+')
        if len(compnickitems) != 2:
            continue
        compnickitems.sort(key=lambda compnick: components_nickname_priority[compnick])
        grid2d[comps.index(compnickitems[0])][comps.index(compnickitems[1])] = embl['name']
    
    with open(f'tftitems/grid/{setof}.txt', 'w+') as gridfile:
        gridfile.write(grid_fix_write(grid2d, comps.copy(), comps.copy(), 'C1\\C2'))
        gridfile.close()



# compare different set same-components-items to craftable
craftitems:Dict[str,list[tuple[str,str]]]={}
for setof in setlist:
    # if setof in ['set15']:
    #     continue
    crafts=itemTyp[setof]['craf']

    for craf in crafts:
        composi=craf['compositions']
        if composi in craftitems:
            craftitems[composi].append((setof, craf['name']))
        else:
            craftitems[composi] = []
with open('tftitems/craft-change.json', 'w+') as craftschangef:
    craftschangef.write(dumps(craftitems, ensure_ascii=True, indent='    '))
    craftschangef.close()

itemchset:dict[str,int]={}
composich:list[str]=[]
for composi,setsitem in craftitems.items():
    chdesc:list[str]=[]
    for i in range(1,len(setsitem)):
        if setsitem[i][1] != setsitem[i-1][1]:
            chdesc.extend([f'{setsitem[i-1][1]}({setsitem[i-1][0]})', f'{setsitem[i][1]}({setsitem[i][0]})'])
            if setsitem[i][0] not in itemchset:
                itemchset[setsitem[i][0]]=1
            else:
                itemchset[setsitem[i][0]]+=1
    if len(chdesc) > 0:
        import pandas as pd
        chdesc = pd.unique(pd.Series(chdesc)).tolist()
        chdescstr=' -> '.join(chdesc)
        composich.append(f'{composi}: {chdescstr}')
with open('tftitems/craft-change.txt', 'w+') as craftchf:
    craftchf.write('\n'.join(composich)+f'\n\n{itemchset}')
    craftchf.close()