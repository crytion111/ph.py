"""查成分，查看B站关注虚拟主播成分
发送：查成分(空格)B站ID
"""
import json
from pathlib import Path

from botoy import S
from botoy.decorators import ignore_botself, on_regexp
import botoy.decorators as deco
import httpx

vtb_path = Path(__file__).absolute().parent / 'vtbs.json'

with open(vtb_path) as f:
    vtbs_data = json.load(f)

@ignore_botself
@deco.these_msgtypes('TextMsg')
def receive_group_msg(ctx):
    strCont = ctx.Content
    # print("+============>" + strCont)
    if strCont.startswith("查成分"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            uid =  args[1]
            resp = httpx.get(
                'https://account.bilibili.com/api/member/getCardByMid?mid='+uid,
                timeout=10,
            )
            ret = resp.json()
            if ret['code'] != 0:
                return

            card = ret['card']

            vtbs = []
            for mid in card['attentions']:
                mid = str(mid)
                if mid in vtbs_data:
                    vtb = vtbs_data[mid]
                    vtbs.append(f"{vtb['uname']}({mid})")

            vtb_count = len(vtbs)
            vtb_msg = '、'.join(vtbs)

            S.image(card['face'], text = card['name'] + "(" + str(card['mid']) + ")关注了 "+ str(vtb_count)+" 个vtb:\n" + str(vtb_msg))
