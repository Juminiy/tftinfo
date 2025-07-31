from json import dumps

from env import setlist
from meta import setdata, augment_tier, augment_color, augment_color2tier
from meta import grid_fix_write

from typing import Literal

def parse_roles():
    roles:dict[str, list[dict]]={}
    for setof in setlist:
        if 'roles' in setdata[setof]:
            roles[setof] = [
                {
                    'name': roleval['name'] if 'name' in roleval else roleval['apiName'] if 'apiName' in roleval else '', 
                    'desc': [descval for descval in str(roleval['description']).removesuffix('<br><tftitemrules>Recommended Items:</tftitemrules>').split('<br>') if len(descval.strip()) > 0] if 'description' in roleval else []
                }
                for _,roleval in setdata[setof]['roles'].items()
            ]
    with open('data/roles.json', 'w+') as rolefile:
        rolefile.write(dumps(roles, ensure_ascii=False, indent=4))
        rolefile.close()

def parse_expr_desc_vars(desc: str, vars: dict) -> str:
    if len(desc) == 0 or len(vars) == 0:
        return desc
    
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
        elif str(varname).endswith('*100') and str(varname).removesuffix('*100') in vars:
            varvalue=str(float(vars[str(varname).removesuffix('*100')])*100)
            descres = descres.replace(f'@{varname}@', varvalue)
    
    # # 3). %i:scale$attri_name% -> statname
    # for icon_src, statof in stat_icons.items():
    #     descres = descres.replace(icon_src, statof)

    return descres

def parse_portals():
    portals:dict[str, list]={}
    for setof in setlist:
        if 'portals' in setdata[setof]:
            portals[setof]=[]
            for ptlval in setdata[setof]['portals']:
                curregion=ptlval['region']
                portals[setof].append(
                    { 
                        'name': ptlval['name'] if 'name' in ptlval else str(ptlval['apiName']).removeprefix(f'TFT_Portals_{curregion}'),
                        'region': curregion,
                        'desc': parse_expr_desc_vars(
                            desc=ptlval['description'] if 'description' in ptlval else ptlval['short'] if 'short' in ptlval else '', 
                            vars={eelem['name']: str(eelem['value']) for eelem in ptlval['effectAmounts'] if 'name' in eelem and 'value' in eelem} if 'effectAmounts' in ptlval else {}
                        ),
                    }
                )
    with open('data/portals.json', 'w+') as portalfile:
        portalfile.write(dumps(portals, ensure_ascii=False, indent=4))
        portalfile.close()

def parse_augmentsodds() -> dict[str, list[list[str]]]:
    setaugodds:dict[str,list[list[str]]]={}
    for setof in setlist:
        if 'augmentOdds' in setdata[setof]:
            setaugodds[setof]=[
                [augment_tier[atier] for atier in augodd['augments']]+[str(float(augodd['odds'])*100)+'%']
                for augodd in setdata[setof]['augmentOdds']
            ]
            with open(f'data/augodds/{setof}.txt', 'w+') as augoddsfile:
                augoddsfile.write(grid_fix_write(
                    grid2d=setaugodds[setof].copy(),
                    row0=['Aug-1', 'Aug-2', 'Aug-3', 'Odds(%)']
                ))
                augoddsfile.close()
    return setaugodds

# can calculate augment conditional-odds
def calc_augmentodds(aug1:augment_color,aug2:augment_color,aug3:augment_color):
    def filter_augth_clrx(oddls:list[list[str]], augth:Literal[1,2,3], clrx:augment_color) -> list[list[str]]:
        return [
            oddo
            for oddo in oddls
            if clrx=='*' or oddo[augth-1] == augment_color2tier[clrx]
        ]

    # filter augodds
    augodds=parse_augmentsodds()['15']
    if aug1 != '?':
        augodds=filter_augth_clrx(augodds, 1, aug1)
    if aug2 != '?':
        augodds=filter_augth_clrx(augodds, 2, aug2)
    if aug3 != '?':
        augodds=filter_augth_clrx(augodds, 3, aug3)
    
    # recalculate augodds
    condprob:int=0
    for oddo in augodds:
        condprob+=int(float(oddo[3].removesuffix('%')))
    for oddo in augodds:
        oriodd=int(float(oddo[3].removesuffix('%')))
        totodd=str(condprob)
        oddo[3] = str(oriodd)+'/'+totodd+'='+str(100*oriodd//int(totodd))+'%'

    # if none fixit
    if len(augodds)==0:
        augodds.append([aug1,aug2,aug3,'None'])

    print(grid_fix_write(grid2d=augodds, row0=['Aug-1', 'Aug-2', 'Aug-3', 'Odds(ratio)']))
    print('-'*44)

def parse_items() -> dict:
    items:dict[str, dict[str,list[dict]]]={}
    for setof in setlist:
        items[setof]={
            'craftable': [],
            'emblem': [],
            'radiant': [],
            'artifact': [],
            'support': [],
            'special': [],
        }
        itemattr=[{
            'name': itemof['name'],
            'composition': itemof['composition'],
            'effects': itemof['effects'],
            'desc': parse_expr_desc_vars(itemof['desc'], {varm['match']:str(varm['value']) for varm in itemof['variable_matches']} if 'variable_matches' in itemof else {}),
        } for itemof in setdata[setof]['items']]
        for itemof in itemattr:
            if str(itemof['name']).startswith('Radiant'):
                items[setof]['radiant'].append(itemof)
            elif str(itemof['name']).endswith('Emblem'):
                items[setof]['emblem'].append(itemof)
            elif len(itemof['composition']) == 2:
                items[setof]['craftable'].append(itemof)
            elif 'tags' in itemof and len(itemof['tags'])>0:
                if itemof['tags'][0]=='Artifact':
                    items[setof]['artifact'].append(itemof)
                elif itemof['tags'][0]=='Support':
                    items[setof]['support'].append(itemof)
            else: 
                items[setof]['special'].append(itemof)
        with open(f'data/items/{setof}.json', 'w+') as itemsfile:
            itemsfile.write(dumps(items[setof], ensure_ascii=True, indent=4))
            itemsfile.close()
    return items

def parse_units():
    pass

def parse_augments():
    pass

def parse_traits():
    pass

def parse_armory():
    pass

for fn in [parse_roles, parse_portals, parse_augmentsodds, parse_items]:
    fn()