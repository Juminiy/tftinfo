from meta_data import setlist, augments_tier
from meta_data import setchampions, setaugments

from meta_func import no_augment_set
from meta_func import select_augments

from json import dumps

# Must Trigger
augs:dict[str,dict[str, list[dict[str,str]]]]={}
# setof -> silver/gold/prismatic -> (name, desc)
for setof in setlist:
    if no_augment_set(setof):
        continue

    ingameKeyCost={chp['ingameKey']:min(chp['cost']) for chp in setchampions(setof) }

    augs[setof] = {
        'normal': [],
        'silver': [],
        'gold': [],
        'prismatic': [],
        'champion': []
    }
    for aug in setaugments(setof):
        if not select_augments(setof, aug):
            continue
        cateof=augments_tier[aug['tier']]
        augdtl={'name': aug['name'],'desc': aug['desc']}
        if 'championIngameKey' in aug and \
            aug['championIngameKey'] and \
            len(aug['championIngameKey']) > 0:
            cateof='champion'
            setofnum=setof.removeprefix('set').removesuffix('.5')
            augdtl['champion_name']=str(aug['championIngameKey']).removeprefix(f'TFT{setofnum}_')
            augdtl['champion_cost']=ingameKeyCost[aug['championIngameKey']]
        augs[setof][cateof].append(augdtl)
    with open(f'tftaugs/{setof}.json', 'w+') as augfile:
        augfile.write(dumps(augs[setof], ensure_ascii=True, indent=4))
        augfile.close()

def augs_compare(setpre: str, setcur: str):
    setpreold={
        aug['name']: augments_tier[aug['tier']]
        for aug in setaugments(setpre)
        if select_augments(setpre, aug)
    }
    setcurnew:dict[str, list[dict[str,str]]] = {}
    for augcolor,auglist in augs[setcur].items():
        setcurnew[augcolor]=[]
        for aug in auglist:
            if aug['name'] not in setpreold:
                setcurnew[augcolor].append(aug)
    with open(f'tftaugs/{setcur}-new.json', 'w+') as s15augf:
        s15augf.write(dumps(setcurnew, ensure_ascii=True, indent=4))
        s15augf.close()

if __name__ == '__main__':
    augs_compare('set14', 'set15')