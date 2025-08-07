from env import setlist

from typing import Any,Dict

from json import dumps

from meta_data import components_nickname, attributes_nickname, allstats, components_nickname_priority
from meta_data import setitems
from meta_data import craft2radiant_name_set5dot5, craft2radiant_name, special_components
from meta_data import set_specitem_keys

from meta_func import no_radiant_set
from meta_func import select_items
from meta_func import select_item_emblems
from meta_func import Grid2d

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

def filter_item_key(setof: str, itemof: dict) -> dict:
    def delkeys(keyls: list[str]):
        for itemkey in keyls:
            if itemkey in itemof:
                del itemof[itemkey]
    # del commonkeys
    delkeys(['ingameKey', 'shortDesc', 'imageUrl', 'isNormal', 'isUnique', 'isNew'])
    # set specifickeys
    match setof:
        case 'set1':
            delkeys(['fromDesc'])
        case 'set2':
            delkeys(['fromDesc'])
        case _:
            pass
    if 'name' in itemof and 'key' in itemof:
        itemof['name'] = itemof['key']
    return itemof 

def merge_trait_spec_items(setof: str, setitems: list[dict]) -> list[dict]:
    if setof not in set_specitem_keys:
        return setitems
    
    newsetls:list[dict]=[]
    if setof != 'set14':
        for istraitkey in set_specitem_keys[setof]:
            newsetls.append({
                'trait_key': istraitkey.removeprefix('is'),
                'trait_items': [itemof for itemof in setitems if istraitkey in itemof] 
            })
        for setitem in setitems:
            if all([itemkey not in set_specitem_keys[setof] for itemkey in setitem]):
                newsetls.append(setitem)
    else:
        for istraitkey in set_specitem_keys[setof]:
            newsetls.append({
                'trait_key': istraitkey.removeprefix('TFT14_'),
                'trait_items': [itemof for itemof in setitems if 'tags' in itemof and itemof['tags'][0] == istraitkey] 
            })

    return newsetls


itemTyp:Dict[str,Any] = {}
for setof in setlist:
    itemTyp[setof]={
        'comp': [], # Components
        'craf': [], # Craftable
        'embl': [], # Emblems
        'crow': [], # Crown
        'radi': [], # Radiant
        'arti': [], # Artifacts
        'supp': [], # Support
        'spec': [], # Special
    }
    def valid_composi(itemof: dict) -> bool:
        return 'compositions' in itemof and len(itemof['compositions']) == 2
    def item_composi_nick(itemof: dict) -> str:
        # return '+'.join([components_nickname[compof] for compof in sorted(itemof['compositions'], key=emblem_cmp_key)])
        return '+'.join(sorted([components_nickname[compof] for compof in itemof['compositions']], key=lambda nickof: components_nickname_priority[nickof]))

    for itemof in setitems(setof):
        if not select_items(setof, itemof):
            continue
        elif 'isFromItem' in itemof:
            itemTyp[setof]['comp'].append({
                'name': itemof['key'],
                'attr': itemof['shortDesc'],
            })
        elif valid_composi(itemof) and \
            'Spatula' not in itemof['compositions'] and \
            'FryingPan' not in itemof['compositions'] and \
            'ShadowSpatula' not in itemof['compositions']:
            itemTyp[setof]['craf'].append({
                'name': itemof['key'],
                'compositions': item_composi_nick(itemof),
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        elif select_item_emblems(setof, itemof):
            itemTyp[setof]['embl'].append({
                'name': itemof['key'],
                'compositions': item_composi_nick(itemof) if valid_composi(itemof) else '',
                'gain_trait': itemof['affectedTraitKey'] if 'affectedTraitKey' in itemof else '',
                'add_attrs': itemof['desc'],
            })
        elif valid_composi(itemof) and \
            itemof['compositions'][0] in special_components and \
            itemof['compositions'][1] in special_components:
            itemTyp[setof]['crow'].append({
                'name': itemof['key'],
                'compositions': item_composi_nick(itemof)
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
            itemTyp[setof]['spec'].append(
                filter_item_key(setof, dict(itemof).copy())
            )
    itemTyp[setof]['spec'] = merge_trait_spec_items(setof, itemTyp[setof]['spec'])

    with open(f'tftitems/{setof}.json', 'w+') as itemsfile:
        itemsfile.write(dumps(itemTyp[setof], ensure_ascii=True, indent=4))
        itemsfile.close()

def get_craftable_grid(setof: str) -> Grid2d:
    comps=sorted([components_nickname[comp['name']] for comp in itemTyp[setof]['comp']], key=lambda nickof: components_nickname_priority[nickof])
    crafts=itemTyp[setof]['craf']
    emblems=itemTyp[setof]['embl']
    crowns=itemTyp[setof]['crow']

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
    
    for crown in crowns:
        compnickitems=str(crown['compositions']).split('+')
        if len(compnickitems) != 2:
            continue
        grid2d[comps.index(compnickitems[0])][comps.index(compnickitems[1])] = crown['name']
    
    return Grid2d(grid2d, comps.copy(), comps.copy(), 'C1\\C2', True)

def compare_craftable_radiant_items():
    for setof in setlist:
        if no_radiant_set(setof):
            continue
        
        craft_radi_comp:list[dict]=[]
        radiants, craftable = itemTyp[setof]['radi'], itemTyp[setof]['craf']
        radnames=[raitem['name'] for raitem in radiants]

        def found_by_namemap(craftitem: dict) -> bool:
            craft2rad=craft2radiant_name if setof != 'set5.5' else craft2radiant_name_set5dot5
            if craftitem['name'] in craft2rad and \
                craft2rad[craftitem['name']] in radnames:
                craft_radi_comp.append({
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
                    craft_radi_comp.append({
                        'craftable': craft,
                        'radiant': radiant,
                    })
                    foundrad=True
                    break
                
            if not foundrad:
                craftname=craft['name']
                # print(f'{Fore.RED}{setof} {Fore.GREEN}{craftname}{Style.RESET_ALL} NOT FOUND Radiant OR Radient')
        with open(f'tftitems/craft-vs-radiant/{setof}.json', 'w+') as compfile:
            compfile.write(dumps(craft_radi_comp, ensure_ascii=True, indent=4))
            compfile.close()

def parse_craftable_item_change():
    craftitems:Dict[str,list[tuple[str,str]]]={}
    for setof in setlist:
        crafts=itemTyp[setof]['craf']

        for craf in crafts:
            composi=craf['compositions']
            if composi in craftitems:
                craftitems[composi].append((setof, craf['name']))
            else:
                craftitems[composi] = []
    
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

def collect_allset_spec_items():
    with open('tftitems/specs.json', 'w+') as specf:
        specf.write(dumps({
            setof: set_items['spec']
            for setof, set_items in itemTyp.items()
        }, ensure_ascii=True, indent=4))
        specf.close()

compare_craftable_radiant_items()
parse_craftable_item_change()
collect_allset_spec_items()
# for setof in setlist:
#     with open(f'tftitems/grid/{setof}.txt', 'w+') as gridfile:
#         gridfile.write(str(get_craftable_grid(setof)))
#         gridfile.close()