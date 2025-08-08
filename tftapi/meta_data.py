from env import setlist

from json import loads

from typing import Any

setdata:dict[str,Any]={}
for setof in setlist:
    setdata[setof]={}
    for elemof in ['augments', 'champions', 'items', 'traits']:
        with open(f'tftraw/{setof}-{elemof}.json') as elemfile:
            setdata[setof][elemof]=dict(loads(elemfile.read()));elemfile.close()

def setaugments(setof: str) -> list[dict]:
    return setdata[setof]['augments']['augments']
def setchampions(setof: str) -> list[dict]:
    return setdata[setof]['champions']['champions']
def setitems(setof: str) -> list[dict]:
    return setdata[setof]['items']['items']
def settraits(setof: str) -> list[dict]:
    return setdata[setof]['traits']['traits']

special_components=['Spatula', 'FryingPan', 'ShadowSpatula', 'spatula', 'pan']

components_nickname={
    'BFSword': 'sword',          'ShadowBFSword': 's-sword',            # 'PBEBFSword': 'sword',         
    'ChainVest': 'vest',         'ShadowChainVest': 's-vest',           # 'PBEChainVest': 'vest',        
    'FryingPan': 'pan',          'ShadowFryingPan': 's-pan',            # 'PBEFryingPan': 'pan',         
    'GiantsBelt': 'belt',        'ShadowGiantsBelt': 's-belt',          # 'PBEGiantsBelt': 'belt',       
    'NeedlesslyLargeRod': 'rod', 'ShadowNeedlesslyLargeRod': 's-rod',   # 'PBENeedlesslyLargeRod': 'rod',
    'NegatronCloak': 'cloak',    'ShadowNegatronCloak': 's-cloak',      # 'PBENegatronCloak': 'cloak',   
    'RecurveBow': 'bow',         'ShadowRecurveBow': 's-bow',           # 'PBERecurveBow': 'bow',        
    'SparringGloves': 'glove',   'ShadowSparringGloves': 's-glove',     # 'PBESparringGloves': 'glove',  
    'Spatula': 'spatula',        'ShadowSpatula': 's-spatula',          # 'PBESpatula': 'spatula',       
    'Tearofthegoddess': 'tear',  'ShadowTearofthegoddess': 's-tear',    # 'PBETearofthegoddess': 'tear', 
}

components_nickname_priority={
    'sword': 1,  's-sword': 11,  
    'bow': 2,    's-bow': 21,       
    'vest': 3,   's-vest': 31,   
    'cloak': 4,  's-cloak': 41,  
    'rod': 5,    's-rod': 51,
    'tear': 6,   's-tear': 61, 
    'belt': 7,   's-belt': 71,   
    'glove': 8,  's-glove': 81,  
    'spatula': 9,'s-spatula': 91,
    'pan': 10,   's-pan': 101,   
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
    '%i:scaleAS%': 'AS',
}

craft2radiant_name={
    # after set9.5                              
    'AdaptiveHelm': 'JakshotheProtean',         
    'ArcaneGauntlet': 'RadientJeweledGauntlet', 
    'BlueSentinel': 'RadientBlueBuff',
    'Guardbreaker': 'RadientStridebreaker',
    'GuardianAngel': 'RadientEdgeofNight',
    'IronWill': 'RadientGargoyleStoneplate',
    'LordsEdge': 'RadientDeathblade',
    'LudensEcho': 'RadientArchangelsStaff',
    'RedBuffItem': 'RadientRedBuff',
    'SteraksGage': 'SteraksMegashield',
    'VoidStaff': 'RadientStatikkShiv',

    # set9.5                                  
    'Chalice': 'RadientChaliceofPower',       
    'Shroud': 'RadientShroudofStillness',    

    # set7.5
    'Backhand': 'RadientBansheesClaw', 
}

craft2radiant_name_set5dot5={
    # set5.5
    'LordsEdge': 'RadiantDeathblade',
    'RapidFirecannon': 'RadiantRapidfireCannon',
    'ZzRotPortal': 'RadiantZzrotPortal',
    'LudensEcho': 'RadiantArchangelsStaff',
    'ArcaneGauntlet': 'RadiantJeweledGauntlet',
    'BlueSentinel': 'RadiantBlueBuff',
    'Chalice': 'RadiantChaliceofPower',
    'IronWill': 'RadiantGargoyleStoneplate',
    'Shroud': 'RadiantShroudofStillness',
    'Backhand': 'RadiantTrapClaw',
}

setopentime={
    'set1': '2019.07.08',
    'set2': '2019.11.07',
    'set3': '2020.03.18',
    'set4': '2020.09.16',
    'set5': '2021.04.29',
    'set6': '2021.11.04',
    'set7': '2022.06.09',
    'set8': '2022.12.07',
    'set9': '2023.06.13',
    'set10': '2023.11.21',
    'set11': '2024.03.07',
    'set12': '2024.08.01',
    'set13': '2024.11.21',
    'set14': '2025.04.02',
    'set15': '2025.08.01',
}

setname={
    'set1': '-',
    'set2': 'Elemental Hexes',
    'set3': 'Galaxies',          'set3.5': 'Galaxies Return to Stars',  
    'set4': 'Fates',             'set4.5': 'Fates Festival of Beasts',
    'set5': 'Reckoning',         'set5.5': 'Reckoning Dawn of Heroes',
    'set6': 'Gizmos & Gadgets',  'set6.5': 'Gizmos & Gadgets Neon Nights',
    'set7': 'Dragonlands',       'set7.5': 'Dragonlands Uncharted Realms',
    'set8': 'Monsters Attack',   'set8.5': 'Monsters Attack Glitched Out',
    'set9': 'Runeterra Reforged','set9.5': 'Runeterra Reforged HorizonBound',
    'set10': 'Remix Rumble',
    'set11': 'Inkborn Fables',
    'set12': "Magic N' Mayhem",
    'set13': 'Into the Arcane',
    'set14': 'CyberCity',
    'set15': 'K.O. Coliseum',
}

settrait_entertainment={
    'set1': None,
    'set2': None,
    'set3': None, 'set3.5': None,
    'set4': 'Fortune', 'set4.5': 'Fortune',
    'set5': 'Draconic', 'set5.5': 'Draconic',
    'set6': 'Mercenary', 'set6.5': 'Mercenary',
    'set7': 'Shimmerscale', 'set7.5': 'Shimmerscale',
    'set8': 'Underground', 'set8.5': 'Underground',
    'set9': 'Piltover', 'set9.5': 'Piltover',
    'set10': 'HeartSteal',
    'set11': 'Fortune',
    'set12': None,
    'set13': 'Chem-Baron',
    'set14': 'Cypher',
    'set15': 'Crystal Gambit',
}

set_specitem_keys={
    'set7': ['isShimmerscale'], 'set7.5': ['isShimmerscale'],
    'set8': ['isGadgeteen'], 'set8.5': ['isGadgeteen'],
    'set9': ['isZaun', 'isShimmerscale'], 'set9.5': ['isZaun'],
    'set11': ['isInkshadow', 'isStoryweaver'],
    'set12': ['isFaerie'],
    'set14': ['TFT14_Exotech', 'TFT14_AnimaSquad', 'Consumable', 'Etc'], # ['tags'][0]
}

set_itemstype={
    'comp': 'Components',
    'craf': 'Craftable',
    'embl': 'Emblems',
    'crow': 'Crown',
    'radi': 'Radiant',
    'arti': 'Artifacts',
    'supp': 'Support',
    'spec': 'Special',
}