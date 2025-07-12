from get_env import setlist

from json import loads,dumps 

from typing import (Mapping,Any,List,Sequence)

setdata:dict[str,Any]={}

for setof in setlist:
    setdata[setof]={}
    for elemof in ['augments', 'champions', 'items', 'traits']:
        with open(f'tftraw/{setof}-{elemof}.json') as elemfile:
            setdata[setof][elemof]=dict(loads(elemfile.read()));elemfile.close()