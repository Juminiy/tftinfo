from meta_data import settraits, setchampions

from meta_func import select_traits, select_champions
from meta_func import Grid2d

def two_champions_slash(ch1: str, ch2: str) -> str:
    if len(ch1) > 0:
        return ch1+'/'+ch2
    else:
        return ch2

def get_synergy_grid(setof: str) -> Grid2d:
    # select traits
    origin_key:list[str]=[]
    class_key:list[str]=[]
    key2name:dict[str,str]={}
    for trt in settraits(setof):
        if not select_traits(setof, trt):
            continue
        match trt['type']:
            case 'ORIGIN':
                origin_key.append(trt['key'])
            case 'CLASS':
                class_key.append(trt['key'])
        key2name[trt['key']]=trt['name']
    origin_key.sort()
    class_key.sort()
    
    # select champions
    chmps=[(chp['key'], chp['traits']) for chp in setchampions(setof) if select_champions(setof, chp)]
    
    # champions grid
    grid2d=[['']*(len(class_key)) for _ in range(len(origin_key))]
    for chp in chmps:
        chpname=chp[0]
        chptrt=chp[1]
        for chpori in [ori for ori in chptrt if ori in origin_key]:
            for chpcls in [chpcls for chpcls in chptrt if chpcls in class_key]:
                oriidx,clsidx=origin_key.index(chpori),class_key.index(chpcls)
                grid2d[oriidx][clsidx]=two_champions_slash(grid2d[oriidx][clsidx], chpname)
    
    # first row is classls
    # clsnames=[key2name[clskey] for clskey in class_key]
    # header fix
    # orinames=[key2name[orikey] for orikey in origin_key]
    
    return Grid2d(grid2d, class_key, origin_key, 'Origins\\Classes', True)

if __name__ == '__main__':
    # for setof in setlist:
    #     with open(f'tfttraits/grid/{setof}.txt', 'w+') as setgridf:
    #         setgridf.write(str(get_synergy_grid(setof)))
    #         setgridf.close()
    pass