def grid_fix_write(grid2d: list[list[str]], row0: list[str]=[], line0: list[str]=[], hdr00: str='') -> str:
    if len(row0) > 0 and len(line0) > 0:
        grid2d.insert(0, row0)
        line0.insert(0, hdr00)
        for i in range(len(grid2d)):
            grid2d[i].insert(0, line0[i])
    
    return '\n'.join(grid_convert2_table(grid2d))

def grid_convert2_table(grid2d: list[list[str]]) -> list[str]:
    if len(grid2d) == 0 or len(grid2d[0]) == 0:
        return []
    szs:list[int]=[]
    for j in range(len(grid2d[0])):
        mxsz=0
        for i in range(len(grid2d)):
            mxsz=max(mxsz, len(grid2d[i][j]))
        szs.append(mxsz)
    
    res:list[str]=[]
    for i in range(len(grid2d)):
        resv=''
        for j in range(len(grid2d[i])):
            resv+= (f'{grid2d[i][j]:<{szs[j]}}'+(' | ' if j<len(grid2d[i])-1 else ''))
        res.append(resv)
    return res

def convert_by_reverse():
    with open('wf_cn.txt') as wfile:
        rows=wfile.readlines()
        grid2d=[row.split('|') for row in rows]
        for i in range(len(grid2d)):
            for j in range(len(grid2d[i])):
                grid2d[i][j] = grid2d[i][j].strip()
        for i in range(len(grid2d)):
            grid2d[i] = grid2d[i][::-1]
        with open('wf_cn_rev.txt', 'w+') as wrfile:
            wrfile.write(grid_fix_write(grid2d))
            wrfile.close()
        wfile.close()