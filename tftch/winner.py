from typing import Literal,Tuple,List,Mapping
def get_compare_lt(a:int, b:int, gt_lt:Literal[1,-1]) -> int:
    if a==b:
        return 0
    if gt_lt==-1:
        return -1 if a<b else 1
    else:
        return -1 if a>b else 1
def ltrep(nval:int) -> bool:
    assert(nval in [-1,1])
    return nval==-1

class TFTPlayer():
    accup: int          # accumulate points = sum(self.points)
    points: list[int]   # points list
    g_name: str         # gamer name (can ignore)
    d_name: str         # division name (can ignore)

    def __init__(self, g_name:str=''):
        self.g_name=g_name
        self.points=[]
        self.accup=0
    
    def round(self, pt:int):
        self.points.append(pt)
        self.accup+=pt

    def top4_count(self) -> int:
        return self.points.count(8) * 2 + \
            self.points.count(7) * 1 + \
            self.points.count(6) * 1 + \
            self.points.count(5) * 1

    def day1_day2_pts(self) -> int:
        assert(len(self.points) == 12) # or programm bugs
        return sum(self.points)

    def __lt__(self, other: 'TFTPlayer') -> bool:
        assert(len(self.points) == len(other.points)) # or programm bugs

        # total accup(bigger ranked top)
        totcmp=get_compare_lt(self.accup, other.accup, -1)
        if totcmp!=0:
            return ltrep(totcmp)

        # top4 count(bigger ranked top)
        top4cmp=get_compare_lt(self.top4_count(), other.top4_count(), -1)
        if top4cmp!=0:
            return ltrep(top4cmp)
        
        if len(self.points) == 12:
            # day1_day2 points(bigger ranked top)
            day1day2cmp=get_compare_lt(self.day1_day2_pts(), other.day1_day2_pts(), -1)
            if day1day2cmp!=0:
                return ltrep(day1day2cmp)
        
        # rank_k count(bigger ranked top)
        for k in [1,2,3,4,5,6,7,8]:
            curpt=9-k
            rank_k_cmp=get_compare_lt(self.points.count(curpt), other.points.count(curpt), -1)
            if rank_k_cmp!=0:
                return ltrep(rank_k_cmp)
        
        # rank_last point(bigger ranked top)
        for lastidx in range(len(self.points)-1, -1, -1):
            rank_last_cmp=get_compare_lt(self.points[lastidx], other.points[lastidx], -1)
            if rank_last_cmp!=0:
                return ltrep(rank_last_cmp)
        
        return False

    def __str__(self) -> str:
        return f'(accumulates: {self.accup}, points: {self.points})'
    
    def __repr__(self) -> str:
        return str(self)

def has_winner(tftps:List[TFTPlayer]) -> Tuple[TFTPlayer, bool]:
    assert(len(tftps) == 8) # or programm bugs

    race_cnt=len(tftps[0].points)

    # no candidates
    if race_cnt < 4:
        return (TFTPlayer(), False)

    for ply in tftps:
        if ply.points[race_cnt-1] == 8 and sum(ply.points[:race_cnt-1]) >= 20:
            return (ply, True)
    
    # no candidates
    return (TFTPlayer(), False)

import pandas as pd
from reverse import grid_fix_write
def write_final(fpath:str, fmode:Literal['a','w','r'], plys:List[TFTPlayer]):
    with open(fpath, fmode) as kresf: 
        kresf.write(grid_fix_write(
            grid2d=[[str(sum(plyi.points))]+[str(plyi_p) for plyi_p in plyi.points] for plyi in plys], 
            row0=['Total']+['Game'+str(idx+1) for idx in range(len(plys[0].points))],
            line0=[plyi.g_name for plyi in plys],
            hdr00='Players\\GameRound'
            ))
        kresf.write('\n\n')
        kresf.close()

# theoretical max_count games
from heapq import heapify, heappop, heappush
from functools import cmp_to_key

def calcu():
    plys=[TFTPlayer('A'), TFTPlayer('B'), TFTPlayer('C'), TFTPlayer('D'), TFTPlayer('E'), TFTPlayer('F'), TFTPlayer('G'), TFTPlayer('H')]
    curcnt=0
    while True:
        heapify(plys)
        # round each
        newplys:List[TFTPlayer]=[]
        for curpt in [8,7,6,5,4,3,2,1]:
            minply=heappop(plys)
            minply.round(curpt)
            heappush(newplys, minply)
        plys=newplys
        curcnt+=1
        curres=has_winner(plys)
        write_final('data/winner_k.txt', 'a', sorted(plys, reverse=True))
        if curres[1]:
            gm_winner=curres[0]
            print(f'game over, game_count: {curcnt}, game_winner: {gm_winner}')
            break

calcu()

# def test_tftply():
#     ply:List[TFTPlayer]=[]
#     for pt in range(8,0,-1):
#         ply0=TFTPlayer(f'{pt}')
#         ply0.round(pt)
#         heappush(ply, ply0)
#     print(ply)
#     while len(ply) > 0:
#         minply=heappop(ply)
#         print(minply)

#     ply1,ply2=TFTPlayer('A'),TFTPlayer('B')
#     ply1.round(4);ply2.round(5)
#     print(ply1 < ply2)
# test_tftply()