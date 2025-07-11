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