def find_all_ch(raws: str, subs: str) -> list[int]:
    return [
        idx
        for idx in range(len(raws))
        if raws[idx]==subs
    ]
    

print([
    find_all_ch(x, '@')
    for x in ['', '@', '@ch@', '@ch1@ @ch2@', '@ch1@ @ch2@ @ch3@ @ch4@']
])
