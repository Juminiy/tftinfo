from meta_data import setlist, setdata, augments_tier

from json import dumps

augs:dict[str,dict[str, list[tuple[str,str]]]]={}
# setof -> silver/gold/prismatic -> (name, desc)
for setof in setlist:
    augs[setof] = {
        'normal': [],
        'silver': [],
        'gold': [],
        'prismatic': [],
        'champion': []
    }
    augments=setdata[setof]['augments']['augments']
    for aug in augments:
        if 'isHidden' in aug:
            continue
        cateof=augments_tier[aug['tier']]
        if 'championIngameKey' in aug and \
            aug['championIngameKey'] and \
            len(aug['championIngameKey']) > 0:
            cateof='champion'
        augs[setof][cateof].append(
            (aug['name'], aug['desc'])
        )
    with open(f'tftaugs/{setof}.json', 'w+') as augfile:
        augfile.write(dumps(augs[setof], ensure_ascii=True, indent='    '))
        augfile.close()

def augs_compare(setpre: str, setcur: str):
    if setpre not in setdata or \
        setcur not in setdata:
        print(f'error set: {setpre}, {setcur}')
        return 
    setpreold={
        aug['name']: augments_tier[aug['tier']]
        for aug in setdata[setpre]['augments']['augments']
        if 'isHidden' not in aug
    }
    setcurnew:dict[str, list[tuple[str,str]]] = {}
    for augcolor,auglist in augs[setcur].items():
        setcurnew[augcolor]=[]
        for aug in auglist:
            if aug[0] not in setpreold:
                setcurnew[augcolor].append(aug)
    with open(f'tftaugs/{setcur}-new.json', 'w+') as s15augf:
        s15augf.write(dumps(setcurnew, ensure_ascii=True, indent='    '))
        s15augf.close()

augs_compare('set14', 'set15')