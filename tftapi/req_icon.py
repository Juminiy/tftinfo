from meta_data import setlist
from meta_data import setchampions, setitems, settraits
from meta_func import select_champions, select_traits, select_items
from meta_func import download_file
from typing import Callable,Any
import os

def req_timeout_sieve(tpls: list[tuple[str,str,float]]):
    while len(tpls) > 0:
        curtpl=tpls.pop(0)
        timeouttpl=download_file(curtpl[0], curtpl[1], curtpl[2])
        if timeouttpl:
            tpls.append(timeouttpl)

def gen_req_func(objpath:str, objfunc:Callable[[str], list[dict]], selectfunc:Callable[[str,dict],bool]):
    def get_ext_suffix(httppath:str) -> str:
        dotidx = httppath.rfind('.')
        if dotidx==-1:
            return 'jpg'
        else:
            return httppath[dotidx+1:]
    tosieve:list[tuple[str,str,float]]=[]
    for setof in setlist:
        setpath=f'{objpath}/icon/{setof}'
        os.makedirs(setpath, exist_ok=True)
        for objof in objfunc(setof):
            if selectfunc(setof, objof) and \
                'imageUrl' in objof and objof['imageUrl'] and \
                'key' in objof and objof['key']:
                fileurl="https:"+str(objof['imageUrl']).removeprefix('https:').removeprefix('http:')
                fileext=get_ext_suffix(fileurl)
                timeouttpl=download_file(
                    fileurl,
                    f"{objpath}/icon/{setof}/{objof['key']}.{fileext}",
                    2,
                )
                if timeouttpl:
                    tosieve.append(timeouttpl)
    
    req_timeout_sieve(tosieve)

def req_champions_icon():
    gen_req_func('tftchampions', setchampions, select_champions)

def req_items_icon():
    gen_req_func('tftitems', setitems, select_items)

def req_traits_icon():
    gen_req_func('tfttraits', settraits, select_traits)

for reqfn in [req_champions_icon, req_items_icon, req_traits_icon]:
    objof=reqfn.__name__.removeprefix('req_').removesuffix('_icon')
    print(f'icon obj: {objof}')
    reqfn()