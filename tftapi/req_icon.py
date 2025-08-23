from meta_data import setlist
from meta_data import setchampions, setitems, settraits
from meta_data import set_itemstype
from meta_func import select_champions, select_items, select_traits_legal
from meta_func import download_file, geturl_extname, copy_icon_emblem2trait, copyfile_src2dst
from typing import Callable,Any
from parse_items import itemTyp
import os
from json import loads

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
    gen_req_func('tfttraits', settraits, select_traits_legal)

def classify_items_icon():
    for setof in setlist:
        itemkey2img={itemof['key']:itemof['imageUrl'] for itemof in setitems(setof)}
        for itemtyp,itemls in itemTyp[setof].items():
            if len(itemls) ==0:
                continue
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

def req_fight_attrs():
    attrsobj:dict[str,Any]={}
    with open('tftraw/specs/fight-attrs-icons.json') as attrfile:
        attrsobj=loads(attrfile.read())
        attrfile.close()

    for _, elval in attrsobj.items():
        for skey,saddr in elval.items():
            if skey not in ['url_fmt','attrs'] and type(saddr)==str:
                extname=geturl_extname(saddr)
                download_file(fileurl=saddr,filepath=f'tftspecs/icon/fights/{skey}.{extname}',timeout_sec=5)
        urlfmt=str(elval['url_fmt'])
        for attrof in elval['attrs']:
            fileurl=urlfmt.format(attrof)
            extname=geturl_extname(fileurl)
            download_file(
                fileurl=fileurl,
                filepath=f'tftspecs/icon/fights/{attrof}.{extname}',
                timeout_sec=5,
            )

def req_rewards():
    def dlbyurl(keyof:str, rwdof:Any):
        if type(rwdof)==str:
            extname=geturl_extname(rwdof)
            download_file(rwdof, f'tftspecs/icon/rewards/{keyof}.{extname}', 5)
        elif type(rwdof) == dict and 'url_fmt' in rwdof and 'val' in rwdof:
            extname=geturl_extname(rwdof['url_fmt'])
            for valof in rwdof['val']:
                download_file(str(rwdof['url_fmt']).format(valof), f'tftspecs/icon/rewards/{keyof}_{valof}.{extname}', 5)
    
    rewardsobj:dict[str,Any]={}
    with open('tftraw/specs/rewards-icons.json') as rwdifile:
        rewardsobj=loads(rwdifile.read())
        rwdifile.close()

    for rwdkey, rwdobj in rewardsobj.items():
        if rwdkey.startswith('Set'):
            for keyof, objof in rwdobj.items():
                dlbyurl(f'{rwdkey}_{keyof}', objof)
        else:
            dlbyurl(rwdkey, rwdobj)
            

if __name__ == '__main__':
    # set15.2 update, some icons download have been restricted, temp to skip it.
    for reqfn in [req_items_icon]: #[req_champions_icon, req_items_icon, req_traits_icon]:
        objof=reqfn.__name__.removeprefix('req_').removesuffix('_icon')
        print(f'icon obj: {objof}')
        reqfn()

    copy_icon_emblem2trait()
    classify_items_icon()

    req_fight_attrs()
    req_rewards()