from dotenv import load_dotenv
from os import getenv
load_dotenv()

def envvalid(value: str|None) -> bool:
    return value is not None and len(value) > 0

setliststr=getenv('SeasonList')
hlliststr=getenv('HLList')
qkliststr=getenv('QueryKeyList')
pathliststr=getenv('APIPath')
baseurl=getenv('BaseURL')

if not setliststr or not hlliststr or not qkliststr or not baseurl or not pathliststr:
    print('env not found')
    exit(1)
if not all([envvalid(enval) for enval in [setliststr,hlliststr,qkliststr,pathliststr,baseurl]]):
    print('apidata env not found')
    exit(1)

setlist=setliststr.split(',')
hllist=hlliststr.split(',')
qklist=qkliststr.split(',')
pthlist=pathliststr.split(',')

openai_apikey=getenv('OPENAI_APIKEY')
openai_baseurl=getenv('OPENAI_BASEURL')
openai_modelname=getenv('OPENAI_MODELNAME')

if not all([envvalid(enval) for enval in [openai_apikey, openai_baseurl, openai_modelname]]):
    print('openai env not found')
    exit(1)