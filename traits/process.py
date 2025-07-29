# value like that

# first we need parse each file into a obj json-that:
# {'s1': {"profession": [], "race": []}}

import os
from typing import Any,Dict


def process_dict() -> Dict[str,Any]:
    """
        return {
            's_': {
                'name': '',
                'profession': [],
                'race': [],
                '5': []
            }
        }
    """
    sdict=dict[str,Any]()
    for i in range(1,15):
        with open(f'data/s{i}.txt', 'r', encoding='utf-8') as sfile:
            wds=[line.strip() for line in sfile.readlines()]
            sdict[f's{i}'] = {}
            sdict[f's{i}']['name'] = wds[0].removeprefix('# ')
            wds=wds[1:]
            wdi=0
            while wdi < len(wds):
                while wdi < len(wds) and len(wds[wdi]) == 0:
                    wdi+=1
                starti=wdi
                while wdi < len(wds) and len(wds[wdi]) > 0:
                    wdi+=1
                cate=wds[starti].removeprefix('# ').lower()
                sdict[f's{i}'][cate] = wds[starti+1:wdi]
    
    return sdict

from json import dumps,loads
s_star_json=dumps(process_dict(), indent=4, ensure_ascii=False)
with open('s_all.json', 'w+') as sstarf:
    sstarf.write(s_star_json)
    sstarf.close()