import math
import random
import time
from threading import Timer
import os
from os import path
from pathlib import Path
import json


curFileDir = Path(__file__).absolute().parent  # 当前文件路径
nMaxTTTLLL = 9  #最大体力


class PlayerInfo:
    def __init__(self, userid: str):
        self.UserID = userid
        self.ZhanDouLi = -1
        self.HP = -1
        self.WuXin = -1
        self.YunQi = -1
        self.TiLi = -1
        self.UpdateCount = -1
        self.UserName = ""+userid
        self.WifeID = ""
        self.WifeName = ""

    def ResetPlayerInfo(self):
        self.ZhanDouLi = random.randint(10, 20)
        self.HP = random.randint(100, 200)
        self.WuXin = round(random.random() * 10, 3)
        self.YunQi = random.randint(10, 20)
        self.TiLi = 0

    def InitPlayerData(self, strSendName=None):
        self.ZhanDouLi = random.randint(10, 20)
        self.HP = random.randint(100, 200)
        self.WuXin = round(random.random() * 10, 3)
        self.YunQi = random.randint(10, 20)
        self.TiLi = nMaxTTTLLL
        self.UpdateCount = 0
        if (strSendName != None and len(strSendName) >= 1):
            self.UserName = strSendName

    def AddPlayerZDL(self, nAddZDL):
        self.ZhanDouLi += nAddZDL
        self.ZhanDouLi = round(self.ZhanDouLi, 3)

    def AddPlayerHP(self, nAddHP):
        self.HP += nAddHP
        self.HP = round(self.HP, 3)

    def AddPlayerWX(self, nAddWX):
        self.WuXin += nAddWX
        self.WuXin = round(self.WuXin, 3)

    def AddPlayerYunQi(self, nAddYunQi):
        self.YunQi += nAddYunQi
        self.YunQi = round(self.YunQi, 3)

    # 战斗力自增
    def UpdatePlayerZDL(self):
        self.ZhanDouLi += self.WuXin
        self.ZhanDouLi = round(self.ZhanDouLi, 3)
        self.UpdateCount += 1
        # self.TiLi += 1
        if (self.UpdateCount >= (60*30)):
            self.UpdateCount = 0
            self.TiLi += 1
            if (self.TiLi > nMaxTTTLLL):
                self.TiLi = nMaxTTTLLL

    def CheckQiYun(self):
        fPlayerRate = self.YunQi / (self.YunQi + 100)
        fRandom = random.random()
        if (fRandom <= fPlayerRate):
            return True
        else:
            return False

    def AdventureGame(self) -> str:
        if (self.TiLi <= 0):
            return "体力不足"
        rInt = random.randint(2, 10)
        LostTL = math.ceil(self.TiLi / rInt)
        fPlayerRate = self.YunQi / (self.YunQi + 100)
        fRandom = random.random()
        if (fRandom <= fPlayerRate):
            # print("触发成功", fPlayerRate, fRandom)
            strCon = "气运加成触发成功,增加"+str(LostTL*5)+"%所有属性"
            for i in range(LostTL):
                self.Add5PlayerInfo()
            self.TiLi -= LostTL
            strPlayerInfo = self.PrintPlayerInfo()
            return strCon+"\n"+strPlayerInfo
        else:
            bAdd = random.randint(0, 10) >= 5
            if bAdd:
                strCon = "遇到" + str(LostTL) + \
                    "个魔兽,顺手杀了,增加"+str(LostTL*2)+"%的战斗力和血量"
                for i in range(LostTL):
                    self.AddRandomInfo()
            else:
                strCon = "遇到" + str(LostTL) + \
                    "个仇家,没打过,消耗元神才逃过去,扣除"+str(LostTL*3)+"%的战斗力和血量"
                for i in range(LostTL):
                    self.ReduceRandomInfo()
            self.TiLi -= LostTL
            strPlayerInfo = self.PrintPlayerInfo()
            return "\n玩家去冒险:\n" + strCon+"\n"+strPlayerInfo+'\n本次冒险扣除('+str(LostTL)+')点体力'

    def AddRandomInfo(self, nPer=2):
        self.AddPlayerZDL(round(self.ZhanDouLi * nPer / 100, 3))
        self.AddPlayerHP(round(self.HP * nPer / 100, 3))

    def ReduceRandomInfo(self, nPer=3):
        self.AddPlayerZDL(-round(self.ZhanDouLi * nPer / 100, 3))
        self.AddPlayerHP(-round(self.HP * nPer / 100, 3))

    def Add5PlayerInfo(self, nPer=5):
        self.AddPlayerZDL(round(self.ZhanDouLi * nPer / 100, 3))
        self.AddPlayerHP(round(self.HP * nPer / 100, 3))
        self.AddPlayerWX(round(self.WuXin * nPer / 100, 3))
        self.AddPlayerYunQi(round(self.YunQi * nPer / 100, 3))

    def MarrWithUser(self, DanShenUse):
        self.WifeID = DanShenUse.UserID
        self.WifeName = DanShenUse.UserName
        DanShenUse.WifeID = self.UserID
        DanShenUse.WifeName = self.UserName
        self.TiLi -= 1

    def XXWithWife(self, wifePlayer):
        if (wifePlayer == None):
            return "没有对象"
        else:
            allZDL = self.ZhanDouLi + wifePlayer.ZhanDouLi
            AddZDL = round(allZDL * 4 / 100, 3) * self.TiLi
            self.AddPlayerZDL(AddZDL)
            return "你把<" + self.WifeName + ">的*****,一起***,然后***,接着<" + self.WifeName + ">*****,****对方****,最后****\n" +\
                "修炼完成,你提升了双方战力总和的4%,共"+str(AddZDL)+"点\n" +\
                "本次双修了" + str(self.TiLi) + "回合\n剩余"+str(self.TiLi)+"点体力,全部双修用了"

    def GiveUpWife(self, bReduceTL=False):
        self.WifeID = ""
        self.WifeName = ""
        if (bReduceTL):
            self.TiLi -= 1

    def PrintPlayerInfo(self):
        fPlayerRate = (self.YunQi / (self.YunQi + 100)) * 100
        fPlayerRate = round(fPlayerRate, 2)
        if (len(self.WifeID) > 0):
            strInfo = "用户:<"+self.UserName + ">的信息:\n" +\
                "总战力:"+str(self.ZhanDouLi)+"\n" +\
                "总血量:"+str(self.HP)+"\n" +\
                "悟性(战力提升速度(每秒)):"+str(self.WuXin)+"\n" +\
                "气运:"+str(self.YunQi)+"("+str(fPlayerRate)+"%的极品事件概率加成)\n" +\
                "剩余体力(30分钟恢复1点):"+str(self.TiLi)+"\n" +\
                "道侣信息:"+str(self.WifeName)+"("+str(self.WifeID)+")\n"
        else:
            strInfo = "用户:<"+self.UserName + ">的信息:\n" +\
                "总战力:"+str(self.ZhanDouLi)+"\n" +\
                "总血量:"+str(self.HP)+"\n" +\
                "悟性(战力提升速度(每秒)):"+str(self.WuXin)+"\n" +\
                "气运:"+str(self.YunQi)+"("+str(fPlayerRate)+"%的极品事件概率加成)\n" +\
                "剩余体力(30分钟恢复1点):"+str(self.TiLi)+"\n" +\
                "没有道侣"+"\n"

        return strInfo


