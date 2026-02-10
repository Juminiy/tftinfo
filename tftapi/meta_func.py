# Traits Func
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
    if setof in ['set16','set15','set14','set13','set12','set11']:
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

# Champions Func
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

# Augments Func
def select_augments(setof:str, aug:dict) -> bool:
    return 'isHidden' not in aug

def no_augment_set(setof: str) -> bool:
    return setof in ['set1','set2','set3','set4','set5','set3.5','set4.5','set5.5']

# Items Func
def select_items(setof:str, itm:dict) -> bool:
    return 'isHidden' not in itm

def select_item_emblems(setof:str, itm:dict) -> bool:
    return select_items(setof, itm) and ('isEmblem' in itm or 'affectedTraitKey' in itm)

from meta_data import special_components
from meta_data import components_nickname,components_nickname_priority
from functools import cmp_to_key
def cpnt_cmp_func(cpnt1:str, cpnt2:str) -> int:
    def get_prio(cpntname:str) -> int:
        return components_nickname_priority[components_nickname[cpntname]]
    return get_prio(cpnt2)-get_prio(cpnt1)
component_cmp_key=cmp_to_key(cpnt_cmp_func)

def spatula_in_compositions(itm:dict) -> bool:
    return ('compositions' in itm) and (len(itm['compositions']) == 2) and \
            any(cpnt in special_components for cpnt in itm['compositions'])

def no_radiant_set(setof: str) -> bool:
    return setof in ['set1','set2','set3','set4','set5','set3.5','set4.5','set6']

# item classify func
def item_valid_compositions(itemof: dict) -> bool:
    return 'compositions' in itemof and len(itemof['compositions']) == 2
def item_Components(itemof:dict) -> bool:
    return 'isFromItem' in itemof
def item_Craftable(itemof:dict) -> bool:
    return item_valid_compositions(itemof) and \
            not spatula_in_compositions(itemof)
def item_Emblems(setof:str, itemof:dict) -> bool:
    return select_item_emblems(setof, itemof)
def item_Crown(itemof:dict) -> bool:
    return item_valid_compositions(itemof) and \
            itemof['compositions'][0] in special_components and \
            itemof['compositions'][1] in special_components
def item_Radiant(itemof:dict) -> bool:
    return 'isRadiant' in itemof
def item_Artifacts(itemof:dict)->bool:
    return 'isArtifact' in itemof
def item_Support(itemof:dict) -> bool:
    return 'isSupport' in itemof
