from meta_data import setlist
from meta_data import setchampions, setitems, settraits
from meta_data import set_itemstype
from meta_func import select_champions, select_traits, select_items
from meta_func import download_file, select_item_emblems, geturl_extname
from typing import Callable
from parse_items import itemTyp
import os

def req_timeout_sieve(tpls: list[tuple[str,str,float]]):
    while len(tpls) > 0:
        curtpl=tpls.pop(0)
        timeouttpl=download_file(curtpl[0], curtpl[1], curtpl[2])
        if timeouttpl:
            tpls.append(timeouttpl)

def gen_req_func(objpath:str, objfunc:Callable[[str], list[dict]], selectfunc:Callable[[str,dict],bool]):
    tosieve:list[tuple[str,str,float]]=[]
    for setof in setlist:
        setpath=f'{objpath}/icon/{setof}'
        os.makedirs(setpath, exist_ok=True)
        for objof in objfunc(setof):
            if selectfunc(setof, objof) and \
                'imageUrl' in objof and objof['imageUrl'] and \
                'key' in objof and objof['key']:
                fileurl="https:"+str(objof['imageUrl']).removeprefix('https:').removeprefix('http:')
                fileext=geturl_extname(fileurl)
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

def copyfile_src2dst(srcpath:str, dstpath:str):
    with open(srcpath, 'rb') as srcf, \
        open(dstpath, 'wb') as dstf:
        dstf.write(srcf.read())
        srcf.close()
        dstf.close()

def copy_icon_emblem2trait():
    for setof in setlist:
        for itemof in setitems(setof):
            if select_item_emblems(setof, itemof):
                itemkey=itemof['key']
                extname=geturl_extname(itemof['imageUrl'])
                copyfile_src2dst(
                    srcpath=f'tftitems/icon/{setof}/{itemkey}.{extname}', 
                    dstpath=f'tfttraits/icon/{setof}/{itemkey}.{extname}',
                )

def classify_items_icon():
    for setof in setlist:
        itemkey2img={itemof['key']:itemof['imageUrl'] for itemof in setitems(setof)}
        for itemtyp,itemls in itemTyp[setof].items():
            if len(itemls) ==0:
                break
            itemtyp=set_itemstype[itemtyp]
            os.makedirs(f'tftitems/icon/{setof}/{itemtyp}', exist_ok=True)
            for itemof in itemls:
                if 'name' not in itemof:
                    continue
                itemkey=itemof['name']
                extname=geturl_extname(itemkey2img[itemkey])
                copyfile_src2dst(
                    srcpath=f'tftitems/icon/{setof}/{itemkey}.{extname}',
                    dstpath=f'tftitems/icon/{setof}/{itemtyp}/{itemkey}.{extname}',
                )
                # os.remove(f'tftitems/icon/{setof}/{itemkey}.{extname}')

copy_icon_emblem2trait()
classify_items_icon()