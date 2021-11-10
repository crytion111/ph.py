#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
from iotbot import IOTBOT, Action, FriendMsg, GroupMsg, EventMsg
import iotbot.decorators as deco
from iotbot.refine import *
from loguru import logger
import base64
import threading
import requests
import random
import time
import re
import json
import sys
import os
import io
from datetime import datetime
import copy
from builtins import str

bot = IOTBOT(157199224, log=False)
action = Action(bot, queue=False)



bSaoLeiStart = False
class MineTable:
    tableLength = 8  # 多长多宽
    mineCount = 8  # 多少雷
    cover = '*'  # 未打开
    mine = '#'  # 雷
    allGoodCount = 0  # 多少空格
    openGoodCount = 0  # 已经打开的空格
    answerTable = []  # 扫雷答案表
    flagTable = []  # 扫雷已打开标记表
    resultTable = []  # 上两张表的合成结果表

    def __init__(self):
        # 多少空格
        self.allGoodCount = self.tableLength * self.tableLength - self.mineCount
        # 初始扫雷表
        initTable = [[self.cover for _ in range(self.tableLength)] for _ in range(self.tableLength)]
        # 答案表
        self.answerTable = copy.deepcopy(initTable)
        # 记录打开标记的扫雷图   已经发现的标记为'd'=>'discover
        self.flagTable = copy.deepcopy(initTable)
        # 结果表，这是用来合成结果后展示的
        self.resultTable = copy.deepcopy(initTable)
        # 设置雷区标记,雷区标记为 "#"
        self.getAnswerTable()
        # 雷区答案表,安全区周围雷区数
        self.promptMine()

    # 扫雷表格编号 [ [0,0],[0,1],[1,0],[1,1] ]
    def getTableAddress(self):
        tableAddress = []
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                tableAddress.append([i, j])
        return tableAddress

    # 设置雷区标记,雷区标记为 "#"
    def getAnswerTable(self):
        mines = random.sample(self.getTableAddress(), self.mineCount)
        for address in mines:
            i = address[0]
            j = address[1]
            # 在扫雷初始表中设置雷区
            self.answerTable[i][j] = self.mine

    # 扫雷表各安全区周围雷区数量提示
    def promptMine(self):
        for table_i in range(self.tableLength):
            for table_j in range(self.tableLength):
                # 本格是雷区就跳过
                if self.answerTable[table_i][table_j] == self.mine:
                    continue

                flag = 0
                for around_i in range(-1, 2):
                    for around_j in range(-1, 2):
                        if (around_i == 0) and (around_j == 0):
                            continue
                        find_i = table_i + around_i
                        find_j = table_j + around_j
                        if 0 <= find_i < self.tableLength:
                            if 0 <= find_j < self.tableLength:
                                if self.answerTable[find_i][find_j] == self.mine:
                                    flag = flag + 1
                # 记录本格雷区数
                self.answerTable[table_i][table_j] = str(flag)

    # 展示扫雷表 (用答案表和打开标记表，合成结果表)
    def getNowData(self):
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                # 将已打开的
                if self.flagTable[i][j] == 'd':
                    self.resultTable[i][j] = self.answerTable[i][j]

    def printShow(self):
        global bSaoLeiStart
        self.getNowData()
        strShow = "xy 0, '1', '2', '3', '4', '5', '6', '7'\n"
        for i in range(self.tableLength):
            strShow += str(i) + str(self.resultTable[i]) +"\n"
        # 如果全部安全区都打开，就结束
        if self.openGoodCount == self.allGoodCount:
            bSaoLeiStart = False
            strShow += '==完成了!!!!==\n'
            return strShow
        else:
            return strShow

    # 已经发现的标记为'd'=>'discover'
    def checkInputAddress(self, i, j):
        # 地址是否合法
        if (not (0 <= i < self.tableLength)) or (not (0 <= j < self.tableLength)):
            return -1
        # 已打开
        if self.flagTable[i][j] == 'd':
            return 0
        # 当前位置有雷
        if self.answerTable[i][j] == self.mine:
            return 2
        # 当前附近有雷
        if self.answerTable[i][j] != '0':
            self.flagTable[i][j] = 'd'
            self.openGoodCount += 1
            return 1
        else:
            # 当前附近无雷
            self.flagTable[i][j] = 'd'
            self.openGoodCount += 1
            self.checkRound(i, j)
            return 1

    # 检查零区周围是否也为零区
    def checkRound(self, table_i, table_j):
        # 检查周围8个格
        for round_i in range(-1, 2):
            for round_j in range(-1, 2):
                # 不用检查自己
                if (round_i == 0) and (round_j == 0):
                    continue
                # 如果要检查的格从没打开
                i = table_i + round_i
                j = table_j + round_j
                if 0 <= i < self.tableLength:
                    if 0 <= j < self.tableLength:
                        if self.flagTable[i][j] != 'd':
                            # 要检查在格也是零区就递归
                            if self.answerTable[i][j] == '0':
                                self.openGoodCount += 1
                                # 先标记它已经被打开
                                self.flagTable[i][j] = 'd'
                                # 递归
                                self.checkRound(i, j)
                            # 要检查的格周围有雷，就仅标记被打开
                            elif self.answerTable[i][j] != self.mine:
                                self.openGoodCount += 1
                                self.flagTable[i][j] = 'd'

    def getLastGood(self):
        #print(str(self.allGoodCount)+"====>" + str(self.openGoodCount))
        return self.allGoodCount - self.openGoodCount

    # 触雷时展示扫雷表，与上面函数不同,它多打开了全部的雷区
    def gameOverMine(self):
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                if self.answerTable[i][j] == self.mine:
                    self.resultTable[i][j] = self.answerTable[i][j]












