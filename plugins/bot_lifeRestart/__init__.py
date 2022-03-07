# coding=utf-8
__doc__ = """
使用举例：人生重来

"""


from os.path import join
from .Life import Life
from .PicClass import *
import traceback
import random
from botoy import GroupMsg, S, jconfig
from botoy.decorators import equal_content, ignore_botself, on_regexp
import time


def genp(prop):
    ps = []
    tmp = prop
    while True:
        for i in range(0,4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp>=10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3]<10:
            break
        else:
            tmp = prop
            ps.clear()
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': ps[3]
    }


@ignore_botself
def receive_group_msg(ctx:GroupMsg):

    strGID = str(ctx.FromGroupId)
    strCont = ctx.Content
    strSendQQID = str(ctx.FromUserId)
    strNickName = ctx.FromNickName

    if strCont.find("人生重来") > -1 or strCont.find("人生重开") > -1 or strCont.find("/remake") > -1:
        
        Life.load(join(FILE_PATH,'data'))
        while True:
            life = Life()
            life.setErrorHandler(lambda e: traceback.print_exc())
            life.setTalentHandler(lambda ts: random.choice(ts).id)
            life.setPropertyhandler(genp)
            flag = life.choose()
            if flag:
                break

        name = strNickName
        choice = 0
        person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
        for t in life.talent.talents:
            choice = choice + 1
            person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

        person = person + "\n【基础属性】\n"
        person = person + "   美貌值:" + str(life.property.CHR)+"  "
        person = person + "智力值:" + str(life.property.INT)+"  "
        person = person + "体质值:" + str(life.property.STR)+"  "
        person = person + "财富值:" + str(life.property.MNY)+"  "
        str11111 = "这是"+name+"本次轮回的基础属性和天赋:\n" + person

        res = life.run() #命运之轮开始转动
        mes = '\n'.join('\n'.join(x) for x in res)
        str22 = str11111 + "\n\n这是"+name+"本次轮回的生平:\n" + mes

        sum = life.property.gensummary() #你的命运之轮到头了
        str33 = str22 + "\n\n这是" + name + "本次轮回的评价:\n"+sum
        strImage222 = ImgText(str33).draw_text()

        S.image(strImage222, text="你的命运正在重启....\n", at=True)

        

        # S.image(group_id=ev['group_id'], messages=mes_list)