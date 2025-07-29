import requests

from env import setlist,baseurlstr,pathfmtstr

from json import dumps

for setnum in setlist:
    requrl=f'{baseurlstr}{pathfmtstr}'.format(setnum)
    print(f'request to {requrl}')
    setresp=requests.get(requrl, timeout=10)
    with open(f'data/raw/{setnum}.json', 'w+') as setfile:
        setfile.write(dumps(setresp.json(), ensure_ascii=False, indent=4))
        setfile.close()