bGameStarted = False
title = '三和大神'
def print_status(status):
    strRes = title+"" \
                        "===========\n" \
                        "当前资金:    " + str(status["Money"])+"\n" \
                        "还债进度:    " + str(status["Debt"])+"/50000\n" \
                        "当前健康:    " + str(status["HP"])+"/100\n" \
                        "===========\n" + str(status["Message"])


    return strRes

status = {
    "Money":5,
    "HP":100,
    "Debt":50000,
    "Message":"",
    "ContinueWorkTime":0
    }

def do_once(name):
    def decorator1(func):
        def dec(*args):
            global action_stack
            action_stack[-1] = [item for item in action_stack[-1] if item[0] != name]
            result = func()
            return result
        return dec
    return decorator1

def random_success(name,posibility,reason = None):
    def decorator1(func):
        def dec(*args):
            global action_stack
            if random.random() < posibility:
                result = func()
                return result
            else:
                status["Message"] = "很遗憾，你的"+ name + "行为遇到了惨痛的失败\n"
                if reason != None :
                    status["Message"] += "那是因为" + reason
                return None
        return dec
    return decorator1

action_stack = [[]]

def pop_action_stack(func):
    def dec(*args):
        global action_stack
        result = func()
        action_stack.pop()
        return result
    return dec

def handle_input(intSelect):
    #try:
    operation_index = intSelect
    action_stack[-1][operation_index][1]()


def reflush_screen():

    strStatus = print_status(status)
    strStatus = strStatus + "\n你可以执行以下操作\n"

    for i in range(0,len(action_stack[-1])):
        strStatus = strStatus + str(i) + str(action_stack[-1][i][0])+'\n'
    return strStatus

is_exit = False

def add_operation(name,handler):
    action_stack[-1].append((name,handler))

