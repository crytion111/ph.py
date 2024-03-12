
from PicImageSearch import Network, Yandex
from PicImageSearch.model import YandexResponse
from botoy import bot, ctx, S
from xiuxian import *
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

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
# 解决请求https报错的问题
ssl._create_default_https_context = ssl._create_unverified_context


######################################################################
xxGame = XiuXianGame()
bOpenXXGame = True


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


proxiesIMG = "http://127.0.0.1:7890"


async def test_sync(filePath) -> str:
    async with Network(proxies=proxiesIMG) as client:
        yandex = Yandex(client=client)
        resp = await yandex.search(file=filePath)
        return show_result(resp)


def show_result(resp: YandexResponse) -> str:
    # print(str(resp.raw))
    strRes = resp.url
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
    'https': 'https://127.0.0.1:7890'
}

# 检查目标文件夹是否存在，如果不存在则创建它
if not os.path.exists("pic"):
    os.makedirs("pic")

# 检查目标文件夹是否存在，如果不存在则创建它
if not os.path.exists("soutu"):
    os.makedirs("soutu")


def SavePIC(image_url, path, nameTemp):
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
        'Cookie': 'list_mode=h; theme=auto; locale=zh; _ym_uid=1693998810306887787; _ym_d=1693998810; _ym_isad=2; over18=1; cf_clearance=JHafX.GsDZwjorK0sJUGEyjBpG.kM6Rw1mWLRULCDnQ-1694054810-0-1-259c7f4f.5c5e812c.729d20af-0.2.1694054810; _jdb_session=rm8R6D9OS3Dm8tlL%2FdyyKP%2BouFfilRYa1a3q0hdt8mu1cQJTaSRrmWGubl18iLMRk3uKTe7o9EmakjcPWNTJxx%2F5nb2vASfDoJVy3BDbb%2Fx%2BfWoUCy9XU%2Be%2B9w13w9JtagzQjpvnkmMEMKmwgzeWLvUmlLgmO10FZ%2FpgPvTlw2NpOdC5bPvdrk5tTBE6BZyIWVz7%2BsFrhVWnGdkQj8iQgZfv4ocKfmskXh06OHs8KrQwuDW89nK8%2FqEOXYBSdaNpeslRmoyh8IlYUvrBBrV7UjpS5r29nSZgAA%2FTFybxaQLhMtHSjAhGRBXb--CAMgWzzjVMYqYEcC--vKuyThE4ti%2BnigZI4CyUTA%3D%3D',
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
    # response = requests.get(page_url, headers=headers, proxies=proxies)
    response = requests.get(page_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    movielist = []
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
            strPicPath = SavePIC(srcIMGURL, "pic")
            strTil += ("\n封面:"+srcIMGURL+"")
            movielist.append(strTil)
            # print("strTil=========>", strTil)
            link = str(item['href'])
            if link:
                url = "https://javdb.com" + link
                req = requests.get(url, headers=headers, proxies=proxies)
                soups = BeautifulSoup(req.text, 'html.parser')
                movielistNew = getDetailedInfo(soups, movielist)
                if movielistNew:
                    movielist = movielistNew
    except Exception as rrr:
        print("That is the end!")
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


@bot
async def GetAV():
    strCont = ""
    strUID = ""
    strSendName = ""
    at_list = []
    strImageUrl = ""

    if ctx.g:
        if ctx.g.text:
            strCont = ctx.g.text
        if ctx.g.images:
            strImageUrl = ctx.g.images[0].Url
        strUID = str(ctx.g.from_user)
        strSendName = ctx.g.from_user_name
        at_list = ctx.g.at_list
        if ctx.g.bot_qq == ctx.g.from_user:
            return

    if ctx.g and ctx.g.text.startswith("番号"):
        strFH = ctx.g.text.replace("番号 ", "")
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

    elif strCont == "搜图" and len(strImageUrl) > 0:
        await S.text("开始以图搜图")
        strPicPath = SavePIC(strImageUrl, "soutu", "nameTemp")
        strCOn11 = await test_sync(strPicPath)
        await S.text("找到了:" + strCOn11)
    elif "活一世" in strCont or "修仙重生" in strCont:
        pl, strCon = xxGame.GetPlayerInfo(strUID, strSendName)
        if not strCon.startswith("新建"):
            if pl.TiLi > 0:
                pl.ResetPlayerInfo()
                strCon = "重生成功\n" + pl.PrintPlayerInfo()+"\n9点悟性以上为卓越天资"
                if pl.WuXin >= 9:
                    strCon += ("\n"+"恭喜抽到卓越天资!\n")
            else:
                strCon = "体力不足"
        await S.text(strCon)
    elif "修仙帮助" in strCont or "修仙指南" in strCont:
        strCon = "1,开始修仙\n" +\
            "2,出去冒险\n" +\
            "3,寻找道侣\n" +\
            "4,开始双修\n" +\
            "5,抛弃道侣\n" +\
            "6,勾引他的道侣@此人\n" +\
            "7,抢夺他的道侣@此人\n" +\
            "8,查看信息@此人\n" +\
            "9,求婚@此人\n" +\
            "10,修仙排名\n" +\
            "12,再活一世 或者 修仙重生"  # "11,修仙gm 账号 项目 数量\n" +\
        await S.text(strCon)
    elif "开始修仙" in strCont:
        pl, strCon = xxGame.GetPlayerInfo(strUID, strSendName)
        if (len(strCon) <= 0):
            strCon = "欢迎回来,你现在属性:\n"+pl.PrintPlayerInfo()+'\n本系统会根据你的悟性自动提升战斗力'
        await S.text(strCon)
    elif "出去冒险" in strCont:
        strCon = xxGame.PlayerAdventure(strUID, strSendName)
        await S.text(strCon)
    elif "寻找道侣" in strCont:
        strCon = xxGame.SearchWife(strUID, strSendName)
        await S.text(strCon)
    elif "开始双修" in strCont or "开始双休" in strCont:
        strCCCC = xxGame.SHuangXiuWithWife(strUID, strSendName)
        await S.text(strCCCC)
    elif "抛弃道侣" in strCont:
        strCCCC = xxGame.XXGiveUpWife(strUID, strSendName)
        await S.text(strCCCC)
    elif "勾引他的道侣" in strCont or "勾引道侣" in strCont:
        atInfoArr = at_list
        print(atInfoArr)
        if (len(atInfoArr) == 1):
            tarID = str(atInfoArr[0].Uin)
            strCCCC = xxGame.GouYinThisWife(strUID, strSendName, tarID)
            await S.text(strCCCC)
    elif "抢夺他的道侣" in strCont or "抢夺道侣" in strCont:
        atInfoArr = at_list
        # print(atInfoArr)
        if (len(atInfoArr) == 1):
            tarID = str(atInfoArr[0].Uin)
            strCCCC = xxGame.QiangDuoThisWife(
                strUID, strSendName, tarID)
            await S.text(strCCCC)
    elif "查看" in strCont or "查看信息" in strCont:
        atInfoArr = at_list
        if (len(atInfoArr) == 1):
            tarID = str(atInfoArr[0].Uin)
            strCCCC = xxGame.LookThisManInfo(tarID)
            await S.text(strCCCC)
    elif "求婚" in strCont:
        atInfoArr = at_list
        if (len(atInfoArr) == 1):
            tarID = str(atInfoArr[0].Uin)
            strCC = xxGame.QiuHun(strUID, strSendName, tarID)
            await S.text(strCC)
    elif "修仙排名" in strCont:
        strasd = xxGame.GetRank15Num()
        await S.text(strasd)

    # if "修仙gm" in strCont:
    #     if not bWihteUser:
    #         return await app.send_message(group, "就你?", quote=message)
    #     args = [i.strip() for i in strCont.split(" ") if i.strip()]
    #     if (len(args) == 4):
    #         try:
    #             uid = args[1]
    #             strAddKey = args[2]
    #             nAddNum = int(args[3])
    #             pl: PlayerInfo = xxGame.MapPlayer[uid]
    #             if strAddKey == "血量":
    #                 pl.HP += nAddNum
    #             if strAddKey == "悟性":
    #                 pl.WuXin += nAddNum
    #             if strAddKey == "战力":
    #                 pl.ZhanDouLi += nAddNum
    #             if strAddKey == "体力":
    #                 pl.TiLi += nAddNum
    #             if strAddKey == "气运":
    #                 pl.YunQi += nAddNum
    #         except:
    #             aaa = 0


if __name__ == "__main__":
    bot.load_plugins()  # 加载插件
    bot.print_receivers()  # 打印插件信息
    bot.run()  # 一键启动
