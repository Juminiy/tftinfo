from meta_data import settraits, setchampions
from meta_data import stat_icons, set_rewards_config
from meta_data import set_item_iconkey_fix

from json import dumps,loads

from typing import Any,Literal

from meta_func import Grid2d
from meta_data import RewardConfig
from meta_func import geticon_extname, geticon_fullpath
import os
from parse_items import parse_item_key2name

def parse_expr_desc_vars(desc: str, vars: dict) -> str:
    def find_all_ch(raws: str, subs: str) -> list[int]:
        return [idx for idx in range(len(raws)) if raws[idx]==subs]
    def ls_map_pairs(ls: list[int]) -> list[tuple[int,int]]:
        res:list[tuple[int,int]]=[]
        for i in range(0, len(ls), 2):
            res.append((ls[i], ls[i+1]))
        return res
    
    descres=desc
    # 1). @var_name@ -> al['variables'][var_name]
    # 2). @var_name*100@ -> eval(al['variables'][var_name]*100)
    for idpr in ls_map_pairs(find_all_ch(desc, '@')):
        varname=desc[idpr[0]+1:idpr[1]]
        if varname in vars:
            descres = descres.replace(f'@{varname}@', vars[varname])
        else:
            varvalue=str(float(vars[str(varname).removesuffix('*100')])*100)
            descres = descres.replace(f'@{varname}@', varvalue)
    
    # 3). %i:scale$attri_name% -> statname
    for icon_src, statof in stat_icons.items():
        descres = descres.replace(icon_src, statof)

    return descres

# Special
# Parse Set SpecialEffect
def set15_power_up():
    set15_powerups=[
        {
            'name': trt['name'],
            'stats': trt['stats']
        }
        for trt in settraits('set15')
        if str(trt['ingameKey']).startswith('TFT15_MechanicTrait_')
    ]
    with open('tftspecs/set15-powerups.json', 'w+') as pwerupf:
        pwerupf.write(dumps(set15_powerups, ensure_ascii=True, indent=4))
        pwerupf.close()

def set13_teamup():
    set13_teamups=[
        {
            'key': trt['key'],
            'name': trt['name'],
            # 'styles': trt['styles'],
            'stats': trt['stats']['2'],
        }
        for trt in settraits('set13')
        if str(trt['ingameKey']).startswith('TFT13_Teamup_')
    ]
    with open('tftspecs/set13-teamups.json', 'w+') as tmupf:
        tmupf.write(dumps(set13_teamups, ensure_ascii=True, indent=4))
        tmupf.close()

def set13_anomalies():
    set13_als_raw:dict[str,Any] = {}
    with open('tftraw/specs/set13-anomalies.json') as alsfile:
        set13_als_raw = loads(alsfile.read())
        alsfile.close()
    
    set13_als:list[dict[str,Any]]=[]
    for _,al in set13_als_raw.items():
        set13_als.append({
            'name': al['title']['en_US'],
            'type': al['category']['en_US'],
            'desc': parse_expr_desc_vars(al['desc']['en_US'], al['variables']),
        })
    set13_als.sort(key=lambda dv: dv['name'])
    with open('tftspecs/set13-anomalies.json', 'w+') as alsf:
        alsf.write(dumps(set13_als, ensure_ascii=True, indent=4))
        alsf.close()

def set12_charms():
    set12_chrms:dict[str,Any]={}
    with open('tftraw/specs/set12-charms.json') as chrmfile:
        set12_chrms=loads(chrmfile.read())
        chrmfile.close()
    chrmtype2desc={1:'economics',2:'combat',3:'random',4:'traits',5:'Xerath'}
    chrmcates:dict[str,list[dict]]={
        'economics': [],
        'combat': [],
        'random': [],
        'traits': [],
        'Xerath': []
    }
    for chrm in [
        {
            'name': chrmval['name']['en_US'],
            'cost': chrmval['cost'],
            'type': chrmval['type'],
            'tier': chrmval['tier'],
            'desc': parse_expr_desc_vars(chrmval['desc']['en_US'], chrmval['variables'])
        }
        for _, chrmval in set12_chrms.items()
    ]:
        chrmcates[chrmtype2desc[chrm['type']]].append(chrm); del chrm['type']
    with open('tftspecs/set12-charms.json', 'w+') as chrmfile:
        chrmfile.write(dumps(chrmcates, ensure_ascii=True, indent=4))
        chrmfile.close()

