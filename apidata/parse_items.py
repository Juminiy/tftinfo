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
    'BFSword': 'sword',             'PBEBFSword': 'sword',
    'ChainVest': 'vest',            'PBEChainVest': 'sword',
    'FryingPan': 'pan',             'PBEFryingPan': 'sword',
    'GiantsBelt': 'belt',           'PBEGiantsBelt': 'sword',
    'NeedlesslyLargeRod': 'rod',    'PBENeedlesslyLargeRod': 'sword',
    'NegatronCloak': 'cloak',       'PBENegatronCloak': 'cloak',
    'RecurveBow': 'bow',            'PBERecurveBow': 'sword',
    'SparringGloves': 'glove',      'PBESparringGloves': 'sword',
    'Spatula': 'spatula',           'PBESpatula': 'sword',
    'Tearofthegoddess': 'tear',     'PBETearofthegoddess': 'sword',
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
                'compositions': '+'.join(sorted(itemof['compositions'], key=cmp_to_key(emblem_cmp_func))) 
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
    with open(f'tftitems/comp-{setof}.json', 'w+') as compfile:
        compfile.write(dumps(crafRadiComp[setof], ensure_ascii=True, indent='    '))
        compfile.close()