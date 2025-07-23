from io import TextIOWrapper

from meta_data import setname, setopentime, setlist
from meta_func import grid_fix_write

from parse_traits_grid import get_synergy_grid
from parse_traits_table import get_traits_table, get_unique_table
from parse_items import get_craftable_grid

def write_detail_txt(wtr: TextIOWrapper, setof: str):
    # set_name
    wtr.write("# "+setname[setof]);wtr.write('\n\n')

    # set_time
    if setof in setopentime:
        wtr.write('## TimeLine\n');wtr.write('### Date\n')
        wtr.write(grid_fix_write(
            grid2d=[[setopentime[setof], '']], 
            row0=['{{start_time}}','{{end_time}}']))
        wtr.write('\n\n')
    # set_featured

    # set_traits
    origintbl, classtbl = get_traits_table(setof)
    wtr.write('## Traits\n')
    wtr.write('### Origins\n')
    wtr.write(origintbl);wtr.write('\n\n')
    wtr.write('### Classes\n')
    wtr.write(classtbl);wtr.write('\n\n')
    wtr.write('### Unique\n')
    wtr.write(get_unique_table(setof));wtr.write('\n\n')
    wtr.write('### SynergyGrid\n')
    wtr.write(get_synergy_grid(setof));wtr.write('\n\n')

    # set_items
    wtr.write('## Items\n')
    wtr.write('### CraftableGrid\n')
    wtr.write(get_craftable_grid(setof))

for setof in setlist:
    with open(f'tfttxt/{setof}.txt', 'w+') as metaf:
        write_detail_txt(metaf, setof)
        metaf.close()