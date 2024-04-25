
import base64
from PicImageSearch import Network, Yandex
from PicImageSearch.model import YandexResponse
from botoy import bot, ctx, S, Action
from bs4 import BeautifulSoup
import re
import requests
import ssl
import time
import urllib3
import random
import math
import json
import os
from threading import Timer
from deepN import NudeOnePerson
import threading
import subprocess
import asyncio
import locale
import re
import subprocess
import sys
import os

from xiuxian import PlayerInfo, XiuXianGame


def wav_to_amr(wav_file, amr_file):
    # 使用 FFmpeg 将 WAV 文件转换为 AMR 格式
    subprocess.run(['ffmpeg', '-y', '-i', wav_file, '-ar',
                   '8000', '-ab', '24.4k', '-ac', '1', amr_file])


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
# 解决请求https报错的问题
ssl._create_default_https_context = ssl._create_unverified_context


bOpenXXGame = True
nMasterQQ = 1973381512

action = Action(1209916110)

######################################################################


proxiesIMG = "http://127.0.0.1:7890"


async def test_sync(filePath) -> str:
    async with Network(proxies=proxiesIMG) as client:
        yandex = Yandex(client=client)
        resp = await yandex.search(file=filePath)
        return show_result(resp)


def H2I(uurrll):
    from html2image import Html2Image
    hti = Html2Image()
    hti.screenshot(url=uurrll, save_as='baidu.png')


def show_result(resp: YandexResponse) -> str:
    strRes = resp.url
    H2I(strRes)
    if resp.raw and len(resp.raw) > 0:
        strRes = resp.raw[0].title+"\n\n"+resp.url
    return strRes
    # # logger.info(resp.origin)  # 原始数据
    # logger.info(resp.url)  # 搜索结果链接
    # # logger.info(resp.raw[0].origin)
    # logger.info(resp.raw[0].title)
    # logger.info(resp.raw[0].url)
    # logger.info(resp.raw[0].thumbnail)
    # logger.info(resp.raw[0].source)
    # logger.info(resp.raw[0].content)
    # logger.info(resp.raw[0].size)
    # logger.info("-" * 50)


proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 检查目标文件夹是否存在，如果不存在则创建它
if not os.path.exists("pic"):
    os.makedirs("pic")

# 检查目标文件夹是否存在，如果不存在则创建它
if not os.path.exists("soutu"):
    os.makedirs("soutu")


def SavePIC(image_url, path, nameTemp):
    print("SavePIC===> ", image_url)
    # 发送 GET 请求获取图片数据
    response = requests.get(image_url, proxies=proxies)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取图片的二进制数据
        image_data = response.content
        if nameTemp and len(nameTemp) > 0:
            ts = time.time()
            imageAllPath = "./" + path + "/nameTemp"+str(ts)+".jpg"
        else:
            # 提取图片文件名
            image_name = image_url.split("/")[-1].split(".")[0]
            imageAllPath = f"./" + path + "/{image_name}.jpg"
        # 保存图片到本地
        with open(imageAllPath, "wb") as image_file:
            image_file.write(image_data)
        # print("imageAllPath", imageAllPath)
        return imageAllPath
    else:
        print("请求失败。", image_url)
        return ""

# https://javdb.com/search?q=test&f=all


