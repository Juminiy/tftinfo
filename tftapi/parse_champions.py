from meta_data import setchampions,setlist
from meta_func import select_champions,geticon_extname
from meta_func import Grid2d

def parse_champions_key2name() -> dict[str,dict[str,str]]:
    championkn:dict[str,dict[str,str]]={}
    for setof in setlist:
        championkn[setof]={}
        chpcost:dict[int,list[dict[str,str]]]={
            1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],10:[],
        }
        for chp in setchampions(setof):
            if not select_champions(setof, chp):
                continue
            championkn[setof][chp['key']] = chp['name']
            pcost=min(chp['cost'])
            if pcost not in chpcost:
                chpcost[pcost]=[]
            extname=geticon_extname(f'tftchampions/icon/{setof}/{chp["key"]}')
            chpcost[pcost].append({
                'key': chp['key'],
                'name': chp['name'],
                'icon': f'![{chp["key"]}](../icon/{setof}/{chp["key"]}.{extname})',
            })
        with open(f'tftchampions/md/{setof}.md', 'w+') as mdfile:
            for pcost,plist in chpcost.items():
                if len(plist)==0:
                    continue

                mdfile.write(f'# Cost: {pcost}, Count: {len(plist)}\n')
                mdfile.write(Grid2d(
                    grid2d=[
                        [chp['key'], chp['name'], chp['icon']]
                        for chp in plist
                    ],
                    row0=['key', 'name', 'icon'],
                ).__str_md__())
                mdfile.write('\n')
            mdfile.close()

    return championkn

if __name__ == '__main__':
    parse_champions_key2name()