def set12_portal():
    portals:dict[str,Any]={}
    with open('tftraw/specs/set12-portal.json') as ptlfile:
        portals=loads(ptlfile.read())
        ptlfile.close()
    
    with open('tftspecs/set12-portal.json', 'w+') as ptlfile:
        ptlfile.write(dumps({
            ptl.removesuffix('_icon'): [
                {
                    'name': ptlval0['label']['en'],
                    'desc': ptlval0['desc']['en'],
                }
                for ptlval0 in ptlval['list']
            ]
            for ptl, ptlval in portals.items()
        }, ensure_ascii=True, indent=4))
        ptlfile.close()

def set11_encounters():
    ectrs:dict[str,Any]={}
    with open('tftraw/specs/set11-encounters.json') as ectrfile:
        ectrs=loads(ectrfile.read())
        ectrfile.close()

    def patch_nums(nums: list[int]) -> str:
        return '/'.join([str(num) for num in nums])

    with open('tftspecs/set11-encounters.json', 'w+') as ectrfile:
        ectrfile.write(dumps({
            heroname: {
                'list': [{'desc': desc['en'], 'stage': patch_nums(desc['stage']), 'round': patch_nums(desc['round'])} for desc in ectr['description']],
                'choices': [{'desc': choice['label']['en'], 'details': choice['value']['en'], 'stage': patch_nums(choice['stage']), 'round': patch_nums(choice['round'])} for choice in ectr['choiceList']]
            }
            for heroname, ectr in ectrs.items()
        }, ensure_ascii=True, indent=4))
        ectrfile.close()

def set10_portal():
    portals:dict[str,Any]={}
    with open('tftraw/specs/set10-portal.json') as ptlfile:
        portals=loads(ptlfile.read())
        ptlfile.close()
    
    with open('tftspecs/set10-portal.json', 'w+') as ptlfile:
        ptlfile.write(dumps({
            ptl.removesuffix('_icon'): [
                {
                    'name': ptlval0['label']['en'],
                    'desc': ptlval0['desc']['en']
                }
                for ptlval0 in ptlval['list']
            ]
            for ptl, ptlval in portals.items()
        }, ensure_ascii=True, indent=4))
        ptlfile.close()

def set9_set9dot5_portal():
    portals:list[dict[str,Any]]=[]
    with open('tftraw/specs/set9-portal.json') as ptlfile:
        portals=loads(ptlfile.read())
        ptlfile.close()
    
    with open('tftspecs/set9_set9.5-portal.json', 'w+') as ptlfile:
        ptlfile.write(dumps({
            ptl['name']['en']: [
                {
                    'name': ptl0['label']['en'],
                    'desc': ptl0['desc']['en'],
                    'set9.5new': ptl0['new']
                }
                for ptl0 in ptl['list']
            ]
            for ptl in portals
        }, ensure_ascii=True, indent=4))
        ptlfile.close()

def trait_compare(setof0: str, trtkey0: str, setof1: str, trtkey1: str):
    def get_settraitchampion(setof:str, trtkey:str) -> dict:
        trt=next(filter(lambda trt: trt['key'] == trtkey, settraits(setof)), {})
        return {
            'trait': {
                'key': trt['key'],
                'name': trt['name'],
                'desc': trt['desc'],
                'stats': trt['stats'],
            },
            'champions': [
                {
                    'name': chp['name'],
                    'cost': min(chp['cost']),
                    'skill_desc': chp['skill']['desc']
                }
                for chp in setchampions(setof)
                if trtkey in chp['traits']
            ]
        }

    with open(f'tfttraits/comp/{setof0}{trtkey0}_{setof1}{trtkey1}.json', 'w+') as cfile:
        cfile.write(dumps({
            f'{setof0}_{trtkey0}': get_settraitchampion(setof0, trtkey0),
            f'{setof1}_{trtkey1}': get_settraitchampion(setof1, trtkey1),
        }, ensure_ascii=True, indent=4))
        cfile.close()

# Rewards
# Parse TO Markdown (showing: text or icon; sparse or dense)
setitem_fakedkey2name=parse_item_key2name()
def parse_rewards():
    for setof, setrwds in set_rewards_config.items():
        for nameof, cfgkey in setrwds.items():
            # parse_set_rewards_scheme(setof, nameof, cfgkey, 'desc')
            # parse_set_rewards_scheme(setof, nameof, cfgkey, 'comic')
            # parse_set_rewards_scheme_sparse(setof, nameof, cfgkey, 'desc')
            parse_set_rewards_scheme_sparse(setof, nameof, cfgkey, 'comic')

