import requests

from dotenv import load_dotenv
from os import getenv
load_dotenv()

setliststr=getenv('SeasonList')
hlliststr=getenv('HLList')
qkliststr=getenv('QueryKeyList')
pathliststr=getenv('APIPath')
baseurl=getenv('BaseURL')
if not setliststr or not hlliststr or not qkliststr or not baseurl or not pathliststr:
    print('env not found')
    exit(1)

setlist=setliststr.split(',')
hllist=hlliststr.split(',')
qklist=qkliststr.split(',')
pthlist=pathliststr.split(',')

from json import dumps, loads
for setof in setlist:
    for pathof in pthlist:
        requrl=f'{baseurl}{pathof}?{qklist[0]}={hllist[0]}&{qklist[1]}={setof}'
        print(f'request to {requrl}')
        setresp=requests.get(requrl)
        with open(f'{setof}-{pathof}.json', 'w+') as setjsonf:
            setjsonf.write(dumps(setresp.json(), ensure_ascii=False, indent='   '))
            setjsonf.close()
        setresp.close()