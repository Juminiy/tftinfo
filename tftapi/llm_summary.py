from json import dumps

from meta_data import attributes_nickname, setlist, setdata

from meta_func import select_traits

from llm_client import chat_resp, modelname

def get_traits_desc(setof: str) -> list[dict]:
    resd:list[dict]=[]
    seltrts=[trt for trt in setdata[setof]['traits']['traits'] if select_traits(setof, trt)]

    for idx,trt in enumerate(seltrts):
        trtname=trt['name']
        trtdesc=trt['desc']
        trtstats=[statdesc for _,statdesc in trt['stats'].items()]
        abstract='\n'.join(chat_resp([
                {
                    'role': 'system',
                    'content': """
背景:tft羁绊数据,请根据给出的json总结格式化数据.给出的jsondesc为这个羁绊的描述,stats是这个羁绊的效果数组,
你需要根据desc和stats对羁绊总体效果进行总结,团队增益 team:{effectname}:(1/2/4/6), 羁绊内增益 bond:{effectname}:(4/6/8/10)
规则是将效果提取出来，将团队增益和羁绊内增益分开,按照增益效果数字非递减次序排列,如果有数字和%请同时保留数字和%
""",
                },
                {
                    'role': 'system',
                    'content': """
如:
desc: Your team gains 10 Armor and Magic Resist.<br><br>Bastions gain more, and the value doubles in the first 10 seconds of combat.,
stats: [18 Armor & MR, 36 Armor & MR, 70 Armor & MR; Non-Bastions gain an additional 25 Armor & MR.]
总结为 team:AR/MR:(10/10/35); bond:AR/MR:(18/36/70),first10s(36/72/140)
如果没有团队增益则忽略team,括号内分割个数为stats长度，如果总结不出数字请根据desc和stats总结出一个简短的说明,没有数字(//)不要胡编乱造
"""
                },
                {
                    'role': 'system',
                    'content': f"""
增益用字典内缩写表示，如果字典中没有则写原始字符串, 增益的缩写字典:{dumps(attributes_nickname)}
"""
                },
                {
                    'role': 'user',
                    'content': dumps({'desc': trtdesc, 'stats': trtstats})
                }
            ])['value'])
        resd.append({
            'name': trtname,
            'desc': trtdesc,
            'stats': trtstats,
            'abstract': abstract,
        })
        print(f'{setof}, bond: {trtname}, progess: {idx+1}/{len(seltrts)}')
    return resd

for setof in setlist:
    with open(f'tftllm/traitsdesc/{modelname}/{setof}.json', 'w+') as descfile:
        descfile.write(dumps(get_traits_desc(setof), ensure_ascii=True, indent='    '))
        descfile.close()