def parse_set_rewards_scheme(setof:str, nameof:str, cfgkey:RewardConfig, outputtyp:Literal['desc','comic']):
    stacklevel=get_set_rewards_hard_objlist(setof, cfgkey)

    rwdgrid2d:list[list[str]]=[]
    stkkey=cfgkey['stacked_key']
    rwdkey=cfgkey['rewards_key']
    oddskey=cfgkey['rewards_odds_key']
    rwdlistkey=cfgkey['rewards_list_key']
    for eachstk in stacklevel:
        rwdrow:list[str]=[eachstk[stkkey]]
        for rwd in eachstk[rwdkey]:
            rwdodds=rwd[oddskey]
            rwdlist=' + '.join([explain_rewards(setof, rwdraw, outputtyp) for rwdraw in rwd[rwdlistkey]])
            rwdrow.append(f'{rwdodds}: {rwdlist}')
        rwdgrid2d.append(rwdrow)
        
    with open(f'tftmd/rewards/{setof}-{nameof}-{outputtyp}.md', 'w+') as rwdmd:
        rwdmd.write(
            Grid2d(
                grid2d=rwdgrid2d, 
                row0=[stkkey, rwdkey],
                md_hll=True,
            ).__str_md__()
        )
        rwdmd.close()

def parse_set_rewards_scheme_sparse(setof:str, nameof:str, cfgkey:RewardConfig,outputtyp:Literal['desc','comic']):
    stacklevel=get_set_rewards_hard_objlist(setof, cfgkey)

    with open(f'tftmd/rewards/{setof}-{nameof}-{outputtyp}-sparse.md', 'w+') as rwdmd:
        stkkey=cfgkey['stacked_key']
        rwdkey=cfgkey['rewards_key']
        oddskey=cfgkey['rewards_odds_key']
        rwdlistkey=cfgkey['rewards_list_key']
        for eachstk in stacklevel:
            rwdgrid2d:list[list[str]]=[]
            rwdmd.write(f'# {stkkey}: {eachstk[stkkey]}\n')
            for rwd in eachstk[rwdkey]:
                rwdgrid2d.append(
                    [rwd[oddskey]]+[explain_rewards(setof, rwdraw, outputtyp) for rwdraw in rwd[rwdlistkey]]
                )

            rwdmd.write(
                Grid2d(
                    grid2d=rwdgrid2d, 
                    row0=[oddskey, rwdkey],
                    md_hll=True,
                ).__str_md__()
            )
            rwdmd.write('\n')
        rwdmd.close()

def get_set_rewards_hard_objlist(setof:str, cfgkey:RewardConfig) -> list[dict[str,Any]]:
    stacklevel:list[dict[str,Any]]=[]
    setfilename=f'tftraw/specs/{setof}-rewards-hard.json'
    if not os.path.exists(setfilename):
        return []
    with open(setfilename) as rwdfile:
        rwdsobj = loads(rwdfile.read())
        for stkkeyofkey in cfgkey['stacklist_keys']:
            rwdsobj=rwdsobj[stkkeyofkey]
        stacklevel=rwdsobj
        rwdfile.close()
    return stacklevel

