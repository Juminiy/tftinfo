from env import setlist

from json import loads

from typing import Any

setdata:dict[str,Any]={}

for setof in setlist:
    setdata[setof]={}
    for elemof in ['augments', 'champions', 'items', 'traits']:
        with open(f'tftraw/{setof}-{elemof}.json') as elemfile:
            setdata[setof][elemof]=dict(loads(elemfile.read()));elemfile.close()

special_components=['Spatula', 'FryingPan', 'ShadowSpatula', 'spatula', 'pan']

components_nickname={
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

components_nickname_priority={
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

attributes_nickname={
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

augments_tier={
    0: 'normal',
    1: 'silver',
    2: 'gold',
    3: 'prismatic',
    4: 'champion',
}

stat_icons={
    '%i:scaleAD%': 'AD',
    '%i:scaleArmor%': 'AR',
    '%i:scaleAP%': 'AP',
    '%i:scaleHealth%': 'HP',
    '%i:scaleDA%': 'DA',
}