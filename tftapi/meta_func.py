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
    if setof in ['set15','set14','set13','set12','set11']:
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

def select_items(setof:str, itm:dict) -> bool:
    return 'isHidden' not in itm

def select_item_emblems(setof:str, itm:dict) -> bool:
    return select_items(setof, itm) and ('isEmblem' in itm or 'affectedTraitKey' in itm)

def select_augments(setof:str, aug:dict) -> bool:
    return 'isHidden' not in aug

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

def no_radiant_set(setof: str) -> bool:
    return setof in ['set1','set2','set3','set4','set5','set3.5','set4.5','set6']

def no_augment_set(setof: str) -> bool:
    return setof in ['set1','set2','set3','set4','set5','set3.5','set4.5','set5.5']

class Grid2d():
    grid2d: list[list[str]]
    row0: list[str]
    line0: list[str]
    hdr00: str
    md_hll: bool

    def __init__(self, grid2d:list[list[str]], row0:list[str]=[], line0:list[str]=[], hdr00:str='', md_hll:bool=False):
        self.grid2d,self.row0,self.line0,self.hdr00=grid2d,row0,line0,hdr00
        self.md_hll=md_hll

    def conv2txt(self, grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
        if len(row0) > 0:
            grid2d.insert(0, row0)
            if len(line0) > 0:
                line0.insert(0, hdr00)
                for i in range(len(grid2d)):
                    grid2d[i].insert(0, line0[i])

        return '\n'.join(self.conv2table(grid2d))

    def conv2table(self, grid2d: list[list[str]]) -> list[str]:
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

    def md_conv2txt(self, grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
        if len(row0) > 0:
            grid2d.insert(0, row0)
            if len(line0) > 0:
                line0.insert(0, hdr00)
                for i in range(len(grid2d)):
                    grid2d[i].insert(0, line0[i])

        # add *txt* for line0, row0
        if self.md_hll:
            for lineidx,_ in enumerate(grid2d[0]):
                grid2d[0][lineidx]=f'**{grid2d[0][lineidx]}**'
            for rowidx in range(len(grid2d)):
                grid2d[rowidx][0]=f'**{grid2d[rowidx][0]}**'

        # add | - | for markdown Table
        grid2d.insert(1, ['-' for _ in grid2d[0]])
        return '\n'.join(self.md_conv2table(grid2d))

    def md_conv2table(self, grid2d: list[list[str]]) -> list[str]:
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
            res.append(f'| {resv} |')
        return res

    def __str_md__(self) -> str:
        return self.md_conv2txt(self.grid2d, self.row0, self.line0, self.hdr00)

    def __str_txt__(self) -> str:
        return self.conv2txt(self.grid2d, self.row0, self.line0, self.hdr00)

    def __str__(self) -> str:
        return self.__str_txt__()

    def __repr__(self) -> str:
        return str(self)

from requests import get as httpget
from requests.exceptions import RequestException
import os
def download_file(fileurl: str, filepath: str, timeout_sec: float) -> tuple[str,str,float]|None:
    try:
        if os.path.exists(filepath): # already downloaded
            return None 
        if fileurl=='https:None':    # illegal url
            return None
        fileresp=httpget(fileurl, stream=True, timeout=timeout_sec)
        fileresp.raise_for_status()
        with open(filepath, 'wb') as savefile:
            for chunk in fileresp.iter_content(chunk_size=1024):
                savefile.write(chunk)
            savefile.close()
        return None
    except RequestException as re:
        print(f"[error] download: {fileurl}, error: {re}")
        return (fileurl, filepath, timeout_sec+1)

def geturl_extname(commonurl:str) -> str:
    dotidx = commonurl.rfind('.')
    if dotidx==-1:
        return 'jpg'
    else:
        return commonurl[dotidx+1:]
