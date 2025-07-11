import requests

from get_env import setlist,hllist,qklist,pthlist,baseurl

from json import dumps, loads
for setof in setlist:
    for pathof in pthlist:
        requrl=f'{baseurl}{pathof}?{qklist[0]}={hllist[0]}&{qklist[1]}={setof}'
        print(f'request to {requrl}')
        setresp=requests.get(requrl)
        with open(f'tftraw/{setof}-{pathof}.json', 'w+') as setjsonf:
            setjsonf.write(dumps(setresp.json(), ensure_ascii=False, indent='   '))
            setjsonf.close()
        setresp.close()