from dotenv import load_dotenv
from os import getenv

load_dotenv()

setliststr=getenv('SETLIST')
baseurlstr=getenv('BASEURL')
pathfmtstr=getenv('PATHFMT')

if not setliststr or not baseurlstr or not pathfmtstr:
    print('env error')
    exit(1)

setlist=setliststr.split(',')