def search_on_street():
    status["HP"] -= 2
    if random.random() < 0.2:
        status["Message"] += "你发现了一堆空瓶子！这可是能卖1块钱的！\n"
        status["Money"]   += 1
        return
    
    if random.random() < 0.4:
        status["Message"] += "你看到了一家卷帘门半拉着的洗头房，你要进去修车吗？修车一次400\n"
        action_stack.append([])
        @pop_action_stack
        def fix_car():
            p = random.random()
            status["Money"] -= 400
            if p < 0.1:
                status["Message"] = '''
当你刚刚搂着怀里的失足少女躺下，随即门外传来了一阵脚步声
一段急促的敲门声响了起来。“开门！警察，查房！”
过了一会儿，你就双手抱头，蹲在了地上。
交出了300块钱罚款之后，你终于被放了出来
                '''
                status["Money"] -= 300
            else :
                status["Message"] = '''
经过一阵子的努力，当那一刻来临的时候，你感觉浑身舒适，仿佛终于找到了属于男性的力量
你回头看了看身边背对着你的失足少女，点了一根烟，然后拍了她的背影
你甚至有一种迷幻的感觉，想要和她在一起，你赶紧甩了甩头，打消了这种想法
你把照片发到戒赌吧，配上几句“今天这车怎么样”之类的话，然后刷了刷网友回帖
随后翻过身睡着了
                '''
                status["HP"] += 50
        add_operation("修车",fix_car)

        @pop_action_stack
        def not_fix_car():
            status["Message"] = '''
你看了看那扇门，叹了一口气走开了。
修车就是这个冰冷都市中的唯一爱情吗？或者也只是和盒饭一样的快餐梦幻？
                '''
        add_operation("算了",not_fix_car)
        return
    
    if random.random() < 0.6:
        status["Message"] += "你发现了走在前面的那个人，屁股兜里露出来了半个iphone 6，你想试着偷窃吗\n"
        action_stack.append([])
        @pop_action_stack
        def steal():
            strSTTT = ( '''
你一把从别人的屁股兜里抽出了iphone 6.
但是那个人立刻转过身来，想要抓住你，你转身就开始跑。
                ''')
            p = 0
            while(p < 0.95):
                p = random.random()
                i = random.randint(0, 3)
                if int(i) > 2 :
                    status["Message"] = strSTTT + '''
你开始胡乱跑,由于你愚蠢地决策，你被抓住然后暴打一顿，还被送去了公安局
等你出来的时候，你整个人都饿瘦了一圈，感到头晕眼花
                    '''
                    status["HP"] -= 30
                    return
                catch = random.random()
                if catch < 0.2:
                    status["Message"] = strSTTT + '''
你被抓住然后暴打一顿，还被送去了公安局
等你出来的时候，你整个人都饿瘦了一圈，感到头晕眼花
                    '''
                    status["HP"] -= 30
                    return
                else:
                    strSTTT = strSTTT + ("\n你没能甩开后面的人，他还在穷追不舍\n")
                    continue
            status["Message"] = strSTTT + '''
你成功地甩开了身后追你的人，从怀里掏出了手机
你找到了一个人销赃，他告诉你，这种会被锁住的只能给你1500
你管不了那么多，气喘吁吁地对他说少废话，赶紧给钱
那个人拿着你的手机转身走进了后面的巷子
                    '''
            if random.random() < 0.2:
                status["Message"] += '''
然后再也没见他走出来，等你慌了，四处寻找，却发现没有任何他的踪影，你的手机也没了
                    '''    
            else:
                status["Message"] += '''
过了一会儿他走了出来，递给你1500块钱
                    '''    
                status["Money"] += 1500
            status["HP"] -= 20
            return
        add_operation("偷窃",steal)
        
        @pop_action_stack
        def not_steal():
            status["Message"] = '''
你把目光从别人的屁股后面移开，转而思考别的事情
                '''
            return
        add_operation("算了",not_steal)
        return

    if random.random() < 0.8:
        status["Message"] += '''
你突然收到了一条转账短信，来自你的母亲
你的母亲对你说，这是她出去做保姆攒下来的45块钱
让你吃好一点，在外照顾好自己
欠的钱，慢慢还，娘也帮你一点一点还
只要不赌，就一定能还完
                '''
        status["Money"] += 45
        return
        
    if random.random() < 1:
        status["Message"] += "翻了翻垃圾桶, 吃了点剩饭！HP+1\n"
        status["HP"]   += 1
        return
    