item_classify={
    'Components': item_Components,
    'Craftable':  item_Craftable,
    'Emblems':    item_Emblems,
    'Crown':      item_Crown,
    'Radiant':    item_Radiant,
    'Artifacts':  item_Artifacts,
    'Support':    item_Support,
    'Special':    lambda itemof:True,
}
# Draw Grid Class
class Grid2d():
    grid2d: list[list[str]]
    row0: list[str]
    line0: list[str]
    hdr00: str
    md_hll: bool

    # grid2d:
    # - - - -
    # - - - -
    # - - - - 
    # row0:
    # - - - -
    def __init__(self, grid2d:list[list[str]], row0:list[str]|None=None, line0:list[str]|None=None, hdr00:str|None=None, md_hll:bool=False):
        # to ensure each row's line_count equal
        maxcols = max([len(gridrow) for gridrow in grid2d])
        for rowidx,gridrow in enumerate(grid2d):
            if len(gridrow) < maxcols:
                grid2d[rowidx].extend(['']*(maxcols-len(gridrow)))
        if row0 and len(row0) < maxcols:
            row0.extend(['']*(maxcols-len(row0)))
        if line0 and hdr00 and len(line0)+1 < len(grid2d):
            line0.extend(['']*(len(grid2d)-len(line0)-1))

        self.grid2d=grid2d
        self.row0=row0 or []
        self.line0=line0 or []
        self.hdr00=hdr00 or ''
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

    def md_value_hll(self, valtxt:str) -> str:
        return '' if len(valtxt)==0 \
        else valtxt if valtxt.startswith('**') and valtxt.endswith('**') \
                    else f'**{valtxt}**'

    def md_conv2txt(self, grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
        if len(row0) > 0:
            grid2d.insert(0, row0)
            if len(line0) > 0:
                line0.insert(0, hdr00)
                for i in range(len(grid2d)):
                    grid2d[i].insert(0, line0[i])

        # add **txt** for line0, row0
        if self.md_hll:
            for lineidx,_ in enumerate(grid2d[0]):
                grid2d[0][lineidx]=self.md_value_hll(grid2d[0][lineidx])
            for rowidx in range(len(grid2d)):
                grid2d[rowidx][0]=self.md_value_hll(grid2d[rowidx][0])

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
from requests.exceptions import RequestException, Timeout
from env import setlist
from meta_data import setitems
import os
toobignotdl=[
    # items in set9
    "AdaptiveImplant",              
    "CrownofDemacia",
    "HextechExoskeleton",
    "Masterworkupgrade",
    "RoboticArm",
    "Scrollofknowledge",
    "ShimmerInjector",
    "TheDarkinBlade",
    "UnstableChemtank",
    "VirulentBioware",
    
    # items in set9.5
    "AdaptiveImplant",
    "HextechExoskeleton",
    "RoboticArm",
    "ShimmerInjector",
    "UnstableChemtank",
    "VirulentBioware",
]
def download_file(fileurl: str, filepath: str, timeout_sec: float) -> tuple[str,str,float]|None:
    try:
        if os.path.exists(filepath): # already downloaded
            return None 
        # if any([filepath.find(dirpath)!=-1 for dirpath in ['tftitems/icon/set9','tftitems/icon/set9.5']]) and \
        #     any([fileurl.find(ignorekey)!=-1 for ignorekey in toobignotdl]): # too big ignore
        #     return None
        if fileurl=='https:None':    # illegal url
            return None
        fileresp=httpget(fileurl, stream=True, timeout=timeout_sec)
        fileresp.raise_for_status()
        with open(filepath, 'wb') as savefile:
            for chunk in fileresp.iter_content(chunk_size=1024):
                savefile.write(chunk)
            savefile.close()
        return None
    except Timeout as reqtimeout:
        print(f"[error] download: {fileurl}, timeout: {reqtimeout}")
        return (fileurl, filepath, timeout_sec+1)
    except RequestException as otherexcep:
        print(f"[error] download: {fileurl}, error: {otherexcep}")
        return None
            
def geturl_extname(commonurl:str) -> str:
    for extname in ['png','jpg','jpeg','svg']:
        if commonurl.endswith(extname):
            return extname
    dotidx = commonurl.rfind('.')
    quesidx = commonurl.rfind('?')
    if dotidx==-1:
        return 'jpg'
    else:
        if quesidx == -1 or quesidx < dotidx:
            return commonurl[dotidx+1:]
        else:
            return commonurl[dotidx+1:quesidx]

def copyfile_src2dst(srcpath:str, dstpath:str):
    with open(srcpath, 'rb') as srcf, \
        open(dstpath, 'wb') as dstf:
        dstf.write(srcf.read())
        srcf.close()
        dstf.close()

def copy_icon_emblem2trait() -> dict[str,str]:
    """
        return value: onlyfor traits icon used,
        affectedTraitKey -> iconpath
    """
    traitkey2img:dict[str,str]={}
    for setof in setlist:
        for itemof in setitems(setof):
            if select_item_emblems(setof, itemof):
                itemkey=itemof['key']
                extname=geturl_extname(itemof['imageUrl'])
                copyfile_src2dst(
                    srcpath=f'tftitems/icon/{setof}/{itemkey}.{extname}', 
                    dstpath=f'tfttraits/icon/{setof}/{itemkey}.{extname}',
                )
                if 'affectedTraitKey' in itemof:
                    traitkey=itemof['affectedTraitKey']
                    traitkey2img[f'{setof}-traits-{traitkey}'] = f'![{traitkey}](../tfttraits/icon/{setof}/{itemkey}.{extname})'

    return traitkey2img

def geticon_extname(pathkey:str) -> str:
    for extname in ['png','jpg','jpeg','svg']:
        if os.path.exists(f'{pathkey}.{extname}'):
            return extname
    return 'NONE'
def geticon_fullpath(pathkey:str) -> str:
    return f'{pathkey}.{geticon_extname(pathkey)}'

# Util Func
def reverse_dict_kv(dt:dict[str,str]) -> dict[str,str]:
    ndt:dict[str,str]={}
    for dtkey,dtval in dt.items():
        ndt[dtval]=dtkey
    return ndt

def str_delete(src:str, slist:list[str]) -> str:
    for sof in slist:
        src=src.replace(sof,'')
    return src