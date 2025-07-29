from typing import (Dict, Any, Tuple, List)
from json import dumps,loads
from process import process_tft

def find_hard_traits() -> Dict[str,Any]:
    def parse_unit_active(actv: str) -> int:
        actvs = [aci if aci[0].isdigit() else aci[1:] for aci in actv.split('/') if len(aci)> 0]
        return int(actvs[len(actvs)-1])

    def process_count(bond_of: dict, max_active_gt:int=9, emblem_cnt_gt:int=2, setof:str='?') -> Tuple[Dict[str,Any], bool]: 
        actvunit = parse_unit_active(bond_of['unit_active'])
        unitcnt = int(bond_of['unit_count']) if str(bond_of['unit_count']).isdigit() else actvunit
        emcraftable = bool(str(bond_of['emblem']).count('+') > 0)
        if (actvunit >= max_active_gt and actvunit-unitcnt >= emblem_cnt_gt) or (actvunit-unitcnt >= emblem_cnt_gt+1):
            return (
                {
                    'max_unit_active': actvunit,
                    'emblem_count': actvunit-unitcnt-(1 if setof=='s10' else 0),
                    'emblem_craftable': emcraftable,
                }, True
            )
        # elif not emcraftable and actvunit-unitcnt>0:
        #     return (
        #         {
        #             'max_unit_active': actvunit,
        #             'current_unit': unitcnt,
        #             'emblem_craftable': emcraftable,
        #             'bond_impossible': True,
        #         },True
        #     )
        else:
            return ({}, False)

    info=process_tft()
    hard_traits:dict[str,Any]={}
    for setof, setinfo in info.items():
        # active_count >= 9 or emblem >= 2
        hard_traits[setof]={}
        # traits.origins
        for originof in setinfo['traits']['origins']:
            stat,ok=process_count(originof, setof=setof)
            if ok:
                hard_traits[setof][originof['origin_name']] = stat
        # traits.classes
        for classof in setinfo['traits']['classes']:
            stat,ok= process_count(classof, setof=setof)
            if ok:
                hard_traits[setof][classof['class_name']] = stat
    return hard_traits

hard_traits_info=dumps(find_hard_traits(), ensure_ascii=True, indent=4)
with open('data/output/tft_hard_traits.json', 'w+') as htfile:
    htfile.write(hard_traits_info)
    htfile.close()

def find_most_traits() -> List[Tuple[str, List[Tuple[str,str]]]]:
    res:Dict[str,List[Tuple[str,str]]]={}
    info=process_tft()
    for setof, setinfo in info.items():
        for classof in setinfo['traits']['classes']:
            nameof=classof['class_name']
            tpl=(setof, classof['desc'])
            if nameof in res:
                res[nameof].append(tpl)
            else:
                res[nameof]=[tpl]
    return sorted([(nameof,listof) for nameof,listof in res.items() if len(listof) >= 5], key=lambda tof: len(tof[1]), reverse=True)

most_traits_info=dumps(find_most_traits(), ensure_ascii=True, indent=4)
with open('data/output/tft_most_traits.json', 'w+') as mtfile:
    mtfile.write(most_traits_info)
    mtfile.close()