def init(status):
    status["Message"] = '''
欢迎游玩《三和浮尘录》，本游戏试图模拟一个三和大神的生活，从而展示另一个底层的世界

        [开端]
        当你开始网赌的时候，你听过无数人说，“不赌为赢”，但是你还是想去刺激一下，试一试
        当你输了这个月工资的时候，你一咬牙一跺脚，坚持要通过一把梭哈把整个月的工资赌回来
        当你把积蓄全部输光的时候，你已经无法收场了，你打开了各种小贷APP，开始拆东墙补西墙，寄希望于一把翻盘
        当你小贷APP的催收短信轰炸到你只能关闭手机的时候，你意识到，你和戒赌吧的老哥们就快要会和了
        当高利贷敲你家房门，群发侮辱你的短信给你所有联系人的时候，你借钱买了一张来三和的车票
        当你看到三和人才市场的大门，你终于意识到，你和那些你当笑话看的戒赌吧老哥，没有任何区别
        当你下车的时候，身上除了一张身份证，只剩下5块钱
    '''

    #===================卖身份证 ========================
    @do_once("卖身份证")
    @random_success("卖身份证",0.85,"那个找你做法人的人就是个骗子，拿了你的身份证转身就跑掉了,你的钱也没有拿回来")
    def sale_IDcard():
        status["Message"] = "你把自己的身份证卖掉换了100块钱\n"
        status["Money"]+=100
    add_operation("卖身份证",sale_IDcard)

    #===================还债务   ========================
    def pay_debt():
        status["Message"] = "你凑了一笔钱，还上了100块钱的债务\n"
        status["Money"]-= 100
        status["Debt"] -= 100
    add_operation("还100块钱的债",pay_debt)    

    #===================做日结 ========================
    @random_success("做日结",0.9,"你被骗进了限制人身自由的黑工厂，你完全顾不上别的就赶紧跑了出来")
    def do_one_day_job():
        action_stack.append([])
        status["Message"] = "你挤破头皮想要找到一份工作\n"
        if random.random() < 0.1:
            status["Message"] += "没想到一个趔趄，别人就把你从窗口挤开了，你想要挣扎，结果还挨了一拳"
            status["HP"] -= 3
        
        @pop_action_stack
        #@random_success("好好干活",0.9,"你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来")
        def work_hard():
            intRand = random.randint(1, 5)
            if intRand == 1:
                status["Message"] = "你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来"
                status["ContinueWorkTime"] = 0
                return

            status["Message"] = "你勤奋地工作了一天，获得了130块钱。\n"
            if status["ContinueWorkTime"] > 0 :
                status["Message"] += "主管对你的印象有所改善，他给你稍微加了%d块工资，以示鼓励\n"%(status["ContinueWorkTime"]*5)
            status["Message"] += "你的主管觉得你不错，告诉你如果经常来，会考虑给你加点工资"

            status["Money"]+=130 + status["ContinueWorkTime"]*5
            status["HP"] -= 30
            status["ContinueWorkTime"] += 1
        add_operation("好好干活",work_hard)

        @pop_action_stack
        #@random_success("摸鱼",0.5,"你心不在焉地摆弄着手里的焊枪，结果一不小心戳在了电路板上，你的主管忍无可忍直接让你滚犊子")
        def relax():
            intRand = random.randint(1, 2)
            if intRand != 2:
                status["Message"] = "你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来"
                return
            status["Message"] = "你摸了一天鱼\n"
            if random.random() < 0.5:
                status["Message"] += "主管并没有发现你在摸鱼，还是给你发了130块钱的工资"
                status["Money"]+=130
                status["HP"] -= 15
                status["ContinueWorkTime"] += 1
            else:
                status["Message"] += "主管发现你在摸鱼，但是对你无可奈何。他清楚地知道这里是三和，所以给了你70块钱让你早点滚蛋别来了"
                status["Money"]+=70
                status["HP"] -= 15
                status["ContinueWorkTime"] = 0
        add_operation("摸鱼",relax)
    add_operation("做日结",do_one_day_job)

    #===================去网吧 ========================
    def go_to_netbar():
        action_stack.append([])
        status["Message"] = "你走进一家网吧，花了3块钱开了1个小时的机子\n"
        @random_success("开一把撸啊撸",0.5,"你这把队友坑的要命，结果输得很惨，还被对面肆意嘲讽，气的要命")
        def play_lol():
            status["Message"] = "你决定用小号打一把撸啊撸"
            status["HP"] -= 3
        add_operation("开一把撸啊撸",play_lol)

        #加入支付宝被举报功能
        @random_success("去戒赌吧哭穷要饭",0.9,"贴吧这种不靠谱的东西你也相信？")
        def go_to_tieba():
            if random.random() < 0.5:
                status["Message"] = '''
你刚把支付宝发上去，就被人认出来，你是那个经常来吧里要饭的老哥
还没过几分钟，你的支付宝就被举报了，里面仅有的几块钱也没了
                '''
                status["Money"] -= 5
            else:
                status["Message"] = "你开始一把鼻涕一把泪地在戒赌吧说自己的遭遇，并发了自己的支付宝账号，请求有人能够给你打几块钱，没想到还真的有人上当"
                status["Money"]+=3
            status["HP"] -= 3
        add_operation("去戒赌吧哭穷要饭",go_to_tieba)

        #@random_success("开一局赔率10倍的网赌",0.2,"今天运气一点都不行，你输得非常惨")
        def gambling10():
            status["Message"] = "你打开熟悉的网络赌博平台，下了10块钱的赌注\n"
            if random.random()<0.05:
                status["Money"] += 100000000
                status["Message"] += "这波就稳了！净赚100！今晚怕是得修车庆祝一下"
            else:
                status["Money"] -= 10
                status["Message"] += "结果运气真的不站在你这边，你输了10块，怎么也得修车开开运气"
            status["HP"] -= 3
        add_operation("开一局赔率10倍的网赌",gambling10) 

        @do_once("点一碗红烧牛肉面")
        def buy_noodle():
            status["Message"] = "你买了一碗3块钱的红烧牛肉面,恢复了一些体力\n"
            status["HP"] += 3
            status["Money"] -= 3
        add_operation("点一碗红烧牛肉面",buy_noodle) 

        @pop_action_stack
        def finish_play():
            status["Message"] = "你揉了揉太阳穴，结账下机了\n"
            status["HP"] -= 1
            status["Money"] -= 3
        add_operation("结账下机",finish_play)         

    add_operation("去网吧上网",go_to_netbar)
    #     status["Money"] += 


    #===================吃挂逼面喝大水 ========================
    def eat():
        status["Message"] = "你点了一份3块钱的挂逼面和一块钱的大水，呼哧呼哧地吃了起来，增加了3点HP\n"
        status["HP"]+=3
        status["Money"]-=4
    add_operation("吃挂逼面喝大水",eat)   

    #===================在街上瞎晃荡 ========================
    def walk_on_street():
        status["Message"] = "你开始在深圳三和的街上晃荡，人来人往，没有任何人注意到你的存在\n"
        search_on_street()
    add_operation("在街上晃荡",walk_on_street)
