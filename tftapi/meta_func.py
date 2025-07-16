def select_traits(setof:str, trt:dict) -> bool:
    return count_traits_style(trt) > 1 and \
        select_traits_legal(setof, trt)

def count_traits_style(trt:dict) -> int:
    max_active_val=0
    for styleof in trt['styles']:
        if 'min' in styleof:
            max_active_val = max(max_active_val, styleof['min'])
        if 'max' in styleof:
            max_active_val = max(max_active_val, styleof['max'])
    return max_active_val

def select_traits_legal(setof:str, trt:dict) -> bool:
    cursetnum=setof.removeprefix('set').removesuffix('.5')
    if setof in ['set14','set13','set12','set11']:
        return str(trt['ingameKey']).startswith(f'TFT{cursetnum}_') and \
            'isHidden' not in trt
    elif setof in ['set10','set9','set8','set7','set6','set5']:
        return str(trt['ingameKey']).startswith(f'Set{cursetnum}_') and \
            'isHidden' not in trt
    elif setof in ['set9.5','set8.5','set7.5','set6.5','set5.5','set4.5']:
        return str(trt['ingameKey']).startswith((f'Set{cursetnum}_', f'Set{cursetnum}b_')) and \
            'isHidden' not in trt
    elif setof in ['set4','set3.5','set3','set2','set1']:
        return (str(trt['ingameKey']).startswith((f'Set{cursetnum}_')) or not str(trt['ingameKey']).startswith('Set')) and \
            'isHidden' not in trt
    return False

def select_champions(setof:str, chp:dict) -> bool:
    cursetnum=setof.removeprefix('set').removesuffix('.5')
    if setof.endswith('.5'):
        return str(chp['ingameKey']).startswith((f'TFT{cursetnum}_', 'TFT9b_','TFT8b_','TFT7b_','TFT6b_','TFT4b_')) and \
                'isHidden' not in chp
    elif setof == 'set1':
        return str(chp['ingameKey']).startswith('TFT_') and \
                'isHidden' not in chp
    else:
        return str(chp['ingameKey']).startswith(f'TFT{cursetnum}_') and \
                'isHidden' not in chp

from meta_data import special_components
from functools import cmp_to_key
def emblem_cmp_func(s1:str, s2:str) -> int:
    if s1 in special_components and s2 in special_components:
        return 0
    elif s1 in special_components:
        return -1
    elif s2 in special_components:
        return 1
    return 0
emblem_cmp_key=cmp_to_key(emblem_cmp_func)

def grid_fix_write(grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
    if len(row0) > 0 and len(line0) > 0:
        grid2d.insert(0, row0)
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