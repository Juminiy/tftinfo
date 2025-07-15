from get_env import setlist

from json import loads

from parse_grid import select_traits, select_champions, write_grid

from typing import Any,Dict

from json import dumps,loads

from functools import cmp_to_key

from tftdata import setdata

from parse_traits import emblem_cmp_func

# items[i].name, shortDesc, fromDesc
# Components: isFromItem
# Craftable: isNormal and len(compositions)==2
# Emblems: isEmblem
# Radiant: isRadiant
# Artifacts: isArtifact
# Support: isSupport
# SpecialItems

compnick={
    'BFSword': 'sword',             'PBEBFSword': 'sword',              'ShadowBFSword': 's-sword',
    'ChainVest': 'vest',            'PBEChainVest': 'vest',             'ShadowChainVest': 's-vest',
    'FryingPan': 'pan',             'PBEFryingPan': 'pan',              'ShadowFryingPan': 's-pan',
    'GiantsBelt': 'belt',           'PBEGiantsBelt': 'belt',            'ShadowGiantsBelt': 's-belt',
    'NeedlesslyLargeRod': 'rod',    'PBENeedlesslyLargeRod': 'rod',     'ShadowNeedlesslyLargeRod': 's-rod',
    'NegatronCloak': 'cloak',       'PBENegatronCloak': 'cloak',        'ShadowNegatronCloak': 's-cloak',
    'RecurveBow': 'bow',            'PBERecurveBow': 'bow',             'ShadowRecurveBow': 's-bow',
    'SparringGloves': 'glove',      'PBESparringGloves': 'glove',       'ShadowSparringGloves': 's-glove',
    'Spatula': 'spatula',           'PBESpatula': 'spatula',            'ShadowSpatula': 's-spatula',
    'Tearofthegoddess': 'tear',     'PBETearofthegoddess': 'tear',      'ShadowTearofthegoddess': 's-tear',
}

attrMap={
    'Attack Damage': 'AD', 'AD': 'AD',
    'Attack Speed': 'AS', 'AS': 'AS',
    'Armor': 'AR', 'AR': 'AR',
    'Magic Resist': 'MR', 'MR': 'MR',
    'Health': 'HP', 'HP': 'HP', 'health': 'HP',
    'Range': 'RG',
    'Ability Power': 'AP', 'AP': 'AP', 'Abiltiy Power': 'AP',
    'Mana': 'MP',
    'Omnivamp': 'OV',
    'Damage Amp': 'DA', 'DA': 'DA',
    'Durability': 'DR',
    'Crit Chance': 'CR', 'Critical Strike Chance': 'CR',
    'Critical Strike Damage': 'DPS', 'Critical Strike': 'DPS',
    'Dodge Chance': 'DC',
}
allstats=['AD','AS','AP','MP','AR','MR','HP']
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
                    if bfr in attrMap:
                        descs.append(aft+attrMap[bfr])
                    if aft in attrMap:
                        descs.append(bfr+attrMap[aft])

    for sepby in ['<br>', ', ']:
        if sepby in fulldesc:
            forsplitby(fulldesc.split(sepby))
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
                'compositions': '+'.join([compnick[compof] for compof in itemof['compositions']]),
                'basic_attrs': parse_attr(str(itemof['fromDesc'])),
                'add_attrs': itemof['desc'],
            })
        elif 'isEmblem' in itemof and \
            'affectedTraitKey' in itemof:
            itemTyp[setof]['embl'].append({
                'name': itemof['key'],
                'compositions': '+'.join([compnick[compof] for compof in sorted(itemof['compositions'], key=cmp_to_key(emblem_cmp_func))]) 
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
    if setof in ['set1','set2','set3','set4','set5','set3.5','set4.5']:
        continue
    crafRadiComp[setof]=[]
    radiants, craftable = itemTyp[setof]['radi'], itemTyp[setof]['craf']
    for craft in craftable:
        if str(craft['compositions']).find('spatula') != -1 or \
            str(craft['compositions']).find('pan') != -1:
            continue
        foundrad=False
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
            # print(f'{setof} {craftname} NOT FOUND Radiant OR Radient')
    with open(f'tftitems/craft-vs-radiant/{setof}.json', 'w+') as compfile:
        compfile.write(dumps(crafRadiComp[setof], ensure_ascii=True, indent='    '))
        compfile.close()


compnickComp={
    'sword': 1,  's-sword': 12,  
    'bow': 2,    's-bow': 21,       
    'vest': 3,   's-vest': 31,   
    'cloak': 4,  's-cloak': 41,  
    'rod': 5,    's-rod': 51,
    'tear': 6,   's-tear': 61, 
    'belt': 7,   's-belt': 71,   
    'glove': 8,  's-glove': 81,  
    'spatula': 9,'s-spatula': 11,
    'pan': 10,   's-pan': 13,   
}

# parse items grid
for setof in setlist:
    comps=sorted([compnick[comp['name']] for comp in itemTyp[setof]['comp']], key=lambda nickof: compnickComp[nickof])
    crafts=itemTyp[setof]['craf']
    emblems=itemTyp[setof]['embl']

    grid2d=[['']*len(comps) for _ in range(len(comps))]

    for craf in crafts:
        compnickitems=str(craf['compositions']).split('+')
        if len(compnickitems) != 2:
            continue
        grid2d[comps.index(compnickitems[0])][comps.index(compnickitems[1])] = craf['name']

    for embl in emblems:
        compnickitems=str(embl['compositions']).split('+')
        if len(compnickitems) != 2:
            continue
        compnickitems.sort(key=lambda compnick: compnickComp[compnick])
        grid2d[comps.index(compnickitems[0])][comps.index(compnickitems[1])] = embl['name']

    grid2d.insert(0, comps)
    fixline0=comps.copy()
    fixline0.insert(0, 'C1\\C2')
    for i in range(len(grid2d)):
        grid2d[i].insert(0, fixline0[i])  

    with open(f'tftitems/grid/{setof}.txt', 'w+') as gridfile:
        gridfile.write('\n'.join(write_grid(grid2d)))
        gridfile.close()