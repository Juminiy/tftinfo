from io import TextIOWrapper

from meta_data import setname, setopentime, setlist
from meta_data import setitems, settraits, setchampions
from meta_func import Grid2d
from meta_func import select_items, select_traits, select_champions
from meta_func import geturl_extname

from parse_traits_grid import get_synergy_grid
from parse_traits_table import get_traits_table, get_unique_table
from parse_items import get_craftable_grid

def write_detail_txt(wtr: TextIOWrapper, setof: str):
    # set_name
    wtr.write("# "+setname[setof]);wtr.write('\n\n')

    # set_time
    if setof in setopentime:
        wtr.write('## TimeLine\n');wtr.write('### Date\n')
        wtr.write(str(Grid2d(
            grid2d=[[setopentime[setof], '']], 
            row0=['{{start_time}}','{{end_time}}'])))
        wtr.write('\n\n')
    # set_featured

    # set_traits
    origintbl, classtbl = get_traits_table(setof)
    wtr.write('## Traits\n')
    wtr.write('### Origins\n')
    wtr.write(str(origintbl));wtr.write('\n\n')
    wtr.write('### Classes\n')
    wtr.write(str(classtbl));wtr.write('\n\n')
    wtr.write('### Unique\n')
    wtr.write(str(get_unique_table(setof)));wtr.write('\n\n')
    wtr.write('### SynergyGrid\n')
    wtr.write(str(get_synergy_grid(setof)));wtr.write('\n\n')

    # set_items
    wtr.write('## Items\n')
    wtr.write('### CraftableGrid\n')
    wtr.write(str(get_craftable_grid(setof)))

def write_detail_md(wtr: TextIOWrapper,setof: str):
    # set_name
    wtr.write("# "+setname[setof]);wtr.write('\n\n')

    # set_time
    if setof in setopentime:
        wtr.write('## TimeLine\n');wtr.write('### Date\n')
        wtr.write(Grid2d(
            grid2d=[[setopentime[setof], '']], 
            row0=['{{start_time}}','{{end_time}}']).__str_md__())
        wtr.write('\n\n')
    # set_featured

    # set_traits
    origintbl, classtbl = get_traits_table(setof)
    wtr.write('## Traits\n')
    wtr.write('### Origins\n')
    wtr.write(origintbl.__str_md__());wtr.write('\n\n')
    wtr.write('### Classes\n')
    wtr.write(classtbl.__str_md__());wtr.write('\n\n')
    wtr.write('### Unique\n')
    wtr.write(get_unique_table(setof).__str_md__());wtr.write('\n\n')
    wtr.write('### SynergyGrid\n')
    wtr.write(get_synergy_grid(setof).__str_md__());wtr.write('\n\n')

    # set_items
    wtr.write('## Items\n')
    wtr.write('### CraftableGrid\n')
    wtr.write(get_craftable_grid(setof).__str_md__())

def md_icon(dirpath:str, iconkey:str, extname:str) -> str:
    return f'![{iconkey}]({dirpath}/{iconkey}.{extname})'

iconpath:dict[str, str]={}
for setof in setlist:
    for objof, objfn in {
        'items': setitems,
        'traits': settraits,
        'champions': setchampions,
    }.items():
        for objelem in objfn(setof):
            if 'key' in objelem and objelem['key'] and \
                'imageUrl' in objelem and objelem['imageUrl']:
                objelemkey=objelem['key']
                objelemurlext=geturl_extname(objelem['imageUrl'])
                iconpath[f'{setof}-{objof}-{objelemkey}'] = f'![{objelemkey}](../tft{objof}/icon/{setof}/{objelemkey}.{objelemurlext})'


def modify_traittbl_icon(setof: str, tbl: Grid2d) -> Grid2d:
    # modify line0: traitkey
    # modify line3: emblem composition
    for rowidx,row in enumerate(tbl.grid2d):
        tbl.grid2d[rowidx][0] = iconpath[f'{setof}-traits-{row[0]}']
        composils=row[3].split('+')
        if len(composils) == 2:
            tbl.grid2d[rowidx][3] = '+'.join([
                iconpath[f'{setof}-items-{cmpnt}']
                for cmpnt in composils
            ])

    return tbl

def modify_uniquetbl_icon(setof: str, tbl: Grid2d) -> Grid2d:
    # modify line0: traitkey
    for rowidx, row in enumerate(tbl.grid2d):
        tbl.grid2d[rowidx][0] = iconpath[f'{setof}-traits-{row[0]}']
        chmps=tbl.grid2d[rowidx][1].split('/')
        tbl.grid2d[rowidx][1] = '+'.join([
            iconpath[f'{setof}-champions-{chmp}']
            for chmp in chmps
        ])

    return tbl

def modify_syngrid_icon(setof:str, tbl: Grid2d) -> Grid2d:
    # traits
    # modify row[0][1:]
    for j in range(0, len(tbl.row0)):
        tbl.row0[j] = iconpath[f'{setof}-traits-{tbl.row0[j]}']
    # modify line0
    for i in range(1, len(tbl.line0)):
        tbl.line0[i] = iconpath[f'{setof}-traits-{tbl.line0[i]}']

    # champions
    for i in range(0, len(tbl.grid2d)):
        for j in range(0, len(tbl.grid2d[i])):
            tbl.grid2d[i][j] = '/'.join([
                iconpath[f'{setof}-champions-{chmp}']
                for chmp in tbl.grid2d[i][j].split('/')
                if len(chmp) > 0
            ])
    
    return tbl

def write_detail_md_comic(wtr: TextIOWrapper,setof: str):
    # set_name
    wtr.write("# "+setname[setof]);wtr.write('\n\n')

    # set_time
    if setof in setopentime:
        wtr.write('## TimeLine\n');wtr.write('### Date\n')
        wtr.write(Grid2d(
            grid2d=[[setopentime[setof], '']], 
            row0=['{{start_time}}','{{end_time}}']).__str_md__())
        wtr.write('\n\n')
    # set_featured

    # set_traits
    origintbl, classtbl = get_traits_table(setof)
    origintbl = modify_traittbl_icon(setof, origintbl)
    classtbl = modify_traittbl_icon(setof, classtbl)
    wtr.write('## Traits\n')
    wtr.write('### Origins\n')
    wtr.write(origintbl.__str_md__());wtr.write('\n\n')
    wtr.write('### Classes\n')
    wtr.write(classtbl.__str_md__());wtr.write('\n\n')

    wtr.write('### Unique\n')
    uniquetbl = get_unique_table(setof)
    uniquetbl = modify_uniquetbl_icon(setof, uniquetbl)
    wtr.write(uniquetbl.__str_md__());wtr.write('\n\n')

    wtr.write('### SynergyGrid\n')
    syngrid = get_synergy_grid(setof)
    syngrid = modify_syngrid_icon(setof, syngrid)
    wtr.write(syngrid.__str_md__());wtr.write('\n\n')

    # set_items
    wtr.write('## Items\n')
    wtr.write('### CraftableGrid\n')
    crafgrid = get_craftable_grid(setof)
    wtr.write(crafgrid.__str_md__())


for setof in setlist:
    # with open(f'tfttxt/{setof}.txt', 'w+') as metaf:
    #     write_detail_txt(metaf, setof)
    #     metaf.close()
    with open(f'tftmd/{setof}.md', 'w+') as mdf:
        write_detail_md(mdf, setof)
        mdf.close()
    with open(f'tftmd/{setof}-comic.md', 'w+') as mdf:
        write_detail_md_comic(mdf, setof)
        mdf.close()