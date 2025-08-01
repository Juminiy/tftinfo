from env import setlist

from typing import Any, Literal

from json import loads

setdata:dict[str,Any]={}
for setof in setlist:
    with open(f'data/raw/{setof}.json') as setfile:
        setdata[setof] = loads(setfile.read()) 
        setfile.close()

def grid_fix_write(grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
    if len(row0) > 0:
        grid2d.insert(0, row0)
        if len(line0) > 0:
            line0.insert(0, hdr00)
            for i in range(len(grid2d)):
                grid2d[i].insert(0, line0[i])
    
    return '\n'.join(grid_convert2_table(grid2d))

def grid_convert2_table(grid2d: list[list[str]]) -> list[str]:
    if len(grid2d) == 0 or len(grid2d[0]) == 0:
        return []
    szs:list[int]=[]
    for j in range(len(grid2d[0])):
        mxsz=0
        for i in range(len(grid2d)):
            mxsz=max(mxsz, len(grid2d[i][j]))
        szs.append(mxsz)
    
    res:list[str]=[]
    for i in range(len(grid2d)):
        resv=''
        for j in range(len(grid2d[i])):
            resv+= (f'{grid2d[i][j]:<{szs[j]}}'+(' | ' if j<len(grid2d[i])-1 else ''))
        res.append(resv)
    return res

# augment
augment_tier={
    'Tier1': 'Silver',
    'Tier2': 'Gold',
    'Tier3': 'Prismatic'
}
augment_color=Literal[
    'Silver',    'silver',    's', 'S', '1', '银', '白',
    'Gold',      'gold',      'g', 'G', '2', '金', '黄',
    'Prismatic', 'prismatic', 'p', 'P', '3', '彩',
    '?', # unknown
    '*', # anyone
]
augment_color2tier={
    'Silver':'Silver',       'silver':'Silver',       's':'Silver',    'S': 'Silver',    '1':'Silver',    '银':'Silver',  '白':'Silver',
    'Gold':'Gold',           'gold':'Gold',           'g':'Gold',      'G': 'Gold',      '2':'Gold',      '金':'Gold',    '黄':'Gold',
    'Prismatic':'Prismatic', 'prismatic':'Prismatic', 'p':'Prismatic', 'P': 'Prismatic', '3':'Prismatic', '彩':'Prismatic',
}

# icon
attr_icon={
    '%i:set14AmpIcon%': 'DA', '%i:scaleDA%': 'DA',
    '%i:goldCoins%': 'Gold',
    '%i:scaleAS%': 'AS',
    '%i:scaleRange%': 'RG',
    '%i:scaleAD%': 'AD',
    '%i:scaleArmor%': 'AR',
    '%i:scaleMR%': 'MR',
    '%i:scaleAP%': 'AP',
    '%i:scaleHealth%': 'HP',
    '%i:TFTManaRegen%': 'MP', '%i:scaleMana%': 'MP',
}