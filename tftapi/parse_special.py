from meta_data import setdata

from json import dumps,loads

from typing import Any

def set15_power_up():
    set15_traits=setdata['set15']['traits']['traits']
    set15_powerups=[
        {
            'name': trt['name'],
            'stats': trt['stats']
        }
        for trt in set15_traits
        if str(trt['ingameKey']).startswith('TFT15_MechanicTrait_')
    ]
    with open('tftspecs/set15-powerups.json', 'w+') as pwerupf:
        pwerupf.write(dumps(set15_powerups, ensure_ascii=True, indent='    '))
        pwerupf.close()

def set13_teamup():
    set13_traits=setdata['set13']['traits']['traits']
    set13_teamups=[
        {
            'key': trt['key'],
            'name': trt['name'],
            # 'styles': trt['styles'],
            'stats': trt['stats']['2'],
        }
        for trt in set13_traits
        if str(trt['ingameKey']).startswith('TFT13_Teamup_')
    ]
    with open('tftspecs/set13-teamups.json', 'w+') as tmupf:
        tmupf.write(dumps(set13_teamups, ensure_ascii=True, indent='    '))
        tmupf.close()

def set13_anomalies():
    set13_als_raw:dict[str,Any] = {}
    with open('tftraw/specs/set13-anomalies.json') as alsfile:
        set13_als_raw = loads(alsfile.read())
        alsfile.close()
    
    def find_all_ch(raws: str, subs: str) -> list[int]:
        return [idx for idx in range(len(raws)) if raws[idx]==subs]
    def ls_map_pairs(ls: list[int]) -> list[tuple[int,int]]:
        res:list[tuple[int,int]]=[]
        for i in range(0, len(ls), 2):
            res.append((ls[i], ls[i+1]))
        return res

    set13_als:list[dict[str,Any]]=[]
    for _,al in set13_als_raw.items():
        rawdesc=al['desc']['en_US']
        resdesc=str(rawdesc)
        varlist=al['variables']
        # 1). @var_name@ -> al['variables'][var_name]
        # 2). @var_name*100@ -> eval(al['variables'][var_name]*100)
        # 3). %i:scale$attri_name% -> ''
        for idpr in ls_map_pairs(find_all_ch(rawdesc, '@')):
            varname=rawdesc[idpr[0]+1:idpr[1]]
            if varname in varlist:
                resdesc = resdesc.replace(f'@{varname}@', varlist[varname])
            else:
                varvalue=str(float(varlist[str(varname).removesuffix('*100')])*100)
                resdesc = resdesc.replace(f'@{varname}@', varvalue)

        set13_als.append({
            'name': al['title']['en_US'],
            'type': al['category']['en_US'],
            'desc': resdesc,
        })
    set13_als.sort(key=lambda dv: dv['name'])
    with open('tftspecs/set13-anomalies.json', 'w+') as alsf:
        alsf.write(dumps(set13_als, ensure_ascii=True, indent='    '))
        alsf.close()

def set12_charms():
    pass

def set11_encounters():
    pass

for fn in [set15_power_up, set13_teamup, set13_anomalies, set11_encounters]:
    fn()

def trait_compare(setof0: str, trtkey0: str, setof1: str, trtkey1: str):
    def get_settraitchampion(setof:str, trtkey:str) -> dict:
        trt=next(filter(lambda trt: trt['key'] == trtkey, setdata[setof]['traits']['traits']), {})
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
                for chp in setdata[setof]['champions']['champions']
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