class XiuXianGame:
    def __init__(self):
        self.MapPlayer = {}
        self.nGameLoopCount = 0

    def InitOnePlayer(self, strPlayerID: str, strSendName) -> PlayerInfo:
        onePlayer = PlayerInfo(strPlayerID)
        onePlayer.InitPlayerData(strSendName)
        self.MapPlayer[strPlayerID] = onePlayer
        return onePlayer

    def GetPlayerInfo(self, strPlayerID: str, strSendName: str):
        strCC = ""
        player: PlayerInfo = None
        if (strPlayerID in self.MapPlayer):
            player = self.MapPlayer[strPlayerID]
            if (strSendName != None):
                player.UserName = strSendName
        else:
            player = self.InitOnePlayer(strPlayerID, strSendName)
            strIII = player.PrintPlayerInfo()
            strCC = "新建玩家角色成功:\n"+"初始属性:\n"+strIII+"\n9点悟性以上为卓越天资"
            if player.WuXin >= 9:
                strCC += ("\n"+"恭喜抽到卓越天资!\n")
        return player, strCC

    def UpdatePlayersZDL(self):
        for player in self.MapPlayer:
            playerData: PlayerInfo = self.MapPlayer[player]
            playerData.UpdatePlayerZDL()
        self.nGameLoopCount += 1
        if (self.nGameLoopCount >= 30): #30秒存储一次玩家数据
            self.nGameLoopCount = 0
            self.SaveAllPlayerInfo()

    # 玩家去冒险
    def PlayerAdventure(self, strID, strSendName) -> str:
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        strInfo = player.AdventureGame()
        return strCC + strInfo

    def SearchWife(self, strID, strSendName):
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        strReturn = ""
        if (len(player.WifeID) > 0):
            strReturn = "你已有一个<"+player.WifeName+">("+player.WifeID+")作伴,不能再寻"
        else:
            if (player.TiLi <= 0):
                return "体力不足"
            DanShenUse: PlayerInfo = None
            DanShenUseArr = []
            for playerOtherID in self.MapPlayer:
                playerOther = self.MapPlayer[playerOtherID]
                if (len(playerOther.WifeID) <= 0 and playerOther.UserID != player.UserID):
                    # DanShenUse = playerOther
                    DanShenUseArr.append(playerOther)

            if (len(DanShenUseArr) > 0):
                DanShenUse = DanShenUseArr[random.randint(
                    0, len(DanShenUseArr)-1)]

            if DanShenUse != None:
                player.MarrWithUser(DanShenUse)
                strReturn = "你找到修仙者:"+player.WifeName + \
                    "("+player.WifeID+"),并成功邀请互为道侣"
            else:
                strReturn = "当前宇宙已无单身修仙者,请尝试勾引或者抢夺吧"
        return strCC+strReturn

    def XXGiveUpWife(self, strID, strSendName):
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        if (player.TiLi <= 0):
            return "体力不足"
        strReturn = ""
        if (len(player.WifeID) > 0):
            strReturn = "你已抛弃了<"+player.WifeName + \
                ">("+player.WifeID+"),现在双方都是单身"
            wifePlayer: PlayerInfo = self.MapPlayer[player.WifeID]
            player.GiveUpWife(True)
            wifePlayer.GiveUpWife()
        else:
            strReturn = "单身狗凑什么热闹!"
        return strCC+strReturn

    def SHuangXiuWithWife(self, strID, strSendName):
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        if (player.TiLi <= 0):
            return "体力不足"
        strReturn = ""
        if (len(player.WifeID) > 0):
            wifePlayer = self.MapPlayer[player.WifeID]
            strReturn = player.XXWithWife(wifePlayer)
            player.TiLi = 0
        else:
            strReturn = "单身狗凑什么热闹!"
        return strCC+strReturn

    def GouYinThisWife(self, strID, strSendName, tarUID):
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        if (player.TiLi <= 0):
            return "体力不足"
        strReturn = ""
        if (len(player.WifeID) > 0):
            strReturn = "已有一个<"+player.WifeName+">("+player.WifeID+")作伴,莫要沾花惹草"
        else:
            if (tarUID not in self.MapPlayer):
                strReturn = "此人还未进入修仙世界,无法互动"
            else:
                ntrUser: PlayerInfo = self.MapPlayer[tarUID]
                if (len(ntrUser.WifeID) > 0):
                    if (player.CheckQiYun()):
                        ntrUserWife: PlayerInfo = self.MapPlayer[ntrUser.WifeID]
                        ntrUser.GiveUpWife()
                        player.MarrWithUser(ntrUserWife)
                        strReturn = "气运加持成功,\n依靠自己的魅力俘获<"+ntrUserWife.UserName + \
                            ">("+ntrUserWife.UserID+")的芳心,\n苦主<" + \
                            ntrUser.UserName + ">被你NTR成功"
                    else:
                        player.Add5PlayerInfo(-30)
                        player.TiLi -= 1
                        strReturn = "虽然努力卖弄自己的风骚,\n但是对方不为所动,并且告诉了全天下你的德行,\n全天下开始对你的追杀,\n销耗30%的全属性才逃脱"
                else:
                    strReturn = "此人单身,你在想什么呢?"

        return strCC+strReturn

    def QiangDuoThisWife(self, strID, strSendName, tarUID):
        player, strCC = self.GetPlayerInfo(strID, strSendName)
        if (player.TiLi <= 0):
            return "体力不足"
        strReturn = ""
        if (len(player.WifeID) > 0):
            strReturn = "已有一个<"+player.WifeName+">("+player.WifeID+")作伴,莫要沾花惹草"
        else:
            if (tarUID not in self.MapPlayer):
                strReturn = "此人还未进入修仙世界,无法互动"
            else:
                ntrUser: PlayerInfo = self.MapPlayer[tarUID]
                if (len(ntrUser.WifeID) > 0):
                    ntrUserWife: PlayerInfo = self.MapPlayer[ntrUser.WifeID]
                    nAllZL = ntrUser.ZhanDouLi+ntrUserWife.ZhanDouLi
                    nYouZl = player.ZhanDouLi
                    nMinZl = min(nAllZL, nYouZl)
                    nMaxZl = max(nAllZL, nYouZl)
                    strReturn = "你的战力:"+str(nYouZl) + \
                        "\n对方夫妻总战力:"+str(nAllZL)+"\n"
                    if ((nMaxZl - nMinZl) / nMinZl <= 0.1):
                        strReturn += "双方战力难分伯仲,对方纯爱夫妻心神合一抵御你的攻击,两败俱伤,什么都没抢到"
                    else:
                        if nYouZl > nAllZL:
                            ntrUser.GiveUpWife()
                            player.MarrWithUser(ntrUserWife)
                            strReturn += "你战力滔天,翻手为云覆手为雨,将对方玩弄与股掌之间\n成功打晕对方道侣<"+ntrUserWife.UserName+">,掳到自己的洞府\n" +\
                                "修仙者<"+ntrUser.UserName+">请速速修炼救回自己的道侣"
                        else:
                            player.Add5PlayerInfo(-50)
                            player.TiLi -= 1
                            strReturn += "不敌对方纯爱夫妻,拼死消耗50全属性才逃过一劫"
                else:
                    strReturn = "此人单身,你在想什么呢?"

        return strCC+strReturn

    def LookThisManInfo(self, tarUID):
        if (tarUID not in self.MapPlayer):
            strReturn = "此人还未进入修仙世界,无法互动"
        else:
            uuser: PlayerInfo = self.MapPlayer[tarUID]
            strReturn = "此人信息如下:\n"+uuser.PrintPlayerInfo()
        return strReturn

    def QiuHun(self, strID, strSendName, tarUID):
        if (tarUID not in self.MapPlayer):
            strReturn = "此人还未进入修仙世界,无法互动"
        else:
            player, strCC = self.GetPlayerInfo(strID, strSendName)
            if (len(player.WifeID) > 0):
                strReturn = "已有一个<"+player.WifeName + \
                    ">("+player.WifeID+")作伴,莫要沾花惹草"
            else:
                QHPlayer: PlayerInfo = self.MapPlayer[tarUID]
                if len(QHPlayer.WifeID) > 0:
                    strReturn = "<"+QHPlayer.UserName+">为<" + \
                        QHPlayer.WifeName+">的人妻(人夫),可尝试勾引之"
                else:
                    strDDD = ""
                    if QHPlayer.ZhanDouLi > player.ZhanDouLi:
                        strDDD = "战斗力"
                    if QHPlayer.HP > player.HP:
                        strDDD = "血量"
                    if QHPlayer.WuXin > player.WuXin:
                        strDDD = "悟性"
                    if QHPlayer.YunQi > player.YunQi:
                        strDDD = "气运"
                    if len(strDDD) > 0:
                        player.ReduceRandomInfo(10)
                        strReturn = "<"+QHPlayer.UserName + \
                            ">轻蔑的打量了你一下,笑道:'["+strDDD + \
                            "]这么低,也配和我做道侣?回去撒泡尿照照镜子吧!'\n求婚失败,心魔附体,扣除10%的战力和血量"
                    else:
                        player.MarrWithUser(QHPlayer)
                        strReturn = "<"+QHPlayer.UserName + \
                            ">面对你的求爱,不禁羞红了脸,\n缓缓说道:'上仙实力超群,是天下修炼者的梦中之人,你之所想亦是我之所愿'\n你们二人成功结为道侣"
        return strReturn

    def GetRank15Num(self, nNum=15):
        arr = []
        for pIndex in self.MapPlayer:
            pl: PlayerInfo = self.MapPlayer[pIndex]
            info = {"name": pl.UserName, "zl": pl.ZhanDouLi, "wf": pl.WifeName}
            arr.append(info)
        arr.sort(key=lambda a: a["zl"])
        arr.reverse()

        strRank = ""
        for i in range(len(arr)):
            info = arr[i]
            strRank += ("排名:"+str(i+1)+",昵称:" +
                        str(info["name"])+",战斗力:"+str(info["zl"])+",道侣:"+info["wf"]+'\n')
            if (i >= nNum):
                break
        return strRank

    def LoadAllPlayerInfo(self):
        try:
            with open(curFileDir / "XXGame.json", "r", encoding="utf-8") as f:
                plpCtx = json.load(f)
                playerArr = plpCtx['MapPlayer']
                for playerDataJson in playerArr:
                    MapPlayer = PlayerInfo(playerDataJson['UserID'])
                    MapPlayer.ZhanDouLi = playerDataJson['ZhanDouLi']
                    MapPlayer.HP = playerDataJson['HP']
                    MapPlayer.WuXin = playerDataJson['WuXin']
                    MapPlayer.YunQi = playerDataJson['YunQi']
                    MapPlayer.TiLi = playerDataJson['TiLi']
                    # MapPlayer.UpdateCount = playerDataJson['UpdateCount']
                    MapPlayer.UpdateCount = 999999#重启一次就将UpdateCount置位最大值,给所有玩家加一次体力
                    try:
                        MapPlayer.UserName = playerDataJson['UserName']
                        MapPlayer.WifeID = playerDataJson['WifeID']
                        MapPlayer.WifeName = playerDataJson['WifeName']
                    except:
                        MapPlayer.UserName = MapPlayer.UserID
                        MapPlayer.WifeID = ""
                        MapPlayer.WifeName = ""

                    self.MapPlayer[playerDataJson['UserID']] = MapPlayer
                f.close()
        except:
            self.MapPlayer = {}

    def SaveAllPlayerInfo(self):
        with open(curFileDir / "XXGame.json", 'w', encoding="utf-8")as f:
            playerArr = []
            for player in self.MapPlayer:
                playerData = self.MapPlayer[player]
                playerDataJson = {
                    "UserID": playerData.UserID,
                    "ZhanDouLi": playerData.ZhanDouLi,
                    "HP": playerData.HP,
                    "WuXin": playerData.WuXin,
                    "YunQi": playerData.YunQi,
                    "TiLi": playerData.TiLi,
                    "UpdateCount": playerData.UpdateCount,
                    "UserName": playerData.UserName,
                    "WifeID": playerData.WifeID,
                    "WifeName": playerData.WifeName,
                }
                playerArr.append(playerDataJson)

            data = {"MapPlayer": playerArr}
            json.dump(data, f)
