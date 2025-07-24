from openai import OpenAI

from env import openai_modelname,openai_apikey,openai_baseurl

from typing import Optional,List

llmcli=OpenAI(
    api_key=openai_apikey,
    base_url=openai_baseurl,
)
modelname=openai_modelname if openai_modelname else ''

def parse_resp(respv: Optional[str]) -> dict[str,List[str]]:
    if not respv:
        return {}
    thinkst,thinked=respv.find('<think>\n'), respv.find('\n</think>\n\n')
    if thinkst==-1 or thinked==-1:
        return {'value': respv.split('\n\n'), 'think': []}
    return {
        'think': respv[8:thinked].split('\n\n'),
        'value': respv[thinked+11:].split('\n\n')
    }

def chat_resp(msgs: list) -> dict[str, List[str]]:
    resp = llmcli.chat.completions.create(messages=msgs, model=modelname)
    return parse_resp(resp.choices[0].message.content)