#===================给爸妈打电话 ========================

def add_root_operation(name,handler):
    for k,v in action_stack[0]:
        if k == name:
            return
    action_stack[0].append((name,handler))

def event_manager(ctx):
    global bGameStarted
    global action_stack
    global status
    #===============health and money check ===================
    if status["HP"] <= 0 :
        straa = reflush_screen()
        strRRRR = ('''
很遗憾，由于你的健康状况已经低到不可忍受，你也没有能力寻找到治疗。
当人们发现你的时候，你已经在三和的街边凉透了。
你的遗体被送回老家，但是没有任何亲戚愿意出面帮一个借钱不还的废物举办葬礼。
最后你的老父亲出面，把你火化了，成为了你们家空空如也的房间里唯一的一样家具——你的骨灰盒
        
!!!!!!!!!!!!游戏结束!!!!!!!!!\n 请重新输入 开始游戏
        ''')
        action.send_group_text_msg(ctx.FromGroupId, straa + strRRRR)
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money":5,
            "HP":100,
            "Debt":50000,
            "Message":"",
            "ContinueWorkTime":0
            }
    if status["Money"] <= 0:
        strbb = reflush_screen()
        strRRRR = ('''
即使在三和，也需要一点点的流动资金才能够活下去。如今你真的走到了身无分文的境地，
怎么说呢，你也许距离饿死也不太远了。
放弃吧，当你兴致勃勃地梭哈的时候，就该想到这一天

!!!!!!!!!!!!游戏结束!!!!!!!!!\n 请重新输入 开始游戏
        ''')
        action.send_group_text_msg(ctx.FromGroupId, strbb + strRRRR)
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money":5,
            "HP":100,
            "Debt":50000,
            "Message":"",
            "ContinueWorkTime":0
            }
        
    if status["HP"] > 100:
        status["HP"] = 100
    #===============睡觉===============================
    if status["HP"] <= 60 :
        status["Message"] += '''\n你感觉自己有一些疲惫了，可以考虑找个睡觉的地方'''

        def sleep_in_hole():
            status["Message"] = '''
你晃悠了一圈，找到了一个小桥洞
你从周围收集了一些编织袋，凑成了一个床垫
然后还找了些枯树枝，想生个火熬过晚上
            '''
            if random.random() < 0.1:
                status["Message"] += '''
深夜的寒冷穿透你的骨髓，
等熬到第二天早上的时候，你意识到自己发烧了
                '''    
                status["HP"] -= 10
            elif random.random() < 0.3:
                status["Message"] += '''
深夜的寒冷穿透你的骨髓，
冰冷的水泥地板没有让你很好地休息，但是还是恢复了一些体力
                '''    
                status["HP"] += 10
            else:
                status["Message"] += '''
深夜的寒冷穿透你的骨髓，
顾不得这些的你凑合着睡了过去，然后在太阳出来的时候醒了过来
                '''    
                status["HP"] += 20
        add_root_operation("睡桥洞",sleep_in_hole)  

        def sleep_in_hotel():
            status["Message"] = '''
你在街上找到了一个便宜的小旅馆，睡一次只需要50
洗了个澡出来，躺在床上，你感觉很久没有这么舒服过了
            '''
            status["HP"] += 50
            status["Money"] -= 50
        add_root_operation("睡50的小旅馆",sleep_in_hotel)          
    return
