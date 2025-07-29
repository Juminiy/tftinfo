from meta_data import settraits, setchampions
from meta_data import stat_icons

from json import dumps,loads

from typing import Any

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

for fn in [set15_power_up, set13_teamup, set13_anomalies, set12_charms, set12_portal, set11_encounters, set10_portal, set9_set9dot5_portal]:
    fn()

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

trait_compare('set11', 'Fated', 'set15', 'StarGuardian')