def explain_rewards(setof: str, desc:str, outputtyp:Literal['desc','comic']) -> str:
    """
        follow the rule in: rewards-rules.txt
    """
    def getcntval(cntval:str) -> str:
        if cntval == '1' or cntval == '' or not cntval.isnumeric():
            return ''
        else:
            return f'{cntval} * '
    
    def iconkey_fix(itemcate:str, itemname:str) -> str:
        # print(setof, itemcate, itemname)
        return setitem_fakedkey2name[setof][itemname] if itemname in setitem_fakedkey2name[setof] \
        else set_item_iconkey_fix[setof][itemcate][itemname]

    def geticonpath(pathkey:str,restricted:bool=True) -> str:
        fulliconpath=geticon_fullpath(pathkey=pathkey)
        if not os.path.exists(fulliconpath) and restricted:
            # print(f'ERROR: (1 try) NOT FOUND: Rewards iconpath {fulliconpath}')
            parsedpaths=pathkey.split('/')
            match parsedpaths[0]:
                case 'tftitems':
                    pathkey=pathkey.replace(parsedpaths[4], iconkey_fix(parsedpaths[3],parsedpaths[4]))
                    extname=geticon_extname(pathkey=pathkey)
                    fulliconpath=f'{pathkey}.{extname}'
                    if not os.path.exists(fulliconpath):
                        print(f'ERROR: (2 try) NOT FOUND: Rewards iconpath {fulliconpath}')
                case _:
                    print(f'ERROR: NOT CAUGHT CASE: {parsedpaths}')
        return fulliconpath

    descparts=desc.split(':')
    descpartsz=len(descparts)

    # Set Special Rewards
    if descparts[0].startswith('Set'):
        cntval=getcntval(descparts[descpartsz-1])
        iconpath=geticonpath(f'tftspecs/icon/rewards/{descparts[0]}_{descparts[1]}', False)
        icondesc='' if os.path.exists(iconpath) else descparts[1]
        iconpath=iconpath if os.path.exists(iconpath) else geticonpath('tftspecs/icon/rewards/mystery_item')
        return f'{cntval}{descparts[1]}' if outputtyp=='desc' else f'{cntval}{icondesc}![{descparts[1]}](../../{iconpath})'
    
    # Partial2 Rewards
    if len(descparts)<=2:
        cntval=getcntval(descparts[1]) if len(descparts)==2 else ''
        iconpath=geticonpath(f'tftspecs/icon/rewards/{descparts[0]}')
        return f'{cntval}{descparts[0]}' if outputtyp=='desc' else f'{cntval}![{descparts[0]}](../../{iconpath})'
    
    # PartialMore Rewards
    match descparts[0]:
        case 'Champion':
            starval=descparts[1]
            costval=descparts[2]
            cntval=getcntval(descparts[3])
            return f'{cntval}{starval}Star {costval}Cost Unit' if outputtyp=='desc' \
            else f'{cntval}![Unit_Star](../../tftspecs/icon/rewards/Champion_Star_{starval}.png)![Unit_Cost](../../tftspecs/icon/rewards/Champion_Cost_{costval}.png)'
        case 'Champions':
            starval=descparts[1]
            championkey=descparts[2]
            cntval=getcntval(descparts[3])
            iconpath=geticonpath(f'tftchampions/icon/{setof}/{championkey}')
            return f'{cntval}{starval}Star {championkey}' if outputtyp=='desc' \
            else f'{cntval}![Unit_Star](../../tftspecs/icon/rewards/Champion_Star_{starval}.png)![{championkey}](../../{iconpath})'
        case 'Items':
            itemtyp=descparts[1]
            itemkey=descparts[2]
            cntval=getcntval(descparts[3])
            iconpath=geticonpath(f'tftitems/icon/{setof}/{itemtyp}/{itemkey}')
            return f'{cntval}{itemkey}' if outputtyp=='desc' \
            else f'{cntval}![{itemkey}](../../{iconpath})'
        case 'fight':
            fightrwd=''
            for fightpt in descparts[1:]:
                if fightpt[0].isnumeric():
                   fightrwd=f'{fightrwd},{fightpt}' 
                else:
                    iconpath=geticonpath(f'tftspecs/icon/fights/{fightpt}')
                    fightrwd=fightpt if outputtyp=='desc' \
                    else f'{fightrwd},![{fightpt}](../../{iconpath})'
            return fightrwd.removeprefix(',')
        case _:
            print(f'ERROR: NOT FOUND: Rewards {descparts}')
            return 'NONE'
    return ''

# only for listingdetailjson phase
def gen_rewards_detail():
    rwddtlfilename='tftraw/specs/rewards-gens.txt'
    # if os.path.exists(rwddtlfilename):
    #     return

    rwdenumcnt:list[str]=[]
    with open('tftraw/specs/rewards-rules.txt') as rwdrlfile:
        rwdlines=rwdrlfile.readlines()[1:]
        rwdenumcnt=[ln[:ln.find(' ')] for ln in rwdlines]
        rwdrlfile.close()

    cntls:dict[str,list[int]]={
        'Gold': [i for i in range(1,10,1)]+[i for i in range(10,101,5)],
        '-': [1,2,3,4,5],
    }
    with open(rwddtlfilename, 'w+') as rwdgenfile:
        lss:list[str]=[]
        for rwd0 in rwdenumcnt:
            rwdparts=rwd0.split(':')
            sz=len(rwdparts)
            if sz==1 or rwdparts[sz-1]!='$cnt':
                lss.append(f'{rwd0}')
            elif rwdparts[0]=='Champion':
                for ucnt in cntls['-']:
                    for ustar in range(1,5,1):
                        for ucost in range(1,7,1):
                            lss.append(f'Champion:{ustar}:{ucost}:{ucnt}')
            elif rwdparts[0]=='Champions':
                for ustar in range(1,5,1):
                    for ucnt in cntls['-']:
                        lss.append(f'Champions:{ustar}:$key:{ucnt}')
            else:
                for cntof in cntls['Gold'] if rwdparts[0]=='Gold' else cntls['-']:
                    exceptcntall=rwd0.removesuffix(':$cnt')
                    lss.append(f'{exceptcntall}:{cntof}')

        rwdgenfile.write('\n'.join(sorted(lss)))
        rwdgenfile.close()

if __name__ == '__main__':
    for fn in [set15_power_up, set13_teamup, set13_anomalies, set12_charms, set12_portal, set11_encounters, set10_portal, set9_set9dot5_portal]:
        fn()
    
    trait_compare('set11', 'Fated', 'set15', 'StarGuardian')

    # gen_rewards_detail()
    parse_rewards()