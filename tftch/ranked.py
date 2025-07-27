from winner import TFTPlayer, write_final

from typing import Literal

def player_ranked(gmsz:int, pt_or_rk:Literal['pt', 'rk'], plypts: dict[str, list[int]]):
    plys={plyname: TFTPlayer(plyname) for plyname in plypts }
    for gmround in range(gmsz):
        for plyname, plypt in plypts.items():
            plys[plyname].round(plypt[gmround] if pt_or_rk=='pt' else 9-plypt[gmround])
    
    write_final(
        'data/aolaotou_bo10.txt',
        'w',
        sorted([tftply for _, tftply in plys.items()], reverse=True)
    )
player_ranked(10, 'rk',
    {
        '慎独': [4,4,3,4,1,5,3,5,1,7],
        '教练': [7,8,8,5,7,8,5,2,4,3],
        '弃徒': [6,5,7,8,3,3,2,1,6,5],
        '红莲': [5,3,6,6,8,1,7,3,8,8],
        '幻灭': [1,7,2,1,5,7,8,8,2,4],
        '初七': [2,1,5,2,4,4,6,6,3,6],
        '胡鑫': [8,6,4,7,2,2,4,7,7,1],
        '伊泽': [3,2,1,3,6,6,1,4,5,2],
    },
)