def get_Javdb(keyword: str):
    headers = {
        'authority': 'javdb.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cookie': 'list_mode=h; theme=auto; locale=zh; over18=1; cf_clearance=6JG7chi20vB1DVRXJo5g6UsVc4.4jt2HJt8DDuEukOg-1712654981-1.0.1.1-u.acd._tXPmRj5l_6GaeEA4l9waaNU162T90nkskMdf33FFt_1Id078I3HPA2H4QBSRqcEfVixGbn2_0Egu0jw; _jdb_session=B5Gw5eUqdCEDdWeehq%2Fdt4hnn1VpY79a41GxL8AZBBOLyALQYWPFQGRvOkBGeQI%2FF71F4P%2BXdq7sTw7zCXy5V5%2FYEW9lv5i5EAG887MUQtekfd8J3fndcGxLS3xKdCMZ4Ucq0NNFovxMGya%2FCWk2xbob3YbvKe8ER%2F4IEYPLH%2BIWMydsbb5J5Hcgei9ldrKfJwjfDxntiapHa72LxsswHEbVOu4H7pRDfRsYEGzR5SCtads2%2FFuzHSdrVijwxBIdxoRpSVDyccgdh6SA4wgqLK4KxGf1P3As%2Bndv7I%2BcpyYqZan2RJSqiayw--f%2BL6RSFjB6ciKLrh--79b0aDkwraiGic7Bo8AXaA%3D%3D',
        'Referer': 'https://javdb.com/',
        'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile': '?1',
        'Sec-Ch-Ua-Platform': 'Android',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',

    }
    page_url = f'https://javdb.com/search?q={keyword}&f=all'
    strPicPath = ""
    response = requests.get(page_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    movielist = []

    # print("item=========>", response.text)
    try:
        body = soup.find('body', {'data-lang': 'zh'})
        section = body.find('section', {'class': 'section'})
        itemdiv = section.find_all('a', {'class': 'box'})
        if itemdiv[0]:
            item = itemdiv[0]
            # print("item=========>", item)
            strIMG = item.find("img")
            srcIMGURL = strIMG.get('src')
            strTil = item.find("div", {"class": "video-title"})
            strTil = strTil.get_text()
            strPicPath = SavePIC(srcIMGURL, "pic", "")
            # print("strPicPath=========>", strPicPath)
            # print("item['href']=========>", item['href'])
            strTil += ("\n封面:"+srcIMGURL+"")
            movielist.append(strTil)
            # print("strTil=========>", strTil)
            link = str(item['href'])
            if link:
                url = "https://javdb.com" + link
                print("url=========>", url)
                proxies222 = {
                    'http': 'http://127.0.0.1:7890',
                    'https': 'http://127.0.0.1:7890'
                }
                req = requests.get(url, headers=headers, proxies=proxies222)
                soups = BeautifulSoup(req.text, 'html.parser')
                movielistNew = getDetailedInfo(soups, movielist)
                if movielistNew:
                    movielist = movielistNew
    except Exception as rrr:
        print("That is the end!", rrr)
        return movielist, strPicPath

    return movielist, strPicPath


def getDetailedInfo(soup, movielist):
    clIndex = 0
    MaxIndex = 5
    body = soup.find('body', {'data-lang': 'zh'})
    container = body.find_all('div', {'class': 'item columns is-desktop odd'})
    # print("container====>", container)
    for clIndex in range(MaxIndex):
        containerOne = container[clIndex]
        # print("container====>", containerOne)
        if containerOne:
            a_list = containerOne.find_all('a')
            if a_list[0]:
                # print("a_list[0]====>", a_list[0])
                strNormal = a_list[0]['href']
                daxiao = a_list[0].find('span', {'class': 'meta'})
                zm = a_list[0].find(
                    'span', {'class': 'tag is-warning is-small is-light'})
                zzmmm = ""
                if zm and zm.get_text() == "字幕":
                    zzmmm = "中文字幕"
                movielist.append(strNormal+"   " + (daxiao).get_text() + zzmmm)

    return movielist


def StartChange(strPicPath11, strPicPath22, oooName):
    print(strPicPath11, strPicPath22, oooName)
    strProggg = r"F:\deeplean\mcl\0000000000000\roop\venv\Scripts\python.exe F:\deeplean\mcl\0000000000000\roop\run.py -s " + \
        strPicPath11+" -t " + strPicPath22+" -o " + oooName + \
        " --frame-processor face_swapper face_enhancer --execution-provider cpu"
    print(strProggg)
    os.system(strProggg)

# def GetIMGHTML(strURL):
#     from html2image import Html2Image
#     hti = Html2Image()
#     hti.screenshot(url=strURL, save_as='python_org.png')


nCOUNTS = 0


nMaxLength = 200


######################################################################
xxGame = XiuXianGame()


def XXMain():
    global xxGame
    Timer(1, LoopPlayer).start()


def LoopPlayer():
    global xxGame
    xxGame.UpdatePlayersZDL()
    Timer(1, LoopPlayer).start()


xxGame.LoadAllPlayerInfo()
XXMain()

######################################################################


def GetAIVoice(strText, port=9880):
    global strUID
    global nMaxLength
    if str(strUID) != "1973381512" and (len(strText) > nMaxLength or len(strText) <= 0):
        print("" + str(len(strText)))
        return "0"
    global nCOUNTS
    data = {
        "text": strText,
        "text_language": "zh"
    }
    rep = requests.post(" http://127.0.0.1:"+str(port), json=data)
    if rep.status_code == 400:
        return "0"
    strName = "./sound/azi"+str(nCOUNTS)+".wav"
    nCOUNTS += 1
    with open(strName, "wb") as f:
        f.write(rep.content)
    return strName


strUID = ""


@bot
async def GetAV():
    global nMaxLength
    global strUID
    global xxGame
    global bOpenXXGame
    global nMasterQQ
    strCont = ""
    strSendName = ""
    at_list = []
    strImageUrl = ""

    bMasterUSer = False
    CTXG_P = ctx.g or ctx.f
    if CTXG_P:
        if CTXG_P.text:
            strCont = CTXG_P.text
        if CTXG_P.images:
            strImageUrl = CTXG_P.images[0].Url
        strUID = str(CTXG_P.from_user)
        strSendName = CTXG_P.from_user_name
        try:
            at_list = CTXG_P.at_list
        except:
            at_list = []
        if CTXG_P.bot_qq == CTXG_P.from_user:
            return 1

        if str(CTXG_P.from_user) == str(nMasterQQ):  # or CheckSafeQun(strGroupID):
            bMasterUSer = True

    if CTXG_P and CTXG_P.text.startswith("阿梓"):
        strFH = CTXG_P.text.replace("阿梓", "", 1)
        strR = GetAIVoice(strFH)
        if strR == "0":
            await S.text("太长了受不了,当前长度:"+str(len(strFH))+",最多支持:"+str(nMaxLength))
        if strR != "0":
            strSilk = "output.amr"
            wav_to_amr(strR, strSilk)
            with open(strSilk, 'rb') as ffff:
                dataffff = ffff.read()
                encodestr = base64.b64encode(
                    dataffff).decode()  # 得到 byte 编码的数据
                if ctx.g:
                    await action.sendGroupVoice(group=ctx.g.from_group, base64=encodestr)
                elif ctx.friend_msg:
                    await action.sendFriendVoice(user=ctx.friend_msg.from_user, base64=encodestr)
    if CTXG_P and CTXG_P.text.startswith("雪莲"):
        strFH = CTXG_P.text.replace("雪莲", "", 1)
        strR = GetAIVoice(strFH, 9881)
        if strR == "0":
            await S.text("太长了受不了,当前长度:"+str(len(strFH))+",最多支持:"+str(nMaxLength))
        if strR != "0":
            strSilk = "output.amr"
            wav_to_amr(strR, strSilk)
            with open(strSilk, 'rb') as ffff:
                dataffff = ffff.read()
                encodestr = base64.b64encode(
                    dataffff).decode()  # 得到 byte 编码的数据
                if ctx.g:
                    await action.sendGroupVoice(group=ctx.g.from_group, base64=encodestr)
                elif ctx.friend_msg:
                    await action.sendFriendVoice(user=ctx.friend_msg.from_user, base64=encodestr)
    if CTXG_P and CTXG_P.text.startswith("步非烟",):
        strFH = CTXG_P.text.replace("步非烟", "", 1)
        strR = GetAIVoice(strFH, 9882)
        if strR == "0":
            await S.text("太长了受不了,当前长度:"+str(len(strFH))+",最多支持:"+str(nMaxLength))
        if strR != "0":
            strSilk = "output.amr"
            wav_to_amr(strR, strSilk)
            with open(strSilk, 'rb') as ffff:
                dataffff = ffff.read()
                encodestr = base64.b64encode(
                    dataffff).decode()  # 得到 byte 编码的数据
                if ctx.g:
                    await action.sendGroupVoice(group=ctx.g.from_group, base64=encodestr)
                elif ctx.friend_msg:
                    await action.sendFriendVoice(user=ctx.friend_msg.from_user, base64=encodestr)
    if CTXG_P and CTXG_P.text.startswith("塔菲"):
        return 1
        strFH = CTXG_P.text.replace("塔菲", "", 1)
        strR = GetAIVoice(strFH, 9883)
        if strR == "0":
            await S.text("太长了受不了,当前长度:"+str(len(strFH))+",最多支持:"+str(nMaxLength))
        if strR != "0":
            strSilk = "output.amr"
            wav_to_amr(strR, strSilk)
            with open(strSilk, 'rb') as ffff:
                dataffff = ffff.read()
                encodestr = base64.b64encode(
                    dataffff).decode()  # 得到 byte 编码的数据
                if ctx.g:
                    await action.sendGroupVoice(group=ctx.g.from_group, base64=encodestr)
                elif ctx.friend_msg:
                    await action.sendFriendVoice(user=ctx.friend_msg.from_user, base64=encodestr)
    if CTXG_P and (CTXG_P.text.startswith("otto") or CTXG_P.text.startswith("电棍")):
        return 1
        strFH = CTXG_P.text.replace("otto", "", 1)
        strFH = strFH.replace("电棍", "", 1)
        strR = GetAIVoice(strFH, 9884)
        if strR == "0":
            await S.text("太长了受不了,当前长度:"+str(len(strFH))+",最多支持:"+str(nMaxLength))
        if strR != "0":
            strSilk = "output.amr"
            wav_to_amr(strR, strSilk)
            with open(strSilk, 'rb') as ffff:
                dataffff = ffff.read()
                encodestr = base64.b64encode(
                    dataffff).decode()  # 得到 byte 编码的数据
                if ctx.g:
                    await action.sendGroupVoice(group=ctx.g.from_group, base64=encodestr)
                elif ctx.friend_msg:
                    await action.sendFriendVoice(user=ctx.friend_msg.from_user, base64=encodestr)

    if CTXG_P and CTXG_P.text.startswith("换脸"):
        if CTXG_P.images and len(CTXG_P.images) == 2:
            start_time = time.time()
            strImageUrl111 = CTXG_P.images[0].Url
            strImageUrl222 = CTXG_P.images[1].Url
            strPicPath11 = SavePIC(strImageUrl111, "soutu", "nameTemp1")
            strPicPath22 = SavePIC(strImageUrl222, "soutu", "nameTemp2")
            oooName = "./wordDB/start_time"+str(start_time)+".jpg"

            StartChange(strPicPath11, strPicPath22, oooName)
            if os.path.exists(oooName):
                print("OVER: " + oooName)
                end_time = time.time()
                elapsed_time = end_time - start_time
                wqwwqeq = "合成成功,耗时" + \
                    str(elapsed_time)+"秒\n发送人QQ号:" + \
                    str(strUID)+"("+strSendName+"),由他负责"

                await S.image(data=oooName, text=wqwwqeq)

    if ctx.g and CTXG_P and CTXG_P.text.startswith("脱衣") :
        if not bMasterUSer:
            return S.text("你没权限使用", at=True)
        strTESTURL = strCont.replace("脱衣 ", "")
        strTESTURL = strTESTURL.replace("脱衣", "")
        if len(strImageUrl) > 0:
            await S.text("开始，稍等。。。", at=True)
            image_in_path = SavePIC(strImageUrl, "facein", "nameTemp")
        elif "http" in strTESTURL:
            await S.text("开始，稍等。。。", at=True)
            image_in_path = SavePIC(strTESTURL, "facein", "nameTemp")
            strCont = ""
            
        threading.Thread(target=run_nude_one_person_thread, args=(
            image_in_path, strCont, ctx.g.from_group)).start()

    if CTXG_P and CTXG_P.text.startswith("番号"):
        strFH = CTXG_P.text.replace("番号 ", "")
        strFH = strFH.replace("番号", "")
        await S.text('开始搜索' + strFH)
        Javdblist, strPicPath = get_Javdb(strFH)
        # print("=strPicPath.......", strPicPath)
        if len(Javdblist) <= 0:
            await S.text('没找到')
        else:
            strAllUrl = ""
            nIndex = 1
            for javd in Javdblist:
                strAllUrl += str(nIndex)+":\n"+(javd+"\n\n")
                nIndex += 1
            await S.text(strAllUrl)
            await S.image(strPicPath)
    elif strCont.startswith("搜图"):
        strTESTURL = strCont.replace("搜图 ", "")
        strTESTURL = strTESTURL.replace("搜图", "")
        if len(strImageUrl) > 0:
            await S.text("开始以图搜图")
            strPicPath = SavePIC(strImageUrl, "soutu", "nameTemp")
            strCOn11 = await test_sync(strPicPath)
        elif "http" in strTESTURL:
            await S.text("开始以图搜图")
            strPicPath = SavePIC(strTESTURL, "soutu", "nameTemp")
            strCOn11 = await test_sync(strPicPath)
        await S.image(data="baidu.png", text="找到了:" + strCOn11)

    if CTXG_P and "开启修仙功能" in strCont and bMasterUSer:
        bOpenXXGame = True
        await S.text("开启了")
    if CTXG_P and "关闭修仙功能" in strCont and bMasterUSer:
        bOpenXXGame = False
        await S.text("关闭了")
    if bOpenXXGame:
        if "活一世" in strCont or "修仙重生" in strCont:
            pl, strCon = xxGame.GetPlayerInfo(strUID, strSendName)
            if not strCon.startswith("新建"):
                if pl.TiLi > 0:
                    pl.ResetPlayerInfo()
                    strCon = "\n重生成功\n" + pl.PrintPlayerInfo()+"\n9点悟性以上为卓越天资"
                    if pl.WuXin >= 9:
                        strCon += ("\n"+"恭喜抽到卓越天资!\n")
                else:
                    strCon = "体力不足"
            await S.text(strCon, at=True)
        if "修仙帮助" in strCont or "修仙指南" in strCont:
            strCon = "\n1,开始修仙\n" +\
                "2,出去冒险\n" +\
                "3,寻找道侣\n" +\
                "4,开始双修\n" +\
                "5,抛弃道侣\n" +\
                "6,勾引他的道侣@此人\n" +\
                "7,抢夺他的道侣@此人\n" +\
                "8,查看信息@此人\n" +\
                "9,求婚@此人\n" +\
                "10,修仙排名\n" +\
                "11,修仙gm 账号 项目 数量\n" +\
                "12,再活一世 或者 修仙重生"
            await S.text(strCon, at=True)
        if "开始修仙" in strCont:
            pl, strCon = xxGame.GetPlayerInfo(strUID, strSendName)
            if (len(strCon) <= 0):
                strCon = "\n欢迎回来,你现在属性:\n"+pl.PrintPlayerInfo()+'\n本系统会根据你的悟性自动提升战斗力'
            await S.text(strCon, at=True)
        if "出去冒险" in strCont:
            strCon = xxGame.PlayerAdventure(strUID, strSendName)
            await S.text("\n"+strCon, at=True)
        if "寻找道侣" in strCont:
            strCon = xxGame.SearchWife(strUID, strSendName)
            await S.text("\n"+strCon, at=True)
        if "开始双修" in strCont or "开始双休" in strCont:
            strCCCC = xxGame.SHuangXiuWithWife(strUID, strSendName)
            await S.text("\n"+strCCCC, at=True)
        if "抛弃道侣" in strCont:
            strCCCC = xxGame.XXGiveUpWife(strUID, strSendName)
            await S.text("\n"+strCCCC, at=True)
        if "勾引他的道侣" in strCont or "勾引道侣" in strCont:
            atInfoArr = at_list
            # print(atInfoArr)
            if (len(atInfoArr) == 1):
                tarID = str(atInfoArr[0].Uin)
                strCCCC = xxGame.GouYinThisWife(strUID, strSendName, tarID)
                await S.text("\n"+strCCCC, at=True)
        if "抢夺他的道侣" in strCont or "抢夺道侣" in strCont:
            atInfoArr = at_list
            # print(atInfoArr)
            if (len(atInfoArr) == 1):
                tarID = str(atInfoArr[0].Uin)
                strCCCC = xxGame.QiangDuoThisWife(
                    strUID, strSendName, tarID)
                await S.text("\n"+strCCCC, at=True)
        if "查看" in strCont or "查看信息" in strCont:
            print("查看=====>", at_list)
            atInfoArr = at_list
            if (len(atInfoArr) == 1):
                tarID = str(atInfoArr[0].Uin)
                strCCCC = xxGame.LookThisManInfo(tarID)
                await S.text("\n"+strCCCC, at=True)
        if "求婚" in strCont:
            atInfoArr = at_list
            if (len(atInfoArr) == 1):
                tarID = str(atInfoArr[0].Uin)
                strCC = xxGame.QiuHun(strUID, strSendName, tarID)
                await S.text("\n"+strCC, at=True)
        if "修仙排名" in strCont:
            strasd = xxGame.GetRank15Num()
            await S.text("\n"+strasd, at=True)
        if "修仙gm" in strCont:
            if not bMasterUSer:
                await S.text("就你?", at=True)
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if (len(args) == 4):
                try:
                    uid = args[1]
                    strAddKey = args[2]
                    nAddNum = int(args[3])
                    pl: PlayerInfo = xxGame.MapPlayer[uid]
                    if strAddKey == "血量":
                        pl.HP += nAddNum
                    if strAddKey == "悟性":
                        pl.WuXin += nAddNum
                    if strAddKey == "战力":
                        pl.ZhanDouLi += nAddNum
                    if strAddKey == "体力":
                        pl.TiLi += nAddNum
                    if strAddKey == "气运":
                        pl.YunQi += nAddNum
                except:
                    aaa = 0


def run_nude_one_person_thread(image_path, content, from_group):
    asyncio.run(run_nude_one_person(image_path, content, from_group))


async def run_nude_one_person(image_path, content, from_group):
    img64, resultPath22 = NudeOnePerson(image_path, content)
    if resultPath22 != 0:
        print("成功: "+str(resultPath22))
        await action.sendGroupPic(group=from_group, text="做好了",  base64=img64)
    else:
        await action.sendGroupText(group=from_group, text="失败了")


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):  # 如果是文件夹那么递归调用一下
            del_file(c_path)
        else:  # 如果是一个文件那么直接删除
            try:
                os.remove(c_path)
            except:
                return 1


# del_file("./facein/")
# del_file("./faceout/")
# del_file("./p2p/")
# del_file("./flagged/")
print("Bot started")

if __name__ == "__main__":
    bot.load_plugins()  # 加载插件
    bot.print_receivers()  # 打印插件信息
    bot.run()  # 一键启动