def main(ctx):
    init(status)
    str = reflush_screen()
    str = str +"\n请回复继续游戏加空格加选项, 比如回复 继续游戏 1, 不玩请输入结束游戏"
    action.send_group_text_msg(ctx.FromGroupId, str)














mt = 0
@bot.on_group_msg
@deco.only_this_msg_type('TextMsg')
def receive_group_msg(ctx: GroupMsg):

    global bGameStarted
    global bSaoLeiStart
    global action_stack
    global status
    global mt

    strCont = ctx.Content
    
    if 157199224 == ctx.FromUserId:
        return 1
    if strCont == "开始游戏":
        if bGameStarted == False:
            bGameStarted = True
            main(ctx)
        else:
            action.send_group_text_msg(ctx.FromGroupId, "游戏正在进行中, 不能多开")
    if strCont.startswith("继续游戏"):
        if bGameStarted == True:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 2:
                strSelect = args[1]
                try:
                    intSelect = int(strSelect)
                    handle_input(intSelect)
                    event_manager(ctx)
                    if bGameStarted == True:
                        strRef = reflush_screen()
                        action.send_group_text_msg(ctx.FromGroupId, strRef)
                except:
                    action.send_group_text_msg(ctx.FromGroupId, "输入数字错误! 比如回复 继续游戏 1")
            else:
                action.send_group_text_msg(ctx.FromGroupId, "输入多了!! 比如回复 继续游戏 1")
        else:
            action.send_group_text_msg(ctx.FromGroupId, "游戏未开始, 请回复 开始游戏")
    if strCont == "结束游戏" and bGameStarted == True:
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money":5,
            "HP":100,
            "Debt":50000,
            "Message":"",
            "ContinueWorkTime":0
            }

        action.send_group_text_msg(ctx.FromGroupId, "游戏关闭")


    if strCont == "开始扫雷":
        if bSaoLeiStart == False:
            bSaoLeiStart = True
            mt = MineTable()
            strShow = mt.printShow()
            strShow += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
            action.send_group_text_msg(ctx.FromGroupId, strShow)
        else:
            strShow = "游戏正在进行中, 不能多开\n"
            if mt != 0:
                strShow += mt.printShow()
                strShow += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
            action.send_group_text_msg(ctx.FromGroupId, strShow)
    if strCont.startswith("继续扫雷"):
        if bSaoLeiStart == True:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 2:
                line_input = args[1]
                try:
                    # 用户继续输入, 先判断输入格式
                    if not (re.match(r'^\d+,\d+', line_input)):
                        action.send_group_text_msg(ctx.FromGroupId, "输入错了!! 比如回复 继续扫雷 1,2")
                    else:
                        strResult = ""
                        line, field = eval(line_input)
                        # 打开用户指定的表格位置
                        result = mt.checkInputAddress(line, field)
                        if result == -1:
                            strResult = ('地址错误')
                        elif result == 0:
                            strResult = ('正在展示结果')
                        elif result == 2:
                            strResult = ('---炸了---\n')
                            mt.gameOverMine()
                            for item in mt.resultTable:
                               strResult += (str(item) + '\n')
                        else:
                            strResult = mt.printShow()
                            strResult += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
                        action.send_group_text_msg(ctx.FromGroupId, strResult)
                except:
                    action.send_group_text_msg(ctx.FromGroupId, "输入数字错误! 比如回复 继续扫雷 1,2")
            else:
                action.send_group_text_msg(ctx.FromGroupId, "输入错了!! 比如回复 继续扫雷 1,2")
        else:
            action.send_group_text_msg(ctx.FromGroupId, "游戏未开始, 请回复 开始扫雷")
    if strCont == "gg":
        bSaoLeiStart = False

        

@bot.when_disconnected(every_time=True)
def disconnected():
    o=0
    #logger.warning('socket断开~')


@bot.when_connected(every_time=True)
def connected():
    o=0
    #logger.success('socket连接成功~')
    
    
if __name__ == '__main__':
    # ---------------------------------------------------------------------------------
    bot.run()
