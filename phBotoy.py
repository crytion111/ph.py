﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest.mock import Base
from bs4 import BeautifulSoup
import urllib.request

from src.model import GPT, GPTConfig
import src.utils
from torch.nn import functional as F
import torch.nn as nn
import torch
from aip import AipSpeech
from io import BytesIO
import copy
from pydantic import BaseModel
from botoy import Botoy, Action, FriendMsg, GroupMsg, EventMsg, jconfig
from botoy.sugar import Text
import botoy.decorators as deco
from retrying import retry
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from tinydb.operations import add
from loguru import logger
import base64
import requests
import random
import time
import re
import json
import os
from os import path
import io
import sys
from PIL import Image, ImageDraw, ImageFont
import urllib.parse
from MyQR import myqr
import wave
import math
import struct
from base64 import b64encode
import cv2
import numpy as np
import jieba
import jieba.posseg as pseg
jieba.setLogLevel(20)
import cpuinfo
import psutil
import datetime
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path
from PIL import ImageEnhance
from typing import *
from threading import Timer

# print("=1111111===========>" + str(jconfig.bot))
# print("=22222222===========>" + str(jconfig.superAdmin))

botQQ = jconfig.bot
bMasterQQ = jconfig.superAdmin

bot = Botoy(qq=botQQ, log=False, use_plugins = True)
action = Action(botQQ)

bCloseXX = False

bOpenThisBOT = True
dataCiliGroupData = {}
dataSetuGroupData = {}
dataNudeGroupData = {}
nAAAAAAAA = 91
nBBBBBB = 99999
nReciveTimes = 0

nXXXCount = 0

session = requests.Session()

# wilteList = [779119500, 273590953, 234088768]
wilteList = [779119500, 273590953, 511165870, 135365398, 861644376]
blackList = [143626394]

for x in wilteList:
    strID = str(x)
    dataCiliGroupData[strID] = True
    dataSetuGroupData[strID] = True
    dataNudeGroupData[strID] = True


bBotClose = False

plpDataArr = []
curFileDir = Path(__file__).absolute().parent  # 当前文件路径
with open(curFileDir / "plp.json", "r", encoding="utf-8") as f:
    plpCtx = json.load(f)
    # print("plpp=====> " + str(plpCtx))
    dataArr = plpCtx['plpData'] 
    if(dataArr and len(dataArr) > 0):
        plpDataArr = dataArr

def savePLPJson():
    with open(curFileDir / "plp.json", 'w', encoding="utf-8")as f:
        data = {"plpData": plpDataArr}
        json.dump(data, f)

mrDataArr = []
with open(curFileDir / "mr.json", "r", encoding="utf-8") as f:
    mrCtx = json.load(f)
    # print("plpp=====> " + str(plpCtx))
    dataArr = mrCtx['arr'] 
    if(dataArr and len(dataArr) > 0):
        mrDataArr = dataArr





# 贷款数据库
dkDataArr = []
curFileDir = Path(__file__).absolute().parent  # 当前文件路径
with open(curFileDir / "dk.json", "r", encoding="utf-8") as f:
    plpCtx = json.load(f)
    dataArr = plpCtx['dkData'] 
    if(dataArr and len(dataArr) > 0):
        dkDataArr = dataArr




def loopCheckDK():
    Timer(3, checkDaikuan).start()
    


def checkDaikuan():
    if dkDataArr and len(dkDataArr) > 0:
        for dkD in dkDataArr:
            dTime = dkD["dTime"]
            nTime = int(time.time())
            if nTime - dTime >= 600:
                removeCoins(dkD)
                dkDataArr.remove(dkD)
                SaveDKData()

    loopCheckDK()


def removeCoins(dkD):
    global elsGameData

    dUid = dkD["dUid"]
    dGid = dkD["dGid"]
    strUID = str(dUid)
    
    try:
        elsGameData[strUID]["coins"] -= 11000
    except:
        elsGameData[strUID] = {}
        elsGameData[strUID]["coins"] = -11000
        elsGameData[strUID]["signTime"] = 0
    
    strUCoins = str(elsGameData[strUID]["coins"])

    action.sendGroupText(dGid, "贷款时间到,收回你的11000块贷款,其中1000块利息, 你还剩"+strUCoins+"个金币",  atUser=int(dUid))
    SaveElsGameData()



loopCheckDK()


















np.seterr(divide="ignore", invalid="ignore")

#---------------------------------------TJTKTK

def resize_image(im1: Image.Image, im2: Image.Image, mode: str) -> Tuple[Image.Image, Image.Image]:
    """
    统一图像大小
    """
    _wimg = im1.convert(mode)
    _bimg = im2.convert(mode)

    wwidth, wheight = _wimg.size
    bwidth, bheight = _bimg.size

    width = max(wwidth, bwidth)
    height = max(wheight, bheight)

    wimg = Image.new(mode, (width, height), 255)
    bimg = Image.new(mode, (width, height), 0)

    wimg.paste(_wimg, ((width - wwidth) // 2, (height - wheight) // 2))
    bimg.paste(_bimg, ((width - bwidth) // 2, (height - bheight) // 2))

    return wimg, bimg


# 感谢老司机
# https://zhuanlan.zhihu.com/p/31164700
def gray_car(
    wimg: Image.Image,
    bimg: Image.Image,
    wlight: float = 1.0,
    blight: float = 0.3,
    chess: bool = False,
) -> Image.Image:
    """
    发黑白车
    :param wimg: 白色背景下的图片
    :param bimg: 黑色背景下的图片
    :param wlight: wimg 的亮度
    :param blight: bimg 的亮度
    :param chess: 是否棋盘格化
    :return: 处理后的图像
    """
    wimg, bimg = resize_image(wimg, bimg, "L")

    wpix = np.array(wimg).astype("float64")
    bpix = np.array(bimg).astype("float64")

    # 棋盘格化
    # 规则: if (x + y) % 2 == 0 { wpix[x][y] = 255 } else { bpix[x][y] = 0 }
    if chess:
        wpix[::2, ::2] = 255.0
        bpix[1::2, 1::2] = 0.0

    wpix *= wlight
    bpix *= blight

    a = 1.0 - wpix / 255.0 + bpix / 255.0
    r = np.where(a != 0, bpix / a, 255.0)

    pixels = np.dstack((r, r, r, a * 255.0))

    pixels[pixels > 255] = 255

    return Image.fromarray(pixels.astype("uint8"), "RGBA")


# https://zhuanlan.zhihu.com/p/32532733
def color_car(
    wimg: Image.Image,
    bimg: Image.Image,
    wlight: float = 1.0,
    blight: float = 0.6,
    wcolor: float = 0.01,
    bcolor: float = 0.5,
    chess: bool = False,
) -> Image.Image:
    """
    发彩色车
    :param wimg: 白色背景下的图片
    :param bimg: 黑色背景下的图片
    :param wlight: wimg 的亮度
    :param blight: bimg 的亮度
    :param wcolor: wimg 的色彩保留比例
    :param bcolor: bimg 的色彩保留比例
    :param chess: 是否棋盘格化
    :return: 处理后的图像
    """
    wimg = ImageEnhance.Brightness(wimg).enhance(wlight)
    bimg = ImageEnhance.Brightness(bimg).enhance(blight)

    wimg, bimg = resize_image(wimg, bimg, "RGB")

    wpix = np.array(wimg).astype("float64")
    bpix = np.array(bimg).astype("float64")

    if chess:
        wpix[::2, ::2] = [255., 255., 255.]
        bpix[1::2, 1::2] = [0., 0., 0.]

    wpix /= 255.
    bpix /= 255.

    wgray = wpix[:, :, 0] * 0.334 + wpix[:, :, 1] * 0.333 + wpix[:, :, 2] * 0.333
    wpix *= wcolor
    wpix[:, :, 0] += wgray * (1. - wcolor)
    wpix[:, :, 1] += wgray * (1. - wcolor)
    wpix[:, :, 2] += wgray * (1. - wcolor)

    bgray = bpix[:, :, 0] * 0.334 + bpix[:, :, 1] * 0.333 + bpix[:, :, 2] * 0.333
    bpix *= bcolor
    bpix[:, :, 0] += bgray * (1. - bcolor)
    bpix[:, :, 1] += bgray * (1. - bcolor)
    bpix[:, :, 2] += bgray * (1. - bcolor)

    d = 1. - wpix + bpix

    d[:, :, 0] = d[:, :, 1] = d[:, :, 2] = d[:, :, 0] * 0.222 + d[:, :, 1] * 0.707 + d[:, :, 2] * 0.071

    p = np.where(d != 0, bpix / d * 255., 255.)
    a = d[:, :, 0] * 255.

    colors = np.zeros((p.shape[0], p.shape[1], 4))
    colors[:, :, :3] = p
    colors[:, :, -1] = a

    colors[colors > 255] = 255

    return Image.fromarray(colors.astype("uint8")).convert("RGBA")

def mkTKPic(strP1, strP2, strP3):
    im1 = Image.open(strP1)
    im2 = Image.open(strP2)
    im1 = im1.resize(im2.size, Image.ANTIALIAS)
    # color_car(im1, im2).save(strP3)
    buffered = io.BytesIO()
    color_car(im1, im2).save(buffered, format="png")
    return base64.b64encode(buffered.getvalue()).decode()


#---------------------------------------骂人
def GetMrStr():
    global mrDataArr
    allLength = len(mrDataArr)
    nRIndex = random.randint(0, allLength-1)
    mrd = mrDataArr[nRIndex]
    return mrd

# -------------------------------------------------------------

def GetMeiZiTu(nNum = 1):
    url = "https://bcy.net/apiv3/common/circleFeed"
    par = {
        'circle_id': 14903
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'Referer': 'https://bcy.net/tag/14903'
    }

    res = requests.get(url, headers=header, params=par)
    res_encode = res.text.encode('utf-8')
    res_json = json.loads(res_encode)

    strResJK = ""
    objJK = {}
    strb64JK = []
    nRoninnn = random.randint(1, 10)
    a = 0
    for item in res_json['data']['items']:
        a += 1
        if a != nRoninnn:
            continue
        name = item['item_detail']['uname']
        strResJK += str(name)+"\n\n"
        
        avatar = item['item_detail']['avatar']
        avatar_name = str(avatar).rsplit('.image')[0]
        avatar_name1 = str(avatar_name).rsplit('/')[-1]
        # strResJK += avatar + "\n\n"
        
        # print(f'{avatar_name1}.jpg')

        dataww = requests.get(avatar, headers=header).content 
        strB64 = base64.b64encode(dataww).decode()

        # print(name, avatar_name1)

        for image in item['item_detail']['image_list']:
            images = image['path']
            images_name = str(images).rsplit('.image')[0]
            images_name1 = str(images_name).rsplit('/')[-1]
            strResJK += images + "\n\n"
            aa = (requests.get(images, headers=header).content)
            aa64 = base64.b64encode(aa).decode()
            strb64JK.append(aa64)

        objJK["strResJK"] = strResJK
        objJK["avatar"] = strB64
        objJK["strb64JK"] = strb64JK
        return objJK
        # time.sleep(1)















# -------------------------------------------------------------
def generate_wordcloud(text):
    '''
    输入文本生成词云,如果是中文文本需要先进行分词处理
    '''
    # 设置显示方式
    d=path.dirname(__file__)
    # alice_mask = np.array(Image.open(path.join(d, "Images//alice_mask.png")))
    font_path=path.join(d,"./ArialEnUnicodeBold.ttf")
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",# 设置背景颜色
           max_words=2000, # 词云显示的最大词数  
        #    mask=alice_mask,# 设置背景图片       
           stopwords=stopwords, # 设置停用词
           font_path=font_path, # 兼容中文字体，不然中文会显示乱码
                  )

    # 生成词云 
    wc.generate(text)

    # 生成的词云图像保存到本地
    wc.to_file(path.join(d, "./alice.png"))







# -------------------------------------------------------------


def get_cpu_info():
    info = cpuinfo.get_cpu_info()  # 获取CPU型号等
    cpu_count = psutil.cpu_count(logical=False)  # 1代表单核CPU，2代表双核CPU
    xc_count = psutil.cpu_count()  # 线程数，如双核四线程
    cpu_percent = round((psutil.cpu_percent()), 2)  # cpu使用率
    try:
        model = info["hardware_raw"]  # cpu型号
    except Exception:
        model = info["brand_raw"]  # cpu型号
    try:  # 频率
        freq = info["hz_actual_friendly"]
    except Exception:
        freq = "null"
    cpu_info = (model, freq, info["arch"], cpu_count, xc_count, cpu_percent)
    return cpu_info


def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 3)  # 总内存
    used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 3)  # 已用内存
    available_nc = round((float(memory.available) / 1024 / 1024 / 1024), 3)  # 空闲内存
    percent_nc = memory.percent  # 内存使用率
    swap_total = round((float(swap.total) / 1024 / 1024 / 1024), 3)  # 总swap
    swap_used = round((float(swap.used) / 1024 / 1024 / 1024), 3)  # 已用swap
    swap_free = round((float(swap.free) / 1024 / 1024 / 1024), 3)  # 空闲swap
    swap_percent = swap.percent  # swap使用率
    men_info = (
        total_nc,
        used_nc,
        available_nc,
        percent_nc,
        swap_total,
        swap_used,
        swap_free,
        swap_percent,
    )
    return men_info


def uptime():
    now = time.time()
    boot = psutil.boot_time()
    boottime = datetime.datetime.fromtimestamp(boot).strftime("%Y-%m-%d %H:%M:%S")
    nowtime = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
    up_time = str(
        datetime.datetime.utcfromtimestamp(now).replace(microsecond=0)
        - datetime.datetime.utcfromtimestamp(boot).replace(microsecond=0)
    )
    alltime = (boottime, nowtime, up_time)
    return alltime


def sysinfo():
    cpu_info = get_cpu_info()
    mem_info = get_memory_info()
    up_time = uptime()
    msg = (
        "CPU型号:{0}\r\n频率:{1}\r\n架构:{2}\r\n核心数:{3}\r\n线程数:{4}\r\n负载:{5}%\r\n{6}\r\n"
        "总内存:{7}G\r\n已用内存:{8}G\r\n空闲内存:{9}G\r\n内存使用率:{10}%\r\n{6}\r\n"
        "swap:{11}G\r\n已用swap:{12}G\r\n空闲swap:{13}G\r\nswap使用率:{14}%\r\n{6}\r\n"
        "开机时间:{15}\r\n当前时间:{16}\r\n已运行时间:{17}"
    )
    full_meg = msg.format(
        cpu_info[0],
        cpu_info[1],
        cpu_info[2],
        cpu_info[3],
        cpu_info[4],
        cpu_info[5],
        "*" * 20,
        mem_info[0],
        mem_info[1],
        mem_info[2],
        mem_info[3],
        mem_info[4],
        mem_info[5],
        mem_info[6],
        mem_info[7],
        up_time[0],
        up_time[1],
        up_time[2],
    )
    return full_meg












# -------------------------------------------------------------
# 图片转为Base64
def toBase64(imgUrl):
    req = session.get(imgUrl)
    return base64.b64encode(req.content).decode()


def CheckYYYY(strB64):
    pay_load = {
        'api_key': "X5CYnsaJJCgMJXMPo9JGyHWfsqWx80gr",
        'api_secret': "K1zHwlcl1RalyoLOH3vWLsouLDjPcl69",
        'return_attributes': 'age,gender,skinstatus,beauty,smiling',
        'image_base64': strB64
    }
    # image_file = {'image_url': imageurl}
    r = requests.post(
        "https://api-cn.faceplusplus.com/facepp/v3/detect", data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++detect_face++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(img_file_path)
    # print(r.status_code)
    # print("====>" + r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    try:
        r_json = json.loads(r.text)
        if r.status_code == 200:
            faceNum = r_json["face_num"]
            if faceNum > 1:
                return "暂时只能分辨一张脸, 图中的人脸数="+str(faceNum)
            elif faceNum == 0:
                return "传的图没有人脸!!!!"
            else:
                faceData = r_json["faces"][0]
                attributes = faceData["attributes"]
                strXB = attributes["gender"]["value"]
                strMNMNM = "男性"
                if strXB == "Female":
                    strMNMNM = "女性"
                nAge = attributes["age"]["value"]
                skinstatus = attributes["skinstatus"]["health"]
                dark_circle = attributes["skinstatus"]["dark_circle"]
                butyScore = 0
                if strXB == "Female":
                    butyScore = attributes["beauty"]["female_score"]
                else:
                    butyScore = attributes["beauty"]["male_score"]

                strSMsm = ""
                if attributes["smile"]["value"] > attributes["smile"]["threshold"]:
                    strSMsm = "正在笑,"
                strRRRSS = "这个人是"+strMNMNM+", 年龄大概" + \
                    str(nAge)+"岁,"+ strSMsm +" 皮肤健康度为:"+str(skinstatus) + \
                    ',黑眼圈程度为:'+str(dark_circle) + \
                    ' \n最终颜值评分为:'+str(butyScore)
            return strRRRSS
        else:
            return "网络错误!!!!!!!!!!!!!"
    except Exception as error:
        return "识别错误==>" + str(error)


# -------------------------------------------------------------

def file_to_base64(path):
    with open(path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode()


# 百度语音 API
APP_ID = '25419425'
API_KEY = 'fct6UMiQMLsp53MqXzp7AbKQ'
SECRET_KEY = 'p3wU9nPnfR7iBz2kM25sikN2ms0y84T3'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 文字转语音
def text_to_speech(ai_text):
    # spd：语速0-9，vol：音量0-15，per：发音人选择 0女 1男 3男 4女
    result = client.synthesis(ai_text, 'zh', 1, {
        'vol': 8, 'per': 4, 'spd': 5
    })

    # print("resultresultresult"+str(result))

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        # print('识别成功')
        with open('./aisay.mp3', 'wb') as f:
            f.write(result)
        return "./aisay.mp3"

    return ""

# ---------------------------------------------------------------


# --------------------------------------------------------------


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
        initTable = [[self.cover for _ in range(
            self.tableLength)] for _ in range(self.tableLength)]
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
            strShow += str(i) + str(self.resultTable[i]) + "\n"
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
    "Money": 5,
    "HP": 100,
    "Debt": 50000,
    "Message": "",
    "ContinueWorkTime": 0
}


def do_once(name):
    def decorator1(func):
        def dec(*args):
            global action_stack
            action_stack[-1] = [item for item in action_stack[-1]
                                if item[0] != name]
            result = func()
            return result
        return dec
    return decorator1


def random_success(name, posibility, reason=None):
    def decorator1(func):
        def dec(*args):
            global action_stack
            if random.random() < posibility:
                result = func()
                return result
            else:
                status["Message"] = "很遗憾，你的" + name + "行为遇到了惨痛的失败\n"
                if reason != None:
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
    # try:
    operation_index = intSelect
    action_stack[-1][operation_index][1]()


def reflush_screen():

    strStatus = print_status(status)
    strStatus = strStatus + "\n你可以执行以下操作\n"

    for i in range(0, len(action_stack[-1])):
        strStatus = strStatus + str(i) + str(action_stack[-1][i][0])+'\n'
    return strStatus


is_exit = False


def add_operation(name, handler):
    action_stack[-1].append((name, handler))


def search_on_street():
    status["HP"] -= 2
    if random.random() < 0.2:
        status["Message"] += "你发现了一堆空瓶子！这可是能卖1块钱的！\n"
        status["Money"] += 1
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
            else:
                status["Message"] = '''
经过一阵子的努力，当那一刻来临的时候，你感觉浑身舒适，仿佛终于找到了属于男性的力量
你回头看了看身边背对着你的失足少女，点了一根烟，然后拍了她的背影
你甚至有一种迷幻的感觉，想要和她在一起，你赶紧甩了甩头，打消了这种想法
你把照片发到戒赌吧，配上几句“今天这车怎么样”之类的话，然后刷了刷网友回帖
随后翻过身睡着了
                '''
                status["HP"] += 50
        add_operation("修车", fix_car)

        @pop_action_stack
        def not_fix_car():
            status["Message"] = '''
你看了看那扇门，叹了一口气走开了。
修车就是这个冰冷都市中的唯一爱情吗？或者也只是和盒饭一样的快餐梦幻？
                '''
        add_operation("算了", not_fix_car)
        return

    if random.random() < 0.6:
        status["Message"] += "你发现了走在前面的那个人，屁股兜里露出来了半个iphone 6，你想试着偷窃吗\n"
        action_stack.append([])

        @pop_action_stack
        def steal():
            strSTTT = ('''
你一把从别人的屁股兜里抽出了iphone 6.
但是那个人立刻转过身来，想要抓住你，你转身就开始跑。
                ''')
            p = 0
            while(p < 0.95):
                p = random.random()
                i = random.randint(0, 3)
                if int(i) > 2:
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
        add_operation("偷窃", steal)

        @pop_action_stack
        def not_steal():
            status["Message"] = '''
你把目光从别人的屁股后面移开，转而思考别的事情
                '''
            return
        add_operation("算了", not_steal)
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
        status["HP"] += 1
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

    # ===================卖身份证 ========================
    @do_once("卖身份证")
    @random_success("卖身份证", 0.85, "那个找你做法人的人就是个骗子，拿了你的身份证转身就跑掉了,你的钱也没有拿回来")
    def sale_IDcard():
        status["Message"] = "你把自己的身份证卖掉换了100块钱\n"
        status["Money"] += 100
    add_operation("卖身份证", sale_IDcard)

    # ===================还债务   ========================
    def pay_debt():
        status["Message"] = "你凑了一笔钱，还上了100块钱的债务\n"
        status["Money"] -= 100
        status["Debt"] -= 100
    add_operation("还100块钱的债", pay_debt)

    # ===================做日结 ========================
    @random_success("做日结", 0.9, "你被骗进了限制人身自由的黑工厂，你完全顾不上别的就赶紧跑了出来")
    def do_one_day_job():
        action_stack.append([])
        status["Message"] = "你挤破头皮想要找到一份工作\n"
        if random.random() < 0.1:
            status["Message"] += "没想到一个趔趄，别人就把你从窗口挤开了，你想要挣扎，结果还挨了一拳"
            status["HP"] -= 3

        @pop_action_stack
        # @random_success("好好干活",0.9,"你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来")
        def work_hard():
            intRand = random.randint(1, 5)
            if intRand == 1:
                status["Message"] = "你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来"
                status["ContinueWorkTime"] = 0
                return

            status["Message"] = "你勤奋地工作了一天，获得了130块钱。\n"
            if status["ContinueWorkTime"] > 0:
                status["Message"] += "主管对你的印象有所改善，他给你稍微加了%d块工资，以示鼓励\n" % (
                    status["ContinueWorkTime"]*5)
            status["Message"] += "你的主管觉得你不错，告诉你如果经常来，会考虑给你加点工资"

            status["Money"] += 130 + status["ContinueWorkTime"]*5
            status["HP"] -= 30
            status["ContinueWorkTime"] += 1
        add_operation("好好干活", work_hard)

        @pop_action_stack
        # @random_success("摸鱼",0.5,"你心不在焉地摆弄着手里的焊枪，结果一不小心戳在了电路板上，你的主管忍无可忍直接让你滚犊子")
        def relax():
            intRand = random.randint(1, 2)
            if intRand != 2:
                status["Message"] = "你虽然无比认真，但是还是犯了错误，被主管臭骂一顿之后赶了出来"
                return
            status["Message"] = "你摸了一天鱼\n"
            if random.random() < 0.5:
                status["Message"] += "主管并没有发现你在摸鱼，还是给你发了130块钱的工资"
                status["Money"] += 130
                status["HP"] -= 15
                status["ContinueWorkTime"] += 1
            else:
                status["Message"] += "主管发现你在摸鱼，但是对你无可奈何。他清楚地知道这里是三和，所以给了你70块钱让你早点滚蛋别来了"
                status["Money"] += 70
                status["HP"] -= 15
                status["ContinueWorkTime"] = 0
        add_operation("摸鱼", relax)
    add_operation("做日结", do_one_day_job)

    # ===================去网吧 ========================
    def go_to_netbar():
        action_stack.append([])
        status["Message"] = "你走进一家网吧，花了3块钱开了1个小时的机子\n"

        @random_success("开一把撸啊撸", 0.5, "你这把队友坑的要命，结果输得很惨，还被对面肆意嘲讽，气的要命")
        def play_lol():
            status["Message"] = "你决定用小号打一把撸啊撸"
            status["HP"] -= 3
        add_operation("开一把撸啊撸", play_lol)

        # 加入支付宝被举报功能
        @random_success("去戒赌吧哭穷要饭", 0.9, "贴吧这种不靠谱的东西你也相信？")
        def go_to_tieba():
            if random.random() < 0.5:
                status["Message"] = '''
你刚把支付宝发上去，就被人认出来，你是那个经常来吧里要饭的老哥
还没过几分钟，你的支付宝就被举报了，里面仅有的几块钱也没了
                '''
                status["Money"] -= 5
            else:
                status["Message"] = "你开始一把鼻涕一把泪地在戒赌吧说自己的遭遇，并发了自己的支付宝账号，请求有人能够给你打几块钱，没想到还真的有人上当"
                status["Money"] += 3
            status["HP"] -= 3
        add_operation("去戒赌吧哭穷要饭", go_to_tieba)

        # @random_success("开一局赔率10倍的网赌",0.2,"今天运气一点都不行，你输得非常惨")
        def gambling10():
            status["Message"] = "你打开熟悉的网络赌博平台，下了10块钱的赌注\n"
            if random.random() < 0.05:
                status["Money"] += 100000000
                status["Message"] += "这波就稳了！净赚100！今晚怕是得修车庆祝一下"
            else:
                status["Money"] -= 10
                status["Message"] += "结果运气真的不站在你这边，你输了10块，怎么也得修车开开运气"
            status["HP"] -= 3
        add_operation("开一局赔率10倍的网赌", gambling10)

        @do_once("点一碗红烧牛肉面")
        def buy_noodle():
            status["Message"] = "你买了一碗3块钱的红烧牛肉面,恢复了一些体力\n"
            status["HP"] += 3
            status["Money"] -= 3
        add_operation("点一碗红烧牛肉面", buy_noodle)

        @pop_action_stack
        def finish_play():
            status["Message"] = "你揉了揉太阳穴，结账下机了\n"
            status["HP"] -= 1
            status["Money"] -= 3
        add_operation("结账下机", finish_play)

    add_operation("去网吧上网", go_to_netbar)
    #     status["Money"] +=

    # ===================吃挂逼面喝大水 ========================

    def eat():
        status["Message"] = "你点了一份3块钱的挂逼面和一块钱的大水，呼哧呼哧地吃了起来，增加了3点HP\n"
        status["HP"] += 3
        status["Money"] -= 4
    add_operation("吃挂逼面喝大水", eat)

    # ===================在街上瞎晃荡 ========================
    def walk_on_street():
        status["Message"] = "你开始在深圳三和的街上晃荡，人来人往，没有任何人注意到你的存在\n"
        search_on_street()
    add_operation("在街上晃荡", walk_on_street)
# ===================给爸妈打电话 ========================


def add_root_operation(name, handler):
    for k, v in action_stack[0]:
        if k == name:
            return
    action_stack[0].append((name, handler))


def event_manager(ctx):
    global bGameStarted
    global action_stack
    global status
    # ===============health and money check ===================
    if status["HP"] <= 0:
        straa = reflush_screen()
        strRRRR = ('''
很遗憾，由于你的健康状况已经低到不可忍受，你也没有能力寻找到治疗。
当人们发现你的时候，你已经在三和的街边凉透了。
你的遗体被送回老家，但是没有任何亲戚愿意出面帮一个借钱不还的废物举办葬礼。
最后你的老父亲出面，把你火化了，成为了你们家空空如也的房间里唯一的一样家具——你的骨灰盒
        
!!!!!!!!!!!!游戏结束!!!!!!!!!\n 请重新输入 开始流浪
        ''')
        action.sendGroupText(ctx.FromGroupId, straa + strRRRR)
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money": 5,
            "HP": 100,
            "Debt": 50000,
            "Message": "",
            "ContinueWorkTime": 0
        }
    if status["Money"] <= 0:
        strbb = reflush_screen()
        strRRRR = ('''
即使在三和，也需要一点点的流动资金才能够活下去。如今你真的走到了身无分文的境地，
怎么说呢，你也许距离饿死也不太远了。
放弃吧，当你兴致勃勃地梭哈的时候，就该想到这一天

!!!!!!!!!!!!游戏结束!!!!!!!!!\n 请重新输入 开始流浪
        ''')
        action.sendGroupText(ctx.FromGroupId, strbb + strRRRR)
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money": 5,
            "HP": 100,
            "Debt": 50000,
            "Message": "",
            "ContinueWorkTime": 0
        }

    if status["HP"] > 100:
        status["HP"] = 100
    # ===============睡觉===============================
    if status["HP"] <= 60:
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
        add_root_operation("睡桥洞", sleep_in_hole)

        def sleep_in_hotel():
            status["Message"] = '''
你在街上找到了一个便宜的小旅馆，睡一次只需要50
洗了个澡出来，躺在床上，你感觉很久没有这么舒服过了
            '''
            status["HP"] += 50
            status["Money"] -= 50
        add_root_operation("睡50的小旅馆", sleep_in_hotel)
    return


def mainLiuLang(ctx):
    init(status)
    str = reflush_screen()
    str = str + "\n请回复继续游戏加空格加选项, 比如回复 继续游戏 1, 不玩请输入结束游戏"
    action.sendGroupText(ctx.FromGroupId, str)


mt = 0


# ------------------------------混乱#------------------------------
def transYin(x, y, aaa):
    if x in {',', '，', '。'}:
        return '❤'
    if x in {'!', '！', ' '}:
        return '...'
    if len(x) > 1 and random.random() < 0.5:
        return f'{x[0]}〇♡..?{x}'
    else:
        if y == 'n' and random.random() < 0.4:
            x = '♥' * len(x)
        return f'..{x}'


def chs2yin(s, aaa=0.5):
    return ''.join([transYin(x, y, aaa) for x, y in pseg.cut(s)])
# ----------------------------------------------------------------------------------

# -----------------------------------------------------废话生成


xx = "学生会退会"

text = [
    "现在, 解决x的问题, 是非常非常重要的. 所以, ",
    "我们不得不面对一个非常尴尬的事实, 那就是, ",
    "x的发生, 到底需要如何做到, 不x的发生, 又会如何产生. ",
    "而这些并不是完全重要, 更加重要的问题是, ",
    "x, 到底应该如何实现. ",
    "带着这些问题, 我们来审视一下x. ",
    "所谓x, 关键是x需要如何写. ",
    "我们一般认为, 抓住了问题的关键, 其他一切则会迎刃而解."
    "问题的关键究竟为何? ",
    "x因何而发生?",
    "每个人都不得不面对这些问题.  在面对这种问题时, ",
    "一般来讲, 我们都必须务必慎重的考虑考虑. ",
    "要想清楚, x, 到底是一种怎么样的存在. ",
    "了解清楚x到底是一种怎么样的存在, 是解决一切问题的关键.",
    "就我个人来说, x对我的意义, 不能不说非常重大. ",
    "本人也是经过了深思熟虑,在每个日日夜夜思考这个问题. ",
    "x, 发生了会如何, 不发生又会如何. ",
    "在这种困难的抉择下, 本人思来想去, 寝食难安.",
    "生活中, 若x出现了, 我们就不得不考虑它出现了的事实. ",
    "这种事实对本人来说意义重大, 相信对这个世界也是有一定意义的.",
    "我们都知道, 只要有意义, 那么就必须慎重考虑.",
    "既然如此, ",
    "那么, ",
    "我认为, ",
    "一般来说, ",
    "总结的来说, ",
    "既然如何, ",
    "经过上述讨论",
]

名人名言 = [
    "伏尔泰曾经说过, 不经巨大的困难，不会有伟大的事业。这不禁令我深思",
    "富勒曾经说过, 苦难磨炼一些人，也毁灭另一些人。这不禁令我深思",
    "文森特·皮尔曾经说过, 改变你的想法，你就改变了自己的世界。这不禁令我深思",
    "拿破仑·希尔曾经说过, 不要等待，时机永远不会恰到好处。这不禁令我深思",
    "塞涅卡曾经说过, 生命如同寓言，其价值不在与长短，而在与内容。这不禁令我深思",
    "奥普拉·温弗瑞曾经说过, 你相信什么，你就成为什么样的人。这不禁令我深思",
    "吕凯特曾经说过, 生命不可能有两次，但许多人连一次也不善于度过。这不禁令我深思",
    "莎士比亚曾经说过, 人的一生是短的，但如果卑劣地过这一生，就太长了。这不禁令我深思",
    "笛卡儿曾经说过, 我的努力求学没有得到别的好处，只不过是愈来愈发觉自己的无知。这不禁令我深思",
    "左拉曾经说过, 生活的道路一旦选定，就要勇敢地走到底，决不回头。这不禁令我深思",
    "米歇潘曾经说过, 生命是一条艰险的峡谷，只有勇敢的人才能通过。这不禁令我深思",
    "吉姆·罗恩曾经说过, 要么你主宰生活，要么你被生活主宰。这不禁令我深思",
    "日本谚语曾经说过, 不幸可能成为通向幸福的桥梁。这不禁令我深思",
    "海贝尔曾经说过, 人生就是学校。在那里，与其说好的教师是幸福，不如说好的教师是不幸。这不禁令我深思",
    "杰纳勒尔·乔治·S·巴顿曾经说过, 接受挑战，就可以享受胜利的喜悦。这不禁令我深思",
    "德谟克利特曾经说过, 节制使快乐增加并使享受加强。这不禁令我深思",
    "裴斯泰洛齐曾经说过, 今天应做的事没有做，明天再早也是耽误了。这不禁令我深思",
    "歌德曾经说过, 决定一个人的一生，以及整个命运的，只是一瞬之间。这不禁令我深思",
    "卡耐基曾经说过, 一个不注意小事情的人，永远不会成就大事业。这不禁令我深思",
    "卢梭曾经说过, 浪费时间是一桩大罪过。这不禁令我深思",
    "康德曾经说过, 既然我已经踏上这条道路，那么，任何东西都不应妨碍我沿着这条路走下去。这不禁令我深思",
    "克劳斯·莫瑟爵士曾经说过, 教育需要花费钱，而无知也是一样。这不禁令我深思",
    "伏尔泰曾经说过, 坚持意志伟大的事业需要始终不渝的精神。这不禁令我深思",
    "亚伯拉罕·林肯曾经说过, 你活了多少岁不算什么，重要的是你是如何度过这些岁月的。这不禁令我深思",
    "韩非曾经说过, 内外相应，言行相称。这不禁令我深思",
    "富兰克林曾经说过, 你热爱生命吗？那么别浪费时间，因为时间是组成生命的材料。这不禁令我深思",
    "马尔顿曾经说过, 坚强的信心，能使平凡的人做出惊人的事业。这不禁令我深思",
    "笛卡儿曾经说过, 读一切好书，就是和许多高尚的人谈话。这不禁令我深思",
    "塞涅卡曾经说过, 真正的人生，只有在经过艰难卓绝的斗争之后才能实现。这不禁令我深思",
    "易卜生曾经说过, 伟大的事业，需要决心，能力，组织和责任感。这不禁令我深思",
    "歌德曾经说过, 没有人事先了解自己到底有多大的力量，直到他试过以后才知道。这不禁令我深思",
    "达尔文曾经说过, 敢于浪费哪怕一个钟头时间的人，说明他还不懂得珍惜生命的全部价值。这不禁令我深思",
    "佚名曾经说过, 感激每一个新的挑战，因为它会锻造你的意志和品格。这不禁令我深思",
    "奥斯特洛夫斯基曾经说过, 共同的事业，共同的斗争，可以使人们产生忍受一切的力量。　这不禁令我深思",
    "苏轼曾经说过, 古之立大事者，不惟有超世之才，亦必有坚忍不拔之志。这不禁令我深思",
    "王阳明曾经说过, 故立志者，为学之心也；为学者，立志之事也。这不禁令我深思",
    "歌德曾经说过, 读一本好书，就如同和一个高尚的人在交谈。这不禁令我深思",
    "乌申斯基曾经说过, 学习是劳动，是充满思想的劳动。这不禁令我深思",
    "别林斯基曾经说过, 好的书籍是最贵重的珍宝。这不禁令我深思",
    "富兰克林曾经说过, 读书是易事，思索是难事，但两者缺一，便全无用处。这不禁令我深思",
    "鲁巴金曾经说过, 读书是在别人思想的帮助下，建立起自己的思想。这不禁令我深思",
    "培根曾经说过, 合理安排时间，就等于节约时间。这不禁令我深思",
    "屠格涅夫曾经说过, 你想成为幸福的人吗？但愿你首先学会吃得起苦。这不禁令我深思",
    "莎士比亚曾经说过, 抛弃时间的人，时间也抛弃他。这不禁令我深思",
    "叔本华曾经说过, 普通人只想到如何度过时间，有才能的人设法利用时间。这不禁令我深思",
    "博曾经说过, 一次失败，只是证明我们成功的决心还够坚强。 维这不禁令我深思",
    "拉罗什夫科曾经说过, 取得成就时坚持不懈，要比遭到失败时顽强不屈更重要。这不禁令我深思",
    "莎士比亚曾经说过, 人的一生是短的，但如果卑劣地过这一生，就太长了。这不禁令我深思",
    "俾斯麦曾经说过, 失败是坚忍的最后考验。这不禁令我深思",
    "池田大作曾经说过, 不要回避苦恼和困难，挺起身来向它挑战，进而克服它。这不禁令我深思",
    "莎士比亚曾经说过, 那脑袋里的智慧，就像打火石里的火花一样，不去打它是不肯出来的。这不禁令我深思",
    "希腊曾经说过, 最困难的事情就是认识自己。这不禁令我深思",
    "黑塞曾经说过, 有勇气承担命运这才是英雄好汉。这不禁令我深思",
    "非洲曾经说过, 最灵繁的人也看不见自己的背脊。这不禁令我深思",
    "培根曾经说过, 阅读使人充实，会谈使人敏捷，写作使人精确。这不禁令我深思",
    "斯宾诺莎曾经说过, 最大的骄傲于最大的自卑都表示心灵的最软弱无力。这不禁令我深思",
    "西班牙曾经说过, 自知之明是最难得的知识。这不禁令我深思",
    "塞内加曾经说过, 勇气通往天堂，怯懦通往地狱。这不禁令我深思",
    "赫尔普斯曾经说过, 有时候读书是一种巧妙地避开思考的方法。这不禁令我深思",
    "笛卡儿曾经说过, 阅读一切好书如同和过去最杰出的人谈话。这不禁令我深思",
    "邓拓曾经说过, 越是没有本领的就越加自命不凡。这不禁令我深思",
    "爱尔兰曾经说过, 越是无能的人，越喜欢挑剔别人的错儿。这不禁令我深思",
    "老子曾经说过, 知人者智，自知者明。胜人者有力，自胜者强。这不禁令我深思",
    "歌德曾经说过, 意志坚强的人能把世界放在手中像泥块一样任意揉捏。这不禁令我深思",
    "迈克尔·F·斯特利曾经说过, 最具挑战性的挑战莫过于提升自我。这不禁令我深思",
    "爱迪生曾经说过, 失败也是我需要的，它和成功对我一样有价值。这不禁令我深思",
    "罗素·贝克曾经说过, 一个人即使已登上顶峰，也仍要自强不息。这不禁令我深思",
    "马云曾经说过, 最大的挑战和突破在于用人，而用人最大的突破在于信任人。这不禁令我深思",
    "雷锋曾经说过, 自己活着，就是为了使别人过得更美好。这不禁令我深思",
    "布尔沃曾经说过, 要掌握书，莫被书掌握；要为生而读，莫为读而生。这不禁令我深思",
    "培根曾经说过, 要知道对好事的称颂过于夸大，也会招来人们的反感轻蔑和嫉妒。这不禁令我深思",
    "莫扎特曾经说过, 谁和我一样用功，谁就会和我一样成功。这不禁令我深思",
    "马克思曾经说过, 一切节省，归根到底都归结为时间的节省。这不禁令我深思",
    "莎士比亚曾经说过, 意志命运往往背道而驰，决心到最后会全部推倒。这不禁令我深思",
    "卡莱尔曾经说过, 过去一切时代的精华尽在书中。这不禁令我深思",
    "培根曾经说过, 深窥自己的心，而后发觉一切的奇迹在你自己。这不禁令我深思",
    "罗曼·罗兰曾经说过, 只有把抱怨环境的心情，化为上进的力量，才是成功的保证。这不禁令我深思",
    "孔子曾经说过, 知之者不如好之者，好之者不如乐之者。这不禁令我深思",
    "达·芬奇曾经说过, 大胆和坚定的决心能够抵得上武器的精良。这不禁令我深思",
    "叔本华曾经说过, 意志是一个强壮的盲人，倚靠在明眼的跛子肩上。这不禁令我深思",
    "黑格尔曾经说过, 只有永远躺在泥坑里的人，才不会再掉进坑里。这不禁令我深思",
    "普列姆昌德曾经说过, 希望的灯一旦熄灭，生活刹那间变成了一片黑暗。这不禁令我深思",
    "维龙曾经说过, 要成功不需要什么特别的才能，只要把你能做的小事做得好就行了。这不禁令我深思",
    "郭沫若曾经说过, 形成天才的决定因素应该是勤奋。这不禁令我深思",
    "洛克曾经说过, 学到很多东西的诀窍，就是一下子不要学很多。这不禁令我深思",
    "西班牙曾经说过, 自己的鞋子，自己知道紧在哪里。这不禁令我深思",
    "拉罗什福科曾经说过, 我们唯一不会改正的缺点是软弱。这不禁令我深思",
    "亚伯拉罕·林肯曾经说过, 我这个人走得很慢，但是我从不后退。这不禁令我深思",
    "美华纳曾经说过, 勿问成功的秘诀为何，且尽全力做你应该做的事吧。这不禁令我深思",
    "俾斯麦曾经说过, 对于不屈不挠的人来说，没有失败这回事。这不禁令我深思",
    "阿卜·日·法拉兹曾经说过, 学问是异常珍贵的东西，从任何源泉吸收都不可耻。这不禁令我深思",
    "白哲特曾经说过, 坚强的信念能赢得强者的心，并使他们变得更坚强。 这不禁令我深思",
    "查尔斯·史考伯曾经说过, 一个人几乎可以在任何他怀有无限热忱的事情上成功。 这不禁令我深思",
    "贝多芬曾经说过, 卓越的人一大优点是：在不利与艰难的遭遇里百折不饶。这不禁令我深思",
    "莎士比亚曾经说过, 本来无望的事，大胆尝试，往往能成功。这不禁令我深思",
    "卡耐基曾经说过, 我们若已接受最坏的，就再没有什么损失。这不禁令我深思",
    "德国曾经说过, 只有在人群中间，才能认识自己。这不禁令我深思",
    "史美尔斯曾经说过, 书籍把我们引入最美好的社会，使我们认识各个时代的伟大智者。这不禁令我深思",
    "冯学峰曾经说过, 当一个人用工作去迎接光明，光明很快就会来照耀着他。这不禁令我深思",
    "吉格·金克拉曾经说过, 如果你能做梦，你就能实现它。这不禁令我深思",
]

后面垫话 = [
    "这不禁令我深思",
    "带着这句话, 我们还要更加慎重的审视这个问题: ",
    "这启发了我",
    "我希望诸位也能好好地体会这句话. ",
    "这句话语虽然很短, 但令我浮想联翩. ",
]

前面垫话 = [
    "曾经说过",
    "在不经意间这样说过",
]


def 来点名人名言():
    xx = 名人名言[random.randint(0, len(名人名言)-1)]
    xx = xx.replace("曾经说过", 前面垫话[random.randint(0, len(前面垫话)-1)])
    xx = xx.replace("这不禁令我深思", 后面垫话[random.randint(0, len(后面垫话)-1)])
    return xx


def 另起一段():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx

    # print(tmp)


def GPBT(strWords):
    xx = strWords
    for x in xx:
        tmp = str()
        while (len(tmp) < 2000):
            分支 = random.randint(0, 100)
            if 分支 < 5:
                tmp += 另起一段()
            elif 分支 < 20:
                tmp += 来点名人名言()
            else:
                tmp += text[random.randint(0, len(text)-1)]
        tmp = tmp.replace("x", xx)
        return tmp

# -----------------------------------------------------------------------------------------


def AIXXX(context):
    RUN_DEVICE = 'cpu'  # gpu 或 dml 或 cpu
    MODEL_NAME = 'model/wangwen-2022-02-15'  # 模型名
    WORD_NAME = 'model/wangwen-2022-02-15'  # 这个也修改
    NUM_OF_RUNS = 1  # 写多少遍
    LENGTH_OF_EACH = 220  # 每次写多少字
    top_p = 0.75  # 这个的范围是 0 到 1。越大，变化越多。越小，生成效果越规矩。自己试试 0 和 0.5 和 1.0 的效果就知道了
    top_p_newline = 0.9

    ctx_len = 512
    n_layer = 12
    n_head = 12
    n_embd = n_head * 64
    n_attn = n_embd
    n_ffn = n_embd

    #print("输入=====>" + context)
    context = context.strip().split('\n')
    for c in range(len(context)):
        context[c] = context[c].strip().strip('\u3000')
    context = '\n' + ('\n'.join(context)).strip()
    #print('您输入的开头有 ' + str(len(context)) + ' 个字。注意，模型只会看最后 ' + str(ctx_len) + ' 个字。')

    with open(WORD_NAME + '.json', "r", encoding="utf-16") as result_file:
        word_table = json.load(result_file)

    vocab_size = len(word_table)

    train_dataset = lambda: None
    train_dataset.stoi = {v: int(k) for k, v in word_table.items()}
    train_dataset.itos = {int(k): v for k, v in word_table.items()}
    UNKNOWN_CHAR = train_dataset.stoi['\ue083']

    #print(f'\nLoading model for {RUN_DEVICE}...', end=' ')
    if RUN_DEVICE == 'dml':
        import onnxruntime as rt
        sess_options = rt.SessionOptions()
        sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.execution_mode = rt.ExecutionMode.ORT_SEQUENTIAL
        sess_options.enable_mem_pattern = False
        rt_session = rt.InferenceSession(
            MODEL_NAME + '.onnx', sess_options=sess_options, providers=['DmlExecutionProvider'])
        rt_session.set_providers(['DmlExecutionProvider'])
    else:
        model = GPT(GPTConfig(vocab_size, ctx_len, n_layer=n_layer, n_head=n_head, n_embd=n_embd, n_attn=n_attn, n_ffn=n_ffn))
        m2 = torch.load(MODEL_NAME + '.pth', map_location='cpu').state_dict()
        for i in range(n_layer):
            prefix = f'blocks.{i}.attn.'
            time_w = m2[prefix + 'time_w']
            time_alpha = m2[prefix + 'time_alpha']
            time_beta = m2[prefix + 'time_beta']

            TT = ctx_len
            T = ctx_len
            w = F.pad(time_w, (0, TT))
            w = torch.tile(w, [TT])
            w = w[:, :-TT].reshape(-1, TT, 2 * TT - 1)
            w = w[:, :, TT-1:]
            w = w[:, :T, :T] * time_alpha[:, :, :T] * time_beta[:, :T, :]

            m2[prefix + 'time_ww'] = w
            del m2[prefix + 'time_w']
            del m2[prefix + 'time_alpha']
            del m2[prefix + 'time_beta']
        if RUN_DEVICE == 'gpu':
            model = model.cuda()
        model.load_state_dict(m2)

    #print('done:', MODEL_NAME, '&', WORD_NAME)

    ##############################################################################

    strAllResult = ""
    for run in range(NUM_OF_RUNS):

        x = np.array([train_dataset.stoi.get(s, UNKNOWN_CHAR)
                     for s in context], dtype=np.int64)

        real_len = len(x)
        print_begin = 0

        for i in range(LENGTH_OF_EACH):

            if i == 0:

                #print(('-' * 60) + '\n' + context.replace('\n', '\n  ').strip('\n'), end = '')
                strAllResult += '\n' + \
                    context.replace('\n', '\n  ').strip('\n')
                print_begin = real_len

            with torch.no_grad():
                if RUN_DEVICE == 'dml':
                    if real_len < ctx_len:
                        xxx = np.pad(x, (0, ctx_len - real_len))
                    else:
                        xxx = x
                    out = rt_session.run(
                        None, {rt_session.get_inputs()[0].name: [xxx[-ctx_len:]]})
                    out = torch.tensor(out[0])
                else:
                    xxx = torch.tensor(
                        x[-ctx_len:], dtype=torch.long)[None, ...]
                    if RUN_DEVICE == 'gpu':
                        xxx = xxx.cuda()
                    out, _ = model(xxx)
                out[:, :, UNKNOWN_CHAR] = -float('Inf')
            pos = -1 if real_len >= ctx_len else real_len - 1

            if train_dataset.itos[int(x[real_len-1])] == '\n':
                char = src.utils.sample_logits(
                    out, pos, temperature=1.0, top_p=top_p_newline)
            else:
                char = src.utils.sample_logits(
                    out, pos, temperature=1.0, top_p=top_p)

            x = np.append(x, char)
            real_len += 1

            if i % 2 == 1 or i == LENGTH_OF_EACH-1 or i < 10 or RUN_DEVICE != 'gpu':
                completion = ''.join([train_dataset.itos[int(i)]
                                     for i in x[print_begin:real_len]])
                strAllResult += completion.replace('\n', '\n  ')
                #print(completion.replace('\n', '\n  '), end = '', flush=True)
                print_begin = real_len

    # print("结果===>"+strAllResult)
    return strAllResult


# ------------------------------幻影坦克------------------------------
def linear_add(pic1, pic2):
    out = pic1 + pic2
    out[out > 255] = 255
    return out


def divide(pic1, pic2):
    pic2 = pic2.astype(np.float64)
    pic2[pic2 == 0] = 1e-10
    out = (pic1 / pic2) * 255
    out[out > 255] = 255
    return out


def inversion(pic):
    return 255 - pic


def rgb2gray(pic):
    pic_shape = pic.shape
    out = np.ones((pic_shape[0], pic_shape[1], 4)) * 255
    temp = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    out[:, :, 0] = temp
    out[:, :, 1] = temp
    out[:, :, 2] = temp
    return out.astype(np.uint8)


def get_red_channel(pic):
    return pic[:, :, 2]


def add_alpha(pic, A):
    pic[:, :, 3] = A
    return pic


def change_color_level(pic, is_light):
    light_table = [120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126, 126, 127, 127, 128, 128,
                   129, 129, 130, 130, 131, 132, 132, 133, 133, 134, 134, 135, 135, 136, 136, 137, 137, 138,
                   138, 139, 139, 140, 140, 141, 142, 142, 143, 143, 144, 144, 145, 145, 146, 146, 147, 147,
                   148, 148, 149, 149, 150, 150, 151, 152, 152, 153, 153, 154, 154, 155, 155, 156, 156, 157,
                   157, 158, 158, 159, 159, 160, 161, 161, 162, 162, 163, 163, 164, 164, 165, 165, 166, 166,
                   167, 167, 168, 168, 169, 170, 170, 171, 171, 172, 172, 173, 173, 174, 174, 175, 175, 176,
                   176, 177, 177, 178, 179, 179, 180, 180, 181, 181, 182, 182, 183, 183, 184, 184, 185, 185,
                   186, 186, 187, 188, 188, 189, 189, 190, 190, 191, 191, 192, 192, 193, 193, 194, 194, 195,
                   195, 196, 197, 197, 198, 198, 199, 199, 200, 200, 201, 201, 202, 202, 203, 203, 204, 205,
                   205, 206, 206, 207, 207, 208, 208, 209, 209, 210, 210, 211, 211, 212, 212, 213, 214, 214,
                   215, 215, 216, 216, 217, 217, 218, 218, 219, 219, 220, 220, 221, 222, 222, 223, 223, 224,
                   224, 225, 225, 226, 226, 227, 227, 228, 228, 229, 229, 230, 231, 231, 232, 232, 233, 233,
                   234, 234, 235, 235, 236, 236, 237, 237, 238, 239, 239, 240, 240, 241, 241, 242, 242, 243,
                   243, 244, 244, 245, 245, 246, 247, 247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252,
                   253, 253, 254, 255]
    dark_table = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
                  10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21,
                  22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 32, 32,
                  33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 41, 41, 42, 42, 43, 43,
                  44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54,
                  55, 55, 56, 56, 57, 57, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
                  66, 66, 67, 68, 68, 69, 69, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 77,
                  77, 78, 78, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 84, 85, 85, 86, 86, 87, 87, 88,
                  88, 89, 89, 90, 90, 91, 91, 92, 92, 93, 94, 94, 95, 95, 96, 96, 97, 97, 98, 98, 99,
                  99, 100, 100, 101, 102, 102, 103, 103, 104, 104, 105, 105, 106, 106, 107, 107, 108,
                  108, 109, 109, 110, 111, 111, 112, 112, 113, 113, 114, 114, 115, 115, 116, 116, 117,
                  117, 118, 119, 119, 120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126,
                  127, 127, 128, 128, 129, 129, 130, 130, 131, 131, 132, 132, 133, 133, 134, 135]

    pic_shape = pic.shape
    out = np.zeros((pic_shape[0], pic_shape[1], 4), dtype=np.uint8)
    if is_light:
        out[:, :, 0] = [[light_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[light_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[light_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    else:
        out[:, :, 0] = [[dark_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[dark_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[dark_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    return out


def make(file1, file2, savePath):
    surface_pic = cv2.imread(file1)
    hidden_pic = cv2.imread(file2)
    sur_shape = surface_pic.shape
    hid_shape = hidden_pic.shape

    #print("aaaa" + str(sur_shape[0]) + "   " + str(hid_shape[0])+ "   " + str(sur_shape[1])+ "   " +str(hid_shape[1]))
    out_shape = (hid_shape[1], hid_shape[0])
    surface_pic = cv2.resize(surface_pic, out_shape)
    hidden_pic = cv2.resize(hidden_pic, out_shape)

    surface_pic = rgb2gray(surface_pic)
    surface_pic = change_color_level(surface_pic, True)
    surface_pic = inversion(surface_pic)

    hidden_pic = rgb2gray(hidden_pic)
    hidden_pic = change_color_level(hidden_pic, False)

    out_pic = linear_add(surface_pic, hidden_pic)
    A = get_red_channel(out_pic)
    out_pic = divide(hidden_pic, out_pic)
    out_pic = add_alpha(out_pic, A)
    #cv2.imwrite(savePath, out_pic,  [int(cv2.IMWRITE_PNG_COMPRESSION), 7])
    base64_str = cv2.imencode('.png', out_pic)[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode()
    return base64_str
# ----------------------------------------------------------------------------------


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def to_unicode(check_str):
    ret = ""
    for v in check_str:
        ret = ret + hex(ord(v)).upper().replace("0X", "\\u")
    return ret


# ---------------------------------------------------------------------------------
LEFT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 2
LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 1
RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_RADII = 10
BG_COLOR = "#000000"
BOX_COLOR = "#F7971D"
LEFT_TEXT_COLOR = "#FFFFFF"
RIGHT_TEXT_COLOR = "#000000"
FONT_SIZE = 50

FONT_PATH = "./ArialEnUnicodeBold.ttf"
assert FONT_PATH is not None, "请自己处理字体路径"

# SavePic ---------------------------------------------------------------------------------------------------------------


def SavePic(urlTB):
    html = requests.get(urlTB)
    with open('./MJX.png', 'wb') as file:
        file.write(html.content)


def SavePic2222(urlTB):
    html = requests.get(urlTB)
    with open('./MJX2.png', 'wb') as file:
        file.write(html.content)


# ----------------------------------------------------------------------------------------------------------------


# clclc---------------------------------------------------------------------------------
def ciliSou(strSearch, nmmm):
    urlss = "https://zhaocili307.xyz/s.php?q=" + strSearch
    strText = requests.get(urlss).text
    strTemp11 = strText

    textArr = []
    textTTTTArr = []
    sizeArr = []
    arr1 = strTemp11.split('cililianjie/')

    # print(len(arr1))

    for ao1 in arr1:
        if ao1.find('.html" title="') > -1:
            arreee = ao1.split('.html" title="')

            ttstrt = arreee[1]
            aaaRRR = ttstrt.split('">')
            strTTTT = aaaRRR[0]
            textTTTTArr.append(strTTTT)
            textArr.append(arreee[0])
            strSIZEArr = aaaRRR[2].split('<')
            sizeArr.append(strSIZEArr[0])

    # print(textArr[0])
    # print(textTTTTArr[0])

    nLength = len(textTTTTArr)
    if nmmm > nLength:
        nmmm = nLength

    if nLength > nmmm:
        nLength = nmmm
    strResult = ''
    for i in range(nLength):
        strUUU = textArr[i]
        strTTTI = textTTTTArr[i]
        strLine = "《" + strTTTI + "》大小:" + \
            sizeArr[i] + " 地址：magnet:?xt=urn:btih:" + strUUU+" \n "
        strResult = strResult + strLine

    # print(strResult)
    return strResult

# -----------------------------------------------------------------------


# ---------------------------------------------
beast = ['嗷', '呜', '啊', '~']


def str2hex(text: str):
    ret = ""
    for x in text:
        charHexStr = hex(ord(x))[2:]
        if len(charHexStr) == 3:
            charHexStr = "0" + charHexStr
        elif len(charHexStr) == 2:
            charHexStr = "00" + charHexStr
        ret += charHexStr
    return ret


def hex2str(text: str):
    ret = ""
    for i in range(0, len(text), 4):
        unicodeHexStr = text[i:i + 4]
        charStr = chr(int(unicodeHexStr, 16))
        ret += charStr
    return ret


def encoder(str):
    hexArray = list(str2hex(str))
    code = ""
    n = 0
    for x in hexArray:
        k = int(x, 16) + n % 16
        if k >= 16:
            k -= 16
        code += beast[int(k / 4)] + beast[k % 4]
        n += 1
    return code


def decoder(str):
    hexArray = list(str)
    code = ""
    for i in range(0, len(hexArray), 2):
        pos1 = beast.index(hexArray[i])
        pos2 = beast.index(hexArray[i + 1])
        k = ((pos1 * 4) + pos2) - (int(i / 2) % 16)
        if k < 0:
            k += 16
        code += hex(k)[2:]
    return hex2str(code)



# ---------------------------------------------


# --------------------------------------------------------------------------
def jiemi(strText):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    aaaa = {
        'text': strText
    }
    try:
        resultStr = ""
        r = json.loads(requests.post(url, data=aaaa).text)
        # print(str(r))
        name = r[0]['name']
        trans = r[0]['trans']
        resultStr = "\n缩写是" + (name) + "\n 结果可能是" + (str(trans))
        # print(resultStr)
        return resultStr
    except:
        # print(str(err))
        return "解密失败！！！！！！！！！！！"


# --------------------------------------------------------------------------


# 摩斯码 CODE----------------------------------------------------------------------------

def wv(t, f, v, wf):
    sr = 8000
    '''
    t:写入时长
    f:声音频率
    v：音量
    wf：一个可以写入的音频文件
    sr：采样率
    '''
    tt = 0
    dt = 1.0/sr
    while tt <= t:
        s = math.sin(tt*math.pi*2*f)*v*32768  # 采样，调节音量，映射到[-2^15,2^15)
        s = int(s)
        fd = struct.pack("h", s)  # 转换成8bit二进制数据
        wf.writeframes(fd)  # 写入音频文件
        tt += dt  # 时间流逝


MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '
    return cipher


def decrypt(message):

    message += ' '

    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                                                              .values()).index(citext)]
                citext = ''
    return decipher


def mainMorse(msg, FromGroupId):

    ff = wave.open("./morse.wav", "w")
    ff.setframerate(8000)
    ff.setnchannels(1)
    ff.setsampwidth(2)

    message = msg
    if u'\u0039' >= message >= u'\u0030' or u'\u005a' >= message >= u'\u0041' or u'\u007a' >= message >= u'\u0061':  # 判断是否只有数字字母
        li = encrypt(message.upper())
        #print (li)
        mo = []
        for i in li:
            if i == "-":
                mo.append("2")
                mo.append("0")
            elif i == ".":
                mo.append("1")
                mo.append("0")
            elif i == " ":
                mo.append("3")
        # print(mo)
        lo = []
        for i in mo:
            if i == "0" or i == "1":
                lo.append(1)
            elif i == "2" or i == "3":
                lo.append(3)
        # print(lo)
        note = {"1": 600, "2": 600, "3": 0, "0": 0}  # 600是滴答正玄波频率，如更改2个都改
        for i in range(len(mo)):
            wv(lo[i]/17.0, note[mo[i]], 0.8, ff)  # 改变17数值cw快慢
        ff.close()

        with open('./morse.wav', 'rb') as ffff:
            dataffff = ffff.read()
            encodestr = base64.b64encode(dataffff).decode()  # 得到 byte 编码的数据
            action.sendGroupVoice(FromGroupId, voiceBase64Buf=encodestr)
        return True
    else:
        result = decrypt(message)
        return False
        #print (result)


# -------------------------------------------------------------------------------------


# -----JIKI----------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------jiki一下
#from error import error

class Jiki:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Client": "web",
            "Client-Version": "2.1.66a",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }
        self.auto_complete = "https://api.jikipedia.com/go/auto_complete"
        self.api = "https://api.jikipedia.com/go/search_definitions"
        self.eval_cqp_data = ""

    def check(self, word):

        if len(word) > 10:
            return {"res": "不支持该类型消息", "error": 99}
        else:
            i = {}
            i["error"] = 0
            i["title"], i["res"] = self.jiki(word)
            i["complete"] = self.complete(word)
            return i

    def jiki(self, word):

        data = {
            "phrase": word,
            "page": 1
        }
        try:
            resp = requests.post(self.api, headers=self.headers,
                                 data=json.dumps(data), timeout=10)
        except:
            return "", "查询错误 ERROR 机器人即将爆炸"
        resp.encoding = "utf8"
        try:
            resp = json.loads(resp.text)["data"]
            # resp = json.loads(resp.text)["data"][0]
            for i, j in enumerate(resp):
                # print(resp[i]["term"]["title"])
                if word == resp[i]["term"]["title"]:
                    title = resp[i]["term"]["title"]
                    # res = resp["content"].replace("]","")
                    res = re.sub(
                        r"\[.*?:", "", resp[i]["content"].replace("]", ""))
                    break
            else:
                i = random.randint(1, len(resp))-1
                title = resp[i]["term"]["title"]
                # res = res[0]["content"].replace("]","")
                res = re.sub(
                    r"\[.*?:", "", resp[i]["content"].replace("]", ""))
        except Exception as e:
            # print(e)
            return "", "查找不到相关释义"
        else:
            return title, res
            # return res.replace("\n","")

    def complete(self, word):

        data = {
            "phrase": word
        }
        try:
            resp = requests.post(
                self.auto_complete, headers=self.headers, data=json.dumps(data), timeout=10)
        except:
            res = error(self.eval_cqp_data)
            return res
        resp.encoding = "utf8"
        d = json.loads(resp.text)["data"]
        if d == []:
            return "联想词:无"
        else:
            return "联想词为:\n{}".format(",".join([i["word"] for i in d[:10]]))


jkjk = Jiki()


# -------------PH PIC----------------------------------------------------------
# -----------------------------------------------------------------------------
# -------------------------------------------------------------------------------

def create_left_part_img(text: str, font_size: int, type_="h"):
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    if type_ == "h":
        blank_height = font_height * 2
    else:
        blank_height = font_height
    right_blank = int(
        font_width / len(text) * LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH
    )
    img_height = font_height + offset_y + blank_height * 2
    image_width = font_width + right_blank
    image_size = image_width, img_height
    image = Image.new("RGBA", image_size, BG_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((0, blank_height), text, fill=LEFT_TEXT_COLOR, font=font)
    return image


def create_right_part_img(text: str, font_size: int):
    radii = RIGHT_PART_RADII
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    blank_height = font_height * RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT
    left_blank = int(
        font_width / len(text) *
        RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH
    )
    image_width = font_width + 2 * left_blank
    image_height = font_height + offset_y + blank_height * 2
    image = Image.new("RGBA", (image_width, image_height), BOX_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((left_blank, blank_height), text,
              fill=RIGHT_TEXT_COLOR, font=font)

    # 圆
    magnify_time = 10
    magnified_radii = radii * magnify_time
    circle = Image.new(
        "L", (magnified_radii * 2, magnified_radii * 2), 0
    )  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, magnified_radii * 2, magnified_radii * 2),
                 fill=255)  # 画白色圆形

    # 画4个角（将整圆分离为4个部分）
    magnified_alpha_width = image_width * magnify_time
    magnified_alpha_height = image_height * magnify_time
    alpha = Image.new("L", (magnified_alpha_width,
                      magnified_alpha_height), 255)
    alpha.paste(circle.crop(
        (0, 0, magnified_radii, magnified_radii)), (0, 0))  # 左上角
    alpha.paste(
        circle.crop((magnified_radii, 0, magnified_radii * 2, magnified_radii)),
        (magnified_alpha_width - magnified_radii, 0),
    )  # 右上角
    alpha.paste(
        circle.crop(
            (magnified_radii, magnified_radii,
             magnified_radii * 2, magnified_radii * 2)
        ),
        (
            magnified_alpha_width - magnified_radii,
            magnified_alpha_height - magnified_radii,
        ),
    )  # 右下角
    alpha.paste(
        circle.crop((0, magnified_radii, magnified_radii, magnified_radii * 2)),
        (0, magnified_alpha_height - magnified_radii),
    )  # 左下角
    alpha = alpha.resize((image_width, image_height), Image.ANTIALIAS)
    image.putalpha(alpha)
    return image


def combine_img_horizontal(
    left_text: str, right_text, font_size: int = FONT_SIZE
) -> str:
    left_img = create_left_part_img(left_text, font_size)
    right_img = create_right_part_img(right_text, font_size)
    blank = 30
    bg_img_width = left_img.width + right_img.width + blank * 2
    bg_img_height = left_img.height
    bg_img = Image.new("RGBA", (bg_img_width, bg_img_height), BG_COLOR)
    bg_img.paste(left_img, (blank, 0))
    bg_img.paste(
        right_img,
        (blank + left_img.width, int((bg_img_height - right_img.height) / 2)),
        mask=right_img,
    )
    buffer = io.BytesIO()
    bg_img.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode()


def combine_img_vertical(left_text: str, right_text, font_size: int = FONT_SIZE) -> str:
    left_img = create_left_part_img(left_text, font_size, type_="v")
    right_img = create_right_part_img(right_text, font_size)
    blank = 15
    bg_img_width = max(left_img.width, right_img.width) + blank * 2
    bg_img_height = left_img.height + right_img.height + blank * 2
    bg_img = Image.new("RGBA", (bg_img_width, bg_img_height), BG_COLOR)
    bg_img.paste(left_img, (int((bg_img_width - left_img.width) / 2), blank))
    bg_img.paste(
        right_img,
        (int((bg_img_width - right_img.width) / 2), blank + left_img.height),
        mask=right_img,
    )
    buffer = io.BytesIO()
    bg_img.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode()


# --AI CHAT--------------------------------------------------------------------------------#--------------------------------------------------------------------------------------#---------------------------------------------------------------------------------
uid = '1'


def chatAI(text='hello'):
    try:
        # TULING_KEY = '059f9782bab24de6a63d4083590a803b'  7c8cdb56b0dc4450a8deef30a496bd4c
        apikey = '059f9782bab24de6a63d4083590a803b'
        api_url = 'http://www.tuling123.com/openapi/api'
        data = {'key': apikey, 'info': text}
        req = requests.post(api_url, data=data).text
        replys = json.loads(req)['text']
        return replys
    except:
        return "error_chatAI"


# -- yuban10703 -------------------------------------------------------------------------------#--------------------------------------------------------------------------------------#---------------------------------------------------------------------------------
def getYubanPic(tags, pon="0"):
    try:
        # 0:safe,1:nos,2:all
        api_url = 'https://setu.yuban10703.xyz/setu?r18=' + \
            str(pon) + '&num=1&tags=' + tags
        #data = {'r18': 0, 'num': 1, "tags":[]}
        req = requests.get(api_url).text

        if(json.loads(req)["detail"] and json.loads(req)["detail"][0] == "色"):
            llolo_url = 'https://api.lolicon.app/setu/v2?size=original&?r18=' + \
                str(pon) + '&num=1&keyword=' + "黑丝"
            req2222 = requests.get(llolo_url).text
            datas22 = json.loads(req2222)["data"]
            if len(datas22) <= 0:
                return json.loads(req)["detail"]
            else:
                dataatata22 = datas22[0]
                picOriginalUrl_Msg222 = dataatata22["urls"]["original"].replace(
                    "i.pixiv.cat", "i.pixiv.re")
                # print("//////====>picOriginalUrl_Msg=> " + str(picOriginalUrl_Msg222))
                return picOriginalUrl_Msg222
        else:
            datas = json.loads(req)["data"]
            dataatata = datas[0]
            picOriginalUrl = dataatata["urls"]["original"]
            picLargeUrl = dataatata["urls"]["large"].replace(
                "_webp", "").replace("i.pximg.net", "i.pixiv.re")
            picMediumUrl = dataatata["urls"]["medium"].replace(
                "_webp", "").replace("i.pximg.net", "i.pixiv.re")
            picOriginalUrl_Msg = dataatata["urls"]["original"].replace(
                "i.pximg.net", "i.pixiv.re")

            #print("//////====>picOriginalUrl_Msg=> " + str(picMediumUrl))
            return picOriginalUrl_Msg
    except Exception as e:
        return "获取图片出错===>" + str(e)+" tags "+tags+" pn "+pon


class __redirection__:
    def __init__(self):
        self.buff=''
        self.__console__=sys.stdout
        
    def write(self, output_stream):
        self.buff+=output_stream
        
    def flush(self):
        self.buff=''
        
    def reset(self):
        sys.stdout=self.__console__


# ----------------RECIVE-------------------------#--------------------------------------------------------------------------------------#---------------------------------------------------------------------------------
@bot.on_group_msg
@deco.ignore_botself
@deco.these_msgtypes('TextMsg')
def OnGroupMSG(ctx: GroupMsg):
    global bOpenThisBOT
    global dataCiliGroupData
    global dataSetuGroupData
    global nReciveTimes
    global bMasterQQ

    global bGameStarted
    global bSaoLeiStart
    global action_stack
    global status
    global mt
    global nXXXCount
    global bBotClose
    global botQQ
    global plpDataArr
    global mrDataArr
    global bCloseXX
    global blackList
    if bBotClose:
        # action.sendGroupText(ctx.FromGroupId, "已关机")
        return 1

    strGID = str(ctx.FromGroupId)
    strCont = ctx.Content
    strSendQQID = str(ctx.FromUserId)

    if strCont.startswith("小说续写") or strCont.startswith("续写") or strCont.startswith("小说续写"):
        if bCloseXX:
            action.sendGroupText(ctx.FromGroupId, "电脑需要办公, 暂时停掉续写功能")
            return 1
        ccc = 15
        if blackList[0] == ctx.FromGroupId:
            ccc = 0
        if CheckCoins(strSendQQID, ccc, ctx.FromGroupId) == False:
            return 1
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        strHead = args[0]
        strSsss = strCont.replace(strHead, "")
        nXXXCount += 1
        if(nXXXCount > 1):
            action.sendGroupText(ctx.FromGroupId, "任务太多,等等等再试试!!!!!!")
            nXXXCount -= 1
        else:
            action.sendGroupText(ctx.FromGroupId, "好的,我正在构思")
    
            strres = ""
            try:
                strres = AIXXX(strSsss)
            except Exception as eses: 
                strres = str(eses)
            # strres = AIXXX(strSsss)
            action.sendGroupText(ctx.FromGroupId, strres)
            nXXXCount -= 1

    if blackList[0] == ctx.FromGroupId:
        return 1

    if botQQ == ctx.FromUserId:
        return 1
    nReciveTimes = nReciveTimes + 1
    #logger.success('nReciveTimes= ' + str(nReciveTimes))

    if random.random() < 0.0001:
        reeee = chs2yin(strCont, 0)
        action.sendGroupText(ctx.FromGroupId, reeee)

    if strCont.startswith("扔漂流瓶"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        strHead = args[0]
        strSssspplp = strCont.replace(strHead, "")
        plpData1 = {"qquid": ctx.FromUserId, "ctx": strSssspplp, "gName":ctx.FromGroupId}
        plpDataArr.append(plpData1)
        action.sendGroupText(ctx.FromGroupId, "成功扔掉漂流瓶, 等人捞到吧!")
        savePLPJson()
    if strCont.startswith("获取漂流瓶"):
        if len(plpDataArr) > 0:
            allL = len(plpDataArr)
            nRIndex = random.randint(0, allL-1)
            plpData = plpDataArr[nRIndex]
            # NQID = int(plpData["qquid"] / 10000)
            NQID = plpData["qquid"]
            NGID = plpData["gName"]
            strPLP = "捞到一个QQ号:"+ str(NQID) +" 在群("+ str(NGID) +")中发送的漂流瓶.\n里面有张纸条, 内容是:\n"+ str(plpData["ctx"])
            plpDataArr.remove(plpData)
            # print(str(plpData["qquid"]) +  " strPLPstrPLP===>" + strPLP)
            action.sendGroupText(ctx.FromGroupId, strPLP)
            savePLPJson()
        else:
            action.sendGroupText(ctx.FromGroupId, "大海中已经没漂流瓶了!", ctx.FromUserId)
    if strCont.startswith("获取管理员"):
        userslist = action.getGroupAdminList(ctx.FromGroupId)
        strUL = ""
        for x in userslist:
            strUL += "管理员: "+x["NickName"]+", QQ号:"+str(x["MemberUin"])+"\n"
        action.sendGroupText(ctx.FromGroupId, strUL)
    if strCont.startswith("发病"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            re222 = chs2yin(args[1], 0)
            action.sendGroupText(ctx.FromGroupId, re222)

    if strCont.startswith("添加白名单") and ctx.FromUserId == bMasterQQ:
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            aaa = args[1]
            dataCiliGroupData[aaa] = True
            dataSetuGroupData[aaa] = True
            dataNudeGroupData[aaa] = True
            action.sendGroupText(ctx.FromGroupId, "此群内可以使用色图, 磁力, 脱衣")
    if strCont == "关闭磁力" and ctx.FromUserId == bMasterQQ:
        dataCiliGroupData[strGID] = False
        action.sendGroupText(ctx.FromGroupId, "本群磁力已关闭", ctx.FromUserId)

    if strCont == "开启磁力" and ctx.FromUserId == bMasterQQ:
        dataCiliGroupData[strGID] = True
        action.sendGroupText(ctx.FromGroupId, "本群磁力已开启", ctx.FromUserId)

    if strCont == "关闭色图" and ctx.FromUserId == bMasterQQ:
        dataSetuGroupData[strGID] = False
        action.sendGroupText(ctx.FromGroupId, "本群色图已关闭", ctx.FromUserId)

    if strCont == "开启色图" and ctx.FromUserId == bMasterQQ:
        dataSetuGroupData[strGID] = True
        action.sendGroupText(ctx.FromGroupId, "本群色图已开启", ctx.FromUserId)


#================================================
    if strCont == "系统信息":
        strSYSY = sysinfo()
        # print(strSYSY)
        action.sendGroupText(ctx.FromGroupId, strSYSY, ctx.FromUserId)

# clici================================
    if strCont.startswith("磁力搜"):
        bbb = False
        try:
            bbb = dataCiliGroupData[strGID]
        except:
            bbb = False

        if bbb == False:
            action.sendGroupText(
                ctx.FromGroupId, "磁力关掉了, 请联系主人, 找不到就算了", ctx.FromUserId)
            return 1
        if CheckCoins(strSendQQID, 20, ctx.FromGroupId) == False:
            return 1
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strSs = args[1]
            strRRqq = ciliSou(strSs, 6)
            action.sendGroupText(ctx.FromGroupId, strRRqq)
        elif len(args) == 3:
            strSs = args[1]
            nMMM = int(args[2])
            strRRqq = ciliSou(strSs, nMMM)
            action.sendGroupText(ctx.FromGroupId, strRRqq)

# AIAI
    if strCont.startswith("运行代码") and ctx.FromUserId == bMasterQQ:
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        strHead1 = args[0]
        strSsss = strCont.replace(strHead1, "")
        strEEE = ""
        try:
            r_obj = __redirection__()
            sys.stdout = r_obj
            sys.stdout.flush()
            strEEE = str(eval(strSsss))
            strEEE += "\n"+sys.stdout.buff
        except BaseException as err:
            strEEE = str(err)
        action.sendGroupText(ctx.FromGroupId, strEEE)

    if strCont == "关闭续写":
        bCloseXX = True
        action.sendGroupText(ctx.FromGroupId, "关闭续写")
    if strCont == "开启续写":
        bCloseXX = False
        action.sendGroupText(ctx.FromGroupId, "开启续写")

        

# 垃圾分类============================================================================
    if strCont.startswith("垃圾分类"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) >= 2:
            asdas = args[1]
            strUUUDDD = "https://api.vvhan.com/api/la.ji?lj=" + asdas
            res = requests.get(strUUUDDD).text
            #print("asdasda===>" + res)
            jsjsjs = json.loads(res)
            strRRqq123 = "这个垃圾=> "+asdas+" " + jsjsjs["sort"]
            action.sendGroupText(ctx.FromGroupId, strRRqq123)

# PORNHUB PIC---------------------------------------------------------------------------------------
    if strCont.startswith("ph ") or strCont.startswith("作图 ") or strCont.startswith("做图 "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) >= 3:
            left = args[1]
            right = args[2]
            func = combine_img_horizontal
            if len(args) >= 4:
                if args[3] == "1":
                    func = combine_img_vertical
            picBase64Buf = func(left, right)
            action.sendGroupPic(ctx.FromGroupId, picBase64Buf=picBase64Buf,
                                content="OK!!!!", atUser=ctx.FromUserId)
        else:
            action.sendGroupText(ctx.FromGroupId, "至少发两个词语!!!!!!!")
# WIKI------------------------------------------
    if strCont.startswith("找梗 ") or strCont.startswith("百度一下 ") or strCont.startswith("梗 "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            jikidata = jkjk.check(args[1])
            if jikidata["error"] == 0:
                action.sendGroupText(
                    ctx.FromGroupId, "\n"+jikidata["title"]+"\n"+jikidata["res"], ctx.FromUserId)
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "\n"+"查询错误 ERROR 机器人即将爆炸!!!!!!!!!!!!", ctx.FromUserId)
# QR CODE------------------------------
    if strCont.startswith("二维码制作 ") or strCont.startswith("qr "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            index = random.randint(1, 40)
            strWords = args[1]
            if is_contain_chinese(strWords):
                action.sendGroupText(
                    ctx.FromGroupId, "\n"+"不能包含中文!!!!!!!!!!!!", ctx.FromUserId)
            else:
                #strWord2 = to_unicode(strWords)
                try:
                    myqr.run(words=strWords, colorized=True,
                             save_name="./QQRR.png")
                    with open('./QQRR.png', 'rb') as f:  # 以二进制读取图片
                        data = f.read()
                        encodestr = base64.b64encode(
                            data).decode()  # 得到 byte 编码的数据
                        action.sendGroupPic(
                            ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)

                except:
                    print("二维码制作 Error")


# 摩斯 CODE------------------------------
    if strCont.startswith("摩斯码 ") or strCont.startswith("ms "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strWords = args[1]
            if not is_contain_chinese(strWords):
                try:
                    mainMorse(strWords, ctx.FromGroupId)
                except:
                    print("摩斯码 Error")
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "\n"+"不能包含中文!!!!!!!!!!!!", ctx.FromUserId)


# 加密通话 ------------------------------
    if strCont.startswith("解密 ") or strCont.startswith("解谜 ") or strCont.startswith("翻译翻译 "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strWords = args[1]
            try:
                strR = jiemi(strWords)
                action.sendGroupText(ctx.FromGroupId, strR, ctx.FromUserId)
            except:
                action.sendGroupText(
                    ctx.FromGroupId, "解密 Error", ctx.FromUserId)
        else:
            action.sendGroupText(ctx.FromGroupId, "\n" +
                                 "输入错误!!!!!!!!!!!!", ctx.FromUserId)

# 买家秀 ------------------------------
    if strCont.find("买家秀") > -1:
        if CheckCoins(strSendQQID, 10, ctx.FromGroupId) == False:
            return 1

        indexInt = random.randint(1, 6)
        taobaoUrl = "https://api.uomg.com/api/rand.img3"
        if indexInt == 1:
            taobaoUrl = "https://api.ghser.com/tao"
        elif indexInt == 2:
            taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=胖次猫"
        else:
            taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=七了个三"
        action.sendGroupPic(ctx.FromGroupId, picUrl=taobaoUrl,
                            content="OK!!!!", atUser=ctx.FromUserId)


# 幻影坦克 ------------------------------
    if strCont == "幻影坦克":
        if CheckCoins(strSendQQID, 10, ctx.FromGroupId) == False:
            return 1

        taobaoUrl = getYubanPic("")
        # taobaoUrl2 = getYubanPic("")
        SavePic(taobaoUrl)
        # SavePic2222(taobaoUrl2)
        f1 = 'test.jpg'  # 上层
        f2 = 'MJX.png'  # 下层
        savePath = r'T12123123.png'  # 保存路径
        base64_str = mkTKPic(f1, f2, savePath)
        action.sendGroupPic(ctx.FromGroupId, picBase64Buf=base64_str,
                                 content="OK!!!!", atUser=ctx.FromUserId)
    if strCont == "r18幻影坦克":
        if CheckCoins(strSendQQID, 20, ctx.FromGroupId) == False:
            return 1
        taobaoUrl = getYubanPic("", 1)
        SavePic(taobaoUrl)
        f1 = 'test.jpg'  # 上层
        f2 = 'MJX.png'  # 下层
        savePath = r'T12123123.png'  # 保存路径
        base64_str = mkTKPic(f1, f2, savePath)
        action.sendGroupPic(ctx.FromGroupId, picBase64Buf=base64_str,
                                 content="OK!!!!", atUser=ctx.FromUserId)

# 讲个笑话 ------------------------------
    if strCont.find("讲个笑话") > -1:
        urlll = "https://api.ghser.com/xiaohua"
        res = requests.get(urlll)
        # print("===>"+res.text)
        action.sendGroupText(ctx.FromGroupId, res.text)

# 狗屁不通 ------------------------------
    if strCont.find("狗屁不通") > -1:
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strWords = args[1]
            aaa = GPBT(strWords)
            action.sendGroupText(ctx.FromGroupId, aaa)

    if strCont == "开始流浪":
        if bGameStarted == False:
            bGameStarted = True
            mainLiuLang(ctx)
        else:
            action.sendGroupText(ctx.FromGroupId, "游戏正在进行中, 不能多开")
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
                        action.sendGroupText(ctx.FromGroupId, strRef)
                except:
                    action.sendGroupText(
                        ctx.FromGroupId, "输入数字错误! 比如回复 继续游戏 1")
            else:
                action.sendGroupText(ctx.FromGroupId, "输入多了!! 比如回复 继续游戏 1")
        else:
            action.sendGroupText(ctx.FromGroupId, "游戏未开始, 请回复 开始流浪")
    elif strCont == "结束游戏" and bGameStarted == True:
        bGameStarted = False
        action_stack = [[]]
        status = {
            "Money": 5,
            "HP": 100,
            "Debt": 50000,
            "Message": "",
            "ContinueWorkTime": 0
        }

        action.sendGroupText(ctx.FromGroupId, "游戏关闭")

    if strCont == "开始扫雷":
        if bSaoLeiStart == False:
            bSaoLeiStart = True
            mt = MineTable()
            strShow = mt.printShow()
            strShow += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + \
                str(mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
            action.sendGroupText(ctx.FromGroupId, strShow)
        else:
            strShow = "游戏正在进行中, 不能多开\n"
            if mt != 0:
                strShow += mt.printShow()
                strShow += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(
                    mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
            action.sendGroupText(ctx.FromGroupId, strShow)
    if strCont.startswith("继续扫雷"):
        if bSaoLeiStart == True:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 2:
                line_input = args[1]
                line_input = line_input.replace("，", ",")
                try:
                    # 用户继续输入, 先判断输入格式
                    if not (re.match(r'^\d+,\d+', line_input)):
                        action.sendGroupText(
                            ctx.FromGroupId, "输入错了!! 比如回复 继续扫雷 1,2")
                    else:
                        strResult = ""
                        line, field = eval(line_input)
                        # 打开用户指定的表格位置
                        result = mt.checkInputAddress(line, field)
                        if result == -1:
                            strResult = ('地址错误')
                        elif result == 0:
                            strResult = ('这里已经打开了,请选别的点')
                        elif result == 2:
                            bSaoLeiStart = False
                            strResult = ('---!!!炸了,你输了!!!---\n')
                            mt.gameOverMine()
                            for item in mt.resultTable:
                                strResult += (str(item) + '\n')
                        else:
                            strResult = mt.printShow()
                            strResult += '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(
                                mt.getLastGood()) + ' \n(继续游戏输入:"继续扫雷 x,y"/退出:"gg"): '
                        action.sendGroupText(ctx.FromGroupId, strResult)
                except Exception as error:
                    print("输入数字错误输入数字错误" + str(error))
                    action.sendGroupText(
                        ctx.FromGroupId, "输入数字错误! 比如回复 继续扫雷 1,2")
            else:
                action.sendGroupText(ctx.FromGroupId, "输入错了!! 比如回复 继续扫雷 1,2")
        else:
            action.sendGroupText(ctx.FromGroupId, "游戏未开始, 请回复 开始扫雷")
    if strCont == "gg":
        bSaoLeiStart = False
        action.sendGroupText(ctx.FromGroupId, "扫雷关闭")

    if strCont.startswith("来张美图") or strCont.startswith("来张色图") or strCont.startswith("来张图"):
        #print("????????????" + strCont)#
        bbbst = False
        try:
            bbbst = dataSetuGroupData[strGID]
        except:
            bbbst = False
        if bbbst == False:
            action.sendGroupText(
                ctx.FromGroupId, "图片关掉了, 请联系主人, 找不到就算了", ctx.FromUserId)
            return 1

        if CheckCoins(strSendQQID, 10, ctx.FromGroupId) == False:
            return 1

        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        aaa = 0
        if len(args) == 1:
            aaa = getYubanPic("")
        elif len(args) == 2:
            aaa = getYubanPic(args[1], "0")
        elif len(args) == 3:
            aaa = getYubanPic(args[1], args[2])

        if aaa[0] != "h":
            action.sendGroupText(ctx.FromGroupId, "出错了==>"+aaa)
        else:
            SavePic(aaa)
            with open('./MJX.png', 'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data).decode()  # 得到 byte 编码的数据
                action.sendGroupPic(
                    ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)


@bot.on_group_msg
@deco.ignore_botself
@deco.these_msgtypes('AtMsg')
def receive_AT_group_msg(ctx: GroupMsg):
    global dataSetuGroupData
    global bBotClose
    global bMasterQQ
    global botQQ
    global lastBotMsg
    global blackList
    if blackList[0] == ctx.FromGroupId:
        return 1
    objCtx = json.loads(ctx.Content)
    strCont = objCtx['Content']
    atUserID = objCtx['UserID'][0]
    strGID = str(ctx.FromGroupId)
    sendUid = ctx.FromUserId
    strSendQQID = str(ctx.FromUserId)
    nGroupID = ctx.FromGroupId
    if bBotClose:
        return 1

    # print("......" + str(ctx))

    # print("#asdasda==" + str(strCont.find("菜单")))
    if strCont.find("骂") > -1 and atUserID != botQQ and atUserID != bMasterQQ:

        action.sendGroupText(ctx.FromGroupId, "骂人不好, 还是摸摸他吧..发送 头像表情包 可以获取帮助")
        return 1

        admList = action.getGroupAdminList(ctx.FromGroupId, True)
        # print("admListadmListadmList===> "+str(admList))
        qzQQ = admList[0]["MemberUin"]
        if qzQQ == atUserID:
            action.sendGroupText(ctx.FromGroupId, "群主有免骂权, 不服的建议推翻群主统治")
            return 1
        if bBotClose:
            action.sendGroupText(ctx.FromGroupId, "已关机")
            return 1
        # urlMMM = "https://fun.886.be/api.php?lang=zh_cn"
        # html = requests.get(urlMMM)
        # strConnn = str(html.text)
        if CheckCoins(strSendQQID, 3, ctx.FromGroupId) == False:
            return 1
        strConnn = GetMrStr()
        action.sendGroupText(
            ctx.FromGroupId, content=strConnn, atUser=atUserID)
        vocccPath12 = text_to_speech(strConnn)
        if len(vocccPath12) > 0:
            action.sendGroupVoice(
                ctx.FromGroupId, voiceBase64Buf=file_to_base64(vocccPath12))


    # if strCont.find("抢劫") > -1 and atUserID != botQQ and atUserID != bMasterQQ:
    nTime = int(time.time())
    nLastActionTime = 0
    # nCDTIme = 60*60*2
    nCDTIme = 60*3
    if strCont.find("抢劫") > -1:
        stratUserID = str(atUserID)
        enemyCOins = 0
        myCOins = 0
        try:
            enemyCOins = elsGameData[stratUserID]["coins"]
        except:
            elsGameData[stratUserID] = {}
            elsGameData[stratUserID]["coins"]  = 0
            elsGameData[stratUserID]["signTime"]  = 0
            elsGameData[stratUserID]["nLastActionTime"]  = 0
            enemyCOins = 0

        try:
            nLastActionTime = elsGameData[strSendQQID]["nLastActionTime"]
        except:
            elsGameData[strSendQQID]["nLastActionTime"]  = 0
        try:
            myCOins = elsGameData[strSendQQID]["coins"]
        except:
            elsGameData[strSendQQID] = {}
            elsGameData[strSendQQID]["coins"]  = 0
            elsGameData[strSendQQID]["signTime"]  = 0
            myCOins = 0

        if nTime - nLastActionTime <= nCDTIme:
            action.sendGroupText(ctx.FromGroupId, "每"+str(nCDTIme)+"秒才能行动一次, 你还剩"+ str(nCDTIme - (nTime - nLastActionTime))+"秒才能行动", atUser=ctx.FromUserId)
            return 1
        
        if myCOins <= 10:
            action.sendGroupText(ctx.FromGroupId, "收手吧, 你只剩"+str(myCOins)+"金币了, 没钱了", atUser=ctx.FromUserId)
            return 1

        if myCOins > enemyCOins:
            halfC = int(myCOins / 2)
            if halfC > 10:
                halfC = 10
            if halfC <= 0:
                halfC = 0
            elsGameData[strSendQQID]["coins"] -= halfC
            elsGameData[stratUserID]["coins"] += halfC
            action.sendGroupText(ctx.FromGroupId, "用户"+stratUserID+"的钱都没你"+ strSendQQID +"的多, 还抢个JB, 已经分了你的"+str(halfC)+"个金币给他了!")
        else:
            enemyRan = random.randint(1, enemyCOins)
            myRan = random.randint(1, myCOins)
            if enemyRan >= myRan:
                halfC = int(myCOins / 2)
                if halfC <= 0:
                    halfC = 0
                if halfC <= 0:
                    halfC = 0
                elsGameData[strSendQQID]["coins"] -= halfC
                elsGameData[stratUserID]["coins"] += halfC
                action.sendGroupText(ctx.FromGroupId, "用户"+stratUserID+"战斗力为"+str(enemyCOins)
                    +"\n你"+ strSendQQID +"的战斗力为"+str(myCOins)+"\n一番激战后你失败了,输了"+str(halfC)+"个金币给他")
            else:
                halfC = int(enemyCOins / 2)
                if halfC <= 0:
                    halfC = 0
                elsGameData[strSendQQID]["coins"] += halfC
                elsGameData[stratUserID]["coins"] -= halfC
                action.sendGroupText(ctx.FromGroupId, "用户"+stratUserID+"战斗力为"+str(enemyCOins)
                    +"\n你"+ strSendQQID +"的战斗力为"+str(myCOins)+"\n一番激战后你赢了,抢到了"+str(halfC)+"个金币")

        elsGameData[strSendQQID]["nLastActionTime"] = nTime
        SaveElsGameData()

    if strCont.find("决斗") > -1:
        stratUserID = str(atUserID)
        enemyCOins = 0
        myCOins = 0
        try:
            enemyCOins = elsGameData[stratUserID]["coins"]
        except:
            elsGameData[stratUserID] = {}
            elsGameData[stratUserID]["coins"]  = 0
            elsGameData[stratUserID]["signTime"]  = 0
            elsGameData[stratUserID]["nLastActionTime"]  = 0
            enemyCOins = 0

        try:
            nLastActionTime = elsGameData[strSendQQID]["nLastActionTime"]
        except:
            elsGameData[strSendQQID]["nLastActionTime"]  = 0

        try:
            myCOins = elsGameData[strSendQQID]["coins"]
        except:
            elsGameData[strSendQQID] = {}
            elsGameData[strSendQQID]["coins"]  = 0
            elsGameData[strSendQQID]["signTime"]  = 0
            myCOins = 0

        if nTime - nLastActionTime <= nCDTIme:
            action.sendGroupText(ctx.FromGroupId, "每"+str(nCDTIme)+"秒才能行动一次, 你还剩"+ str(nCDTIme - (nTime - nLastActionTime))+"秒才能行动", atUser=ctx.FromUserId)
            return 1

        if myCOins <= 0:
            action.sendGroupText(ctx.FromGroupId, "没钱谁和你赌!!!, 你只剩"+str(myCOins)+"金币了, 没钱了", atUser=ctx.FromUserId)
            return 1

        if enemyCOins <= 0:
            action.sendGroupText(ctx.FromGroupId, "这人没钱,和他赌不值得", atUser=ctx.FromUserId)
            return 1
        
        strRes12 = "决斗开始,本决斗为俄罗斯转盘,6发子弹射自己,看谁先死,因为是你("+strSendQQID+")发起的,所以你先开枪\n\n"
        shootNum = random.randint(0, 5)
        for ii in range(6):
            if ii % 2 == 0:
                if shootNum == ii:
                    strRes12 += "第"+str(ii+1)+"枪, PONG!!!!! 你杀了自己!!!!输了!!!\n"
                    break
                else:
                    strRes12 += "第"+str(ii+1)+"枪, 枪没响,到对方了\n"
            else:
                if shootNum == ii:
                    strRes12 += "第"+str(ii+1)+"枪, PONG!!!!! 对方枪响了!!!!你赢了!!!!\n"
                    break
                else:
                    strRes12 += "第"+str(ii+1)+"枪, 对方枪没响,到你了\n"


        #自己输了
        if shootNum%2 == 0:
            if myCOins >= enemyCOins:
                strRes12 += "\n因为对方("+stratUserID+")只有"+str(enemyCOins)+"个金币, 所以他只赢了"+str(enemyCOins)+"金币!\n而你主动决斗失败,失去所有金币"
                elsGameData[stratUserID]["coins"] += enemyCOins
                elsGameData[strSendQQID]["coins"] -= myCOins
            else:
                strRes12 += "\n你输掉了所有的"+str(myCOins)+"金币!"
                elsGameData[stratUserID]["coins"] += myCOins
                elsGameData[strSendQQID]["coins"] -= myCOins
        #自己赢了
        else:
            if myCOins >= enemyCOins:
                strRes12 += "\n恭喜你赢了对方("+stratUserID+")所有金币"+str(enemyCOins)+"个!"
                elsGameData[strSendQQID]["coins"] += enemyCOins
                elsGameData[stratUserID]["coins"] -= enemyCOins
            else:
                strRes12 += "\n因为你只有"+str(myCOins)+"个金币, 所以你赢了"+str(myCOins)+"金币!"
                elsGameData[strSendQQID]["coins"] += myCOins
                elsGameData[stratUserID]["coins"] -= myCOins

        action.sendGroupText(ctx.FromGroupId, strRes12)
        elsGameData[strSendQQID]["nLastActionTime"] = nTime
        SaveElsGameData()
        return

    if strCont.find("偷钱") > -1:
        stratUserID = str(atUserID)
        enemyCOins = 0
        myCOins = 0
        myStealNum = 0

        try:
            enemyCOins = elsGameData[stratUserID]["coins"]
        except:
            elsGameData[stratUserID] = {}
            elsGameData[stratUserID]["coins"]  = 0
            elsGameData[stratUserID]["signTime"]  = 0
            elsGameData[stratUserID]["nLastActionTime"]  = 0
            enemyCOins = 0

        try:
            nLastActionTime = elsGameData[strSendQQID]["nLastActionTime"]
        except:
            elsGameData[strSendQQID]["nLastActionTime"]  = 0
        try:
            myCOins = elsGameData[strSendQQID]["coins"]
            myStealNum = elsGameData[strSendQQID]["steal"]
        except:
            elsGameData[strSendQQID] = {}
            elsGameData[strSendQQID]["coins"]  = 0
            elsGameData[strSendQQID]["signTime"]  = 0
            myStealNum = 0
            myCOins = 0


        if nTime - nLastActionTime <= nCDTIme:
            action.sendGroupText(ctx.FromGroupId, "每"+str(nCDTIme)+"秒才能行动一次, 你还剩"+ str(nCDTIme - (nTime - nLastActionTime))+"秒才能行动", atUser=ctx.FromUserId)
            return 1

        if myStealNum >= 10:
            action.sendGroupText(ctx.FromGroupId, "造孽太多偷了别人10次, 收手, 放自己一马", atUser=ctx.FromUserId)
            return 1
        if enemyCOins <= 100:
            action.sendGroupText(ctx.FromGroupId, "他就"+str(enemyCOins)+"个金币, 穷逼一个, 放他一马", atUser=ctx.FromUserId)
            return 1
        nStealcoinsNum = 0
        nRandomNum = random.randint(0, 1000)
        strRSRSR ="80%机会偷1%的钱,\n10%的机会偷2%的钱, \n8%会被发现并赔偿自己所有的钱,\n1%的机会偷4%的钱, \n0.5%的机会偷5%的钱, \n0.3%的机会偷6%, \n0.1%机会偷7%, \n0.1%机会偷50%\n一辈子只能偷10次\n\n"

        floatPercent = 0
        if nRandomNum <= 800 : #80%机会抢1%
            floatPercent = 0.01
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum <= 900:#10%的机会偷2%的钱
            floatPercent = 0.02
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum <= 980:#8%的机会被发现赔偿自己所有的钱
            floatPercent = 0.03
            nStealcoinsNum = -myCOins #int(enemyCOins * floatPercent)
        elif nRandomNum <= 990:#1%的机会偷4%的钱
            floatPercent = 0.04
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum <= 995:#0.5%的机会偷5%的钱
            floatPercent = 0.05
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum <= 998:#0.3%的机会偷6%的钱
            floatPercent = 0.06
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum <= 999:#0.3%的机会偷7%的钱
            floatPercent = 0.07
            nStealcoinsNum = int(enemyCOins * floatPercent)
        elif nRandomNum == 1000:#0.3%的机会偷7%的钱
            floatPercent = 0.5
            nStealcoinsNum = int(enemyCOins * floatPercent)
        
        myStealNum += 1
        elsGameData[strSendQQID]["steal"] = myStealNum
        if floatPercent == 0.03:
            strRSRSR += "你开始偷偷接近他, 伸手, 糟了, 被发现了, 你被打了一顿,赔偿了身上所有的钱("+str(myCOins)+"个金币)给对方"
        elif floatPercent < 0.5:
            strRSRSR += "本次行动运气不好,也就偷了"+str(nStealcoinsNum)+"个金币, 占比"+str(floatPercent)+",还剩"+str(10 - myStealNum)+"次机会"
        else:
            strRSRSR += "卧槽!!!!你运气爆表偷了他一半金币,共"+str(nStealcoinsNum)+"个,还剩"+str(10 - myStealNum)+"次机会"


        elsGameData[strSendQQID]["coins"] += nStealcoinsNum
        elsGameData[stratUserID]["coins"] -= nStealcoinsNum
        elsGameData[strSendQQID]["nLastActionTime"] = nTime
        SaveElsGameData()
        action.sendGroupText(ctx.FromGroupId, strRSRSR, atUser=ctx.FromUserId)
        return 1
        
    if sendUid == bMasterQQ:
        if strCont.find("发金币") > -1:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            allLength = len(args)
            addCoins = 0
            strQQ = str(atUserID)
            try:
                addCoins = int(args[allLength - 1])
            except:
                action.sendGroupText(ctx.FromGroupId, "格式错误", atUser=sendUid)
                return 1

            try:
                elsGameData[strQQ]["coins"] += addCoins
            except:
                elsGameData[strQQ] = {}
                elsGameData[strQQ]["coins"] = addCoins
                elsGameData[strQQ]["signTime"] = 0
            SaveElsGameData()
            action.sendGroupText(ctx.FromGroupId, "管理员发金币成功, 你还剩"+str(elsGameData[strQQ]["coins"])+"个金币", atUser=atUserID)


    if(atUserID == botQQ):
        if sendUid == bMasterQQ:
            if strCont.find("撤回") > -1:
                if(lastBotMsg and len(lastBotMsg) > 0):
                    lastCtx = lastBotMsg.pop()
                    action.revoke(lastCtx)
                    return
                else:
                    action.sendGroupText(ctx.FromGroupId, "没有消息列表!!!!!!!")
                    return
            if strCont.find("添加白名单") > -1:
                wilteList.append(nGroupID)
                for x in wilteList:
                    strID = str(x)
                    dataCiliGroupData[strID] = True
                    dataSetuGroupData[strID] = True
                    dataNudeGroupData[strID] = True
                action.sendGroupText(ctx.FromGroupId, "添加成功, " + strGID)
                return
            if strCont.find("添加黑名单") > -1:
                dataCiliGroupData[strGID] = False
                dataSetuGroupData[strGID] = False
                dataNudeGroupData[strGID] = False
                action.sendGroupText(ctx.FromGroupId, "添加成功, " + strGID)
                return

        if bBotClose:
            action.sendGroupText(ctx.FromGroupId, "已关机")
            return 1

        if strCont.find("贷款") > -1:

            aaaINS = False

            if dkDataArr and len(dkDataArr) > 0:
                for dd in dkDataArr:
                    if dd["dUid"] == sendUid:
                        aaaINS = True
                        break


            if aaaINS == True:
                action.sendGroupText(ctx.FromGroupId, "你有贷款在身, 等死吧!!!!!别再贷了!!!!", atUser=sendUid)
                return 1

            dtime = int(time.time())
            dkD = {"dUid":sendUid, "dTime":dtime, "dGid":nGroupID}
            dkDataArr.append(dkD)

            try:
                elsGameData[strSendQQID]["coins"] += 10000
            except:
                elsGameData[strSendQQID] = {}
                elsGameData[strSendQQID]["coins"] = 10000
                elsGameData[strSendQQID]["signTime"] = 0

            SaveDKData()
            action.sendGroupText(ctx.FromGroupId, "你贷款10000块成功, 10分钟后强制收回贷款和利息", atUser=sendUid)
            return 1

        if strCont.find("菜单") > -1 or strCont.find("帮助") > -1:

            struuuu = '''
            发送[买家秀], 则回复好看的买家秀图=\n
            发送[磁力搜 搜索内容],则回复磁力链接=\n
            发送[开始流浪],则开始玩流浪汉文字游戏=\n
            发送[开始扫雷],则开始玩扫雷游戏=\n
            发送[狗屁不通 关键词],回复由关键词生成的狗屁不通文章=\n
            发送[讲个笑话],回复一个笑话=\n
            发送[幻影坦克],回复买家秀生成的幻影坦克图片=\n
            发送[制作幻影坦克 加两个图片],回复指定两个图片生成的幻影坦克图片=\n
            发送[做图 内容1 内容2],回复por...hub风格的logo=\n
            发送[百度一下 内容],回复该内容的网络信息=\n
            发送[来张图 搜索内容],回复该内容的二次元图=\n
            发送[翻译翻译 拼音缩写],就能让机器翻译内容 比如 翻译翻译 yyds, 翻译永远滴神\n
            发送[小说续写 开头内容],就能让机器续写之后的内容, 比如 小说续写 群主挂了之后\n
            发送[颜值检测 加图片],就能让机器人检测颜值\n
            发送[系统信息],查看机器人运行状态\n
            发送[获取管理员],查看本群管理员列表\n
            发送[扔漂流瓶 加内容],\n
            发送[获取漂流瓶],\n
            ==>只有以下两个功能需要@机器人,别的功能别自作主张@它=\n
            @机器人  可以和机器人对话=\n
            @机器人后回复 说说+内容,就能让机器人读出内容 比如@jj-姬器人 说说 你是傻逼=\n
            @机器人后回复 贷款\n

            =>怎么添加机器人到自己的群:\n
            =>1:加机器人好友, 2:邀请它入群, 3:使用\n

            '''
            struuuu += "\n" +bot.plugMgr.help+"\n\n"

            if sendUid == bMasterQQ:
                struuuu += "@机器人加 撤回 添加白名单 添加黑名单 \n"
                struuuu += "群发金币 全群通知\n"
                struuuu += "私聊 群消息 私聊 关机 开机 重启 群列表\n\n"

            struuuu += "发送 机器人签到 可以获取金币\n\n"
            struuuu += "发送 查询金币 可以查询金币\n\n"
            struuuu += "发送 赠送金币 QQ号 金币数  可以转账\n\n"
            struuuu += "买家秀, 续写小说, 幻影坦克, 骂人, 机器人说说+内容 这些功能需要金币\n\n"

            struuuu += "@一个人并发送 抢劫, 可抢劫他的金币\n"
            struuuu += "@一个人并发送 决斗, 运行俄罗斯转盘游戏和他赌运气, 输了金币要清零, 赢了金币最高能翻倍\n"

            action.sendGroupText(ctx.FromGroupId, struuuu)
        # 模特 ------------------------------
        elif strCont.find("来张美图") > -1 or strCont.find("来张色图") > -1 or strCont.find("来张图") > -1:
            bbbstat = False
            try:
                bbbstat = dataSetuGroupData[strGID]
            except:
                bbbstat = False
            if bbbstat == False:
                action.sendGroupText(
                    ctx.FromGroupId, "AT图片关掉了, 请联系主人, 找不到就算了", ctx.FromUserId)
                return 1

            if CheckCoins(strSendQQID, 10, ctx.FromGroupId) == False:
                return 1
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            aaa = 0
            if len(args) == 1 or len(args) == 2:
                aaa = getYubanPic("")
            elif len(args) == 3:
                aaa = getYubanPic(args[2], "0")
            elif len(args) == 4:
                aaa = getYubanPic(args[2], args[3])

            if aaa[0] != "h":
                action.sendGroupText(ctx.FromGroupId, "出错了==>"+aaa)
            else:
                SavePic(aaa)
                with open('./MJX.png', 'rb') as f:  # 以二进制读取图片
                    data = f.read()
                    encodestr = base64.b64encode(
                        data).decode()  # 得到 byte 编码的数据
                    action.sendGroupPic(
                        ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)

        elif strCont.find("隐藏功能") > -1:
            struuuu = '''
                        发送[脱衣 加一个图片],回复指定图片生成的AI脱衣图片(deepnude源码)\n
                        发送[来张图 搜索内容 r18开关(0普通, 1r18, 2随机)],比如[来张图 jk 1]=>回复jk的二次元r18图\n
                        发送[r18幻影坦克]\n
                        '''
            action.sendGroupText(ctx.FromGroupId, struuuu, ctx.FromUserId)
        elif strCont.find("买家秀") > -1:
            if CheckCoins(strSendQQID, 10, ctx.FromGroupId) == False:
                return 1
            indexInt = random.randint(1, 6)
            taobaoUrl = "https://api.uomg.com/api/rand.img3"
            if indexInt == 1:
                taobaoUrl = "https://api.ghser.com/tao"
            elif indexInt == 2:
                taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=胖次猫"
            else:
                taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=七了个三"
            action.sendGroupPic(ctx.FromGroupId, picUrl=taobaoUrl,
                                content="OK!!!!", atUser=ctx.FromUserId)

        elif strCont.find("加密") > -1 or strCont.find("和谐") > -1:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 3:
                str111 = encoder(args[2])
                action.sendGroupText(ctx.FromGroupId, "" + str111)
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        elif strCont.find("还原") > -1:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 3:
                str1112 = decoder(args[2])
                action.sendGroupText(ctx.FromGroupId, "还原为:\n" + str1112)
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        elif strCont.find("解密") > -1 or strCont.find("翻译翻译") > -1:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 3:
                str222 = jiemi(args[2])
                action.sendGroupText(ctx.FromGroupId, str222)
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        elif strCont.find("说说") > -1 or strCont.find("喊一声") > -1 or strCont.find("说一声") > -1:
            if CheckCoins(strSendQQID, 2, ctx.FromGroupId) == False:
                return 1
            # print("strCont===>"+strCont)
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            strHead = args[0]
            if len(args) >= 3:
                strHead2 = args[1]
                strSsss = strCont.replace(strHead, "")
                strSsss = strSsss.replace(strHead2, "")
                vocccPath = text_to_speech(strSsss)
                if len(vocccPath) > 0:
                    action.sendGroupVoice(
                        ctx.FromGroupId, voiceBase64Buf=file_to_base64(vocccPath))
            elif len(args) == 2:
                vocccPath = text_to_speech(args[1])
                if len(vocccPath) > 0:
                    action.sendGroupVoice(
                        ctx.FromGroupId, voiceBase64Buf=file_to_base64(vocccPath))
            else:
                action.sendGroupText(
                    ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        else:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            text = "ERROR!!! "
            if len(args) == 2:
                text = chatAI(args[1])
                try:
                    vocccPath = text_to_speech(text)
                    if len(vocccPath) > 0:
                        action.sendGroupVoice(
                            ctx.FromGroupId, voiceBase64Buf=file_to_base64(vocccPath))
                except:
                    action.sendGroupText(
                        ctx.FromGroupId, "语音失败,发送文字:"+text, ctx.FromUserId)


@bot.on_group_msg
@deco.ignore_botself
@deco.these_msgtypes('PicMsg')
def receive_PIC_group_msg(ctx: GroupMsg):

    global nAAAAAAAA
    global nBBBBBB
    global bBotClose
    global dataNudeGroupData
    global blackList
    if blackList[0] == ctx.FromGroupId:
        return 1
    strGID = str(ctx.FromGroupId)
    strSendQQID = str(ctx.FromUserId)
    if bBotClose:
        # action.sendGroupText(ctx.FromGroupId, "已关机")
        return 1

    objCtx = json.loads(ctx.Content)
    strCont = ""
    picArr = []
    try:
        strCont = objCtx['Content']
        picArr = objCtx['GroupPic']
    except:
        strCont = ""

    nIndex = 1
    if strCont.find("幻影坦克") > -1 and len(picArr) == 2:
        if CheckCoins(strSendQQID, 15, ctx.FromGroupId) == False:
            return 1

        for i in picArr:
            strUrlqq = i["Url"]
            html = requests.get(strUrlqq)
            if nIndex == 1:
                nIndex = 2
                with open('./11.png', 'wb') as file:
                    file.write(html.content)
            else:
                with open('./2.png', 'wb') as file:
                    file.write(html.content)

        f1 = '11.png'  # 上层
        f2 = '2.png'  # 下层
        savePath = r'T1.png'  # 保存路径
        try:
            base64_str = make(f1, f2, savePath)
            action.sendGroupPic(ctx.FromGroupId, picBase64Buf=base64_str,
                                content="OK!!!!", atUser=ctx.FromUserId)
        except:
            action.sendGroupText(ctx.FromGroupId, "\n" +
                                 "合成错误，抱歉!!!!!!!!!!!!", ctx.FromUserId)

    # elif strCont.startswith("333444111脱衣") and len(picArr) == 1:
    #     nAAAAAAAA = nAAAAAAAA + 1
    #     if strCont == "脱衣":
    #         strUrlqq = picArr[0]["Url"]
    #         html = requests.get(strUrlqq)
    #         with open('./222111/' + str(nAAAAAAAA) + '.png', 'wb') as file:
    #             file.write(html.content)
    #         strADB = "./dreampower run --input 222111/" + str(nAAAAAAAA) + ".png --output 222111/" + str(
    #             nAAAAAAAA) + "ot.png --cpu --n-cores 4 --experimental-color-transfer --auto-resize --nsize 1 --bsize 1.6 --hsize 1 --vsize 1"
    #         os.system(strADB)
    #         print(time.strftime("FINISH!!!!!!!!! %Y-%m-%d %H:%M:%S", time.localtime()))
    #         with open("./222111/" + str(nAAAAAAAA) + "ot.png", 'rb') as f:  # 以二进制读取图片
    #             data = f.read()
    #             encodestr = base64.b64encode(data).decode()  # 得到 byte 编码的数据
    #             action.sendGroupPic(
    #                 ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)
    #     else:
    #         args = [i.strip() for i in strCont.split(" ") if i.strip()]
    #         #print("assssssssssssdasd" + str(len(args)))
    #         if len(args) == 7:
    #             strTypeaa = " --auto-resize "
    #             if args[1] == "2":
    #                 strTypeaa = " --auto-resize-crop "
    #             elif args[1] == "3":
    #                 strTypeaa = " --auto-rescale "
    #             strAAAA = " --experimental-color-transfer "
    #             if args[6] == "0":
    #                 strAAAA = " "
    #             strUrlqq = picArr[0]["Url"]
    #             html = requests.get(strUrlqq)
    #             with open('./11/' + str(nAAAAAAAA) + '.png', 'wb') as file:
    #                 file.write(html.content)
    #             strADB = "./dreampower run --input 11/" + str(nAAAAAAAA) + ".png --output 11/" + str(nAAAAAAAA) + "ot.png --cpu --n-cores 4 " + \
    #                 strTypeaa + strAAAA + "--bsize " + \
    #                 args[2] + "  --nsize " + args[3] + \
    #                 " --vsize " + args[4] + " --hsize " + args[5]
    #             os.system(strADB)
    #             print(time.strftime(
    #                 "FINISH!!!!!!!!! %Y-%m-%d %H:%M:%S", time.localtime()))
    #             with open("./11/" + str(nAAAAAAAA) + "ot.png", 'rb') as f:  # 以二进制读取图片
    #                 data = f.read()
    #                 encodestr = base64.b64encode(
    #                     data).decode()  # 得到 byte 编码的数据
    #                 action.sendGroupPic(
    #                     ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)
    #         else:
    #             action.sendGroupText(
    #                 ctx.FromGroupId, "参数少了!需要: 脱衣 图片缩放类型 Boob大小 Ru头大小 Vagina大小 yin毛大小 是否使用原图颜色 \n 比如: 脱衣 1 1.5 1 1 0.9 1", ctx.FromUserId)

    elif strCont.startswith("脱衣") and len(picArr) == 1:
        bbbty = False
        try:
            bbbty = dataNudeGroupData[strGID]
        except:
            bbbty = False
        if bbbty == False:
            action.sendGroupText(ctx.FromGroupId, "无功能")
            return 1

        if CheckCoins(strSendQQID, 1000, ctx.FromGroupId) == False:
            return 1
        nAAAAAAAA = nAAAAAAAA + 1
        strUrlqq = picArr[0]["Url"]
        html = requests.get(strUrlqq)
        with open('./' + str(nAAAAAAAA) + '.png', 'wb') as file:
            file.write(html.content)

            strADB = "python3 main.py -i " + \
                str(nAAAAAAAA) + '.png -o output_' + str(nAAAAAAAA) + '.png'
            os.system(strADB)

            with open("./output_" + str(nAAAAAAAA) + ".png", 'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data).decode()  # 得到 byte 编码的数据
                action.sendGroupPic(
                    ctx.FromGroupId, picBase64Buf=encodestr, content="OK!!!!", atUser=ctx.FromUserId)

    elif strCont.startswith("颜值") and len(picArr) == 1:
        strUrlqqYY = picArr[0]["Url"]
        SavePic2222(strUrlqqYY)
        img = Image.open("./MJX2.png").convert("RGB")
        img.save("./MJX211.jpg", format='JPEG')
        with open('./MJX211.jpg', 'rb') as f:  # 以二进制读取图片
            data = f.read()
            strB64 = base64.b64encode(data).decode()  # 得到 byte 编码的数据
            strresrsrs = CheckYYYY(strB64)
            action.sendGroupText(ctx.FromGroupId, strresrsrs, ctx.FromUserId)


@bot.on_event
def REV_EVENT_MSG(ctx: EventMsg):
    global bMasterQQ
    # a = 12
    if ctx.EventMsg and ctx.EventMsg["Content"] != "群成员退出群聊事件" and ctx.EventMsg["Content"] != "某人进群事件" and ctx.EventMsg["Content"] != "群成员撤回消息事件" and ctx.EventMsg["Content"] != "好友事件状态(被同意添加好友/被拒绝添加好友)":
        aaa = "事件消息===>" + str(ctx.EventData)+" "+  str(ctx.EventMsg)
        action.sendFriendText(bMasterQQ, aaa)

@bot.on_friend_msg
@deco.ignore_botself
def REV_FRD_MSG(ctx: FriendMsg):
    global bBotClose
    global bMasterQQ
    
    nSendID = ctx.FromUin
    strConFrd = ctx.Content
    if ctx.FromUin == bMasterQQ:
        if strConFrd.startswith("群消息"):
            args = [i.strip() for i in strConFrd.split(" ") if i.strip()]
            strreww = args[1]
            FromGroupId = int(args[2])
            action.sendGroupText(FromGroupId, strreww)
            
        if strConFrd.startswith("私聊"):
            args = [i.strip() for i in strConFrd.split(" ") if i.strip()]
            strreww = args[1]
            FromGroupId = int(args[2])
            action.sendFriendText(FromGroupId, strreww)

        if strConFrd== "关机":
            action.sendFriendText(nSendID, "正在关机")
            bBotClose = True
        if strConFrd== "开机":
            action.sendFriendText(nSendID, "正在开机")
            bBotClose = False
        if strConFrd== "重启":
            action.sendFriendText(nSendID, "正在重启")
            restart_program()
        if strConFrd == "群列表":
            glist = action.getGroupList()
            strList = ""
            for x in glist:
                strList += "ID="+ str(x["GroupId"]) + " name= " + str(x["GroupName"])+"\n"
            action.sendFriendText(nSendID, strList)
    else:
        strMSG = "这个人:"+str(nSendID)+"  给你发消息:"+strConFrd
        action.sendFriendText(bMasterQQ, strMSG)

        # action.getUserList
            
            
def restart_program():
  python = sys.executable
  os.execl(python, python, * sys.argv)

lastBotMsg = []
@bot.on_group_msg
def revAllGroupMsg(ctx: GroupMsg):
    global lastBotMsg
    if(ctx.FromUserId == botQQ):
        lastBotMsg.append(ctx)


@bot.when_disconnected(every_time=True)
def disconnected():
    o = 0
    # print('socket断开~')
    # bot.run()


@bot.when_connected(every_time=True)
def connected():
    o = 0
    # print('socket连接成功~')




elsGameData = {}
with open(curFileDir / "elsGame.json", "r", encoding="utf-8") as f:
    elsCtx = json.load(f)
    try:
        dataStr = elsCtx['data']
        elsGameData = dataStr
    except:
        elsGameData = {}

def SaveElsGameData():
    with open(curFileDir / "elsGame.json", 'w', encoding="utf-8")as f:
        data = {"data": elsGameData}
        json.dump(data, f)

def SaveDKData():
    with open(curFileDir / "dk.json", 'w', encoding="utf-8")as f:
        data = {"dkData": dkDataArr}
        json.dump(data, f)


def takecoinsEle(elem):
    return elem["coins"]



hbData = []
with open(curFileDir / "hb.json", "r", encoding="utf-8") as f:
    elsCtx = json.load(f)
    try:
        hbData = elsCtx['hbData']
    except:
        hbData = []
def SaveHBData():
    with open(curFileDir / "hb.json", 'w', encoding="utf-8")as f:
        data = {"hbData": hbData}
        json.dump(data, f)


@bot.on_group_msg
@deco.ignore_botself
@deco.these_msgtypes('TextMsg')
def EluosiGame(ctx: GroupMsg):
    global elsGameData
    global bBotClose
    global blackList
    global hbData
    if blackList[0] == ctx.FromGroupId:
        return 1
    strGID = str(ctx.FromGroupId)
    strCont = ctx.Content
    nQQID = str(ctx.FromUserId)

    if bBotClose:
        # action.sendGroupText(ctx.FromGroupId, "已关机")
        return 1

    
    if ctx.FromUserId == bMasterQQ:
        if strCont.startswith("群发金币"):
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 2:
                nC = int(args[1])
                userslist = action.getGroupMembers(ctx.FromGroupId)
                for x in userslist:
                    uID = str(x["MemberUin"])
                    try:
                        elsGameData[uID]["coins"] += nC
                    except:
                        elsGameData[uID] = {}
                        elsGameData[uID]["coins"]  = nC
                        elsGameData[uID]["signTime"]  = 0
                SaveElsGameData()
                action.sendGroupText(ctx.FromGroupId, "本群金币发送成功")
        if strCont.startswith("全群通知"):
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 2:
                nC = args[1]
                glist = action.getGroupList()
                for x in glist:
                    action.sendGroupText(x["GroupId"], nC)
                    time.sleep(1)
        if strCont.startswith("发金币"):
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) != 3:
                action.sendGroupText(ctx.FromGroupId, "发金币错误!!! 输入 发金币 QQ号 金币数 来赠送")
            else:  
                strQQ = str(args[1])
                nCoins = 0
                try:
                    nCoins = int(args[2])
                except:
                    action.sendGroupText(ctx.FromGroupId, "发金币错误!!! 别送什么乱七八糟的东西")
                    return 1
                try:
                    elsGameData[strQQ]["coins"] += nCoins
                except:
                    elsGameData[strQQ] = {}
                    elsGameData[strQQ]["coins"] = nCoins
                    elsGameData[strQQ]["signTime"] = 0

                SaveElsGameData()
                action.sendGroupText(ctx.FromGroupId, "管理员发金币!!!\n  用户("+ strQQ +")还剩余"+str(elsGameData[strQQ]["coins"])+"个金币")


    if strCont == "机器人签到" or strCont == "获取金币" or strCont == "签到":
        signTime = int(time.time()) #秒级时间戳
        nCoins = random.randint(300, 600)

        nMyCoins = 0
        try:
            nMyCoins = elsGameData[nQQID]["coins"]
        except:
            elsGameData[nQQID] = {}
            elsGameData[nQQID]["coins"] = 0
            elsGameData[nQQID]["signTime"] = 0
            nMyCoins = 0

        # print("nCoinsnCoins"+str(nCoins) + " signTime "+str(signTime))
        # print("elsGameDataelsGameData==>"+str(elsGameData))
        try:
            lastSignTime = elsGameData[nQQID]["signTime"]
            if signTime - lastSignTime > 7200:
                elsGameData[nQQID]["coins"] += nCoins
                elsGameData[nQQID]["signTime"] = signTime
            else:
                if nMyCoins == 0:
                    lastSignTime = 0
                    nCoins = random.randint(1, 10)
                    elsGameData[nQQID]["coins"] += nCoins
                    elsGameData[nQQID]["signTime"] = signTime
                else:
                    action.sendGroupText(ctx.FromGroupId, "用户:" + nQQID + "\n每2小时才能签到一次哦")
                    return 1
        except:
            elsGameData[nQQID] = {}
            elsGameData[nQQID]["coins"]  = nCoins
            elsGameData[nQQID]["signTime"]  = signTime
        
        if nMyCoins == 0:
            action.sendGroupText(ctx.FromGroupId, "用户:" + nQQID + "\n这么快就把钱花完了? 给你点补贴吧...\n签到领取了"+str(nCoins)+"个金币, 剩余"+str(elsGameData[nQQID]["coins"])+"个金币, ")
        else:
            action.sendGroupText(ctx.FromGroupId, "用户:" + nQQID + "\n签到领取了"+str(nCoins)+"个金币, 剩余"+str(elsGameData[nQQID]["coins"])+"个金币, \n可以用来看买家秀,让机器人骂人,续写小说 别再用光了")


        SaveElsGameData()
    if strCont == "查询金币" or strCont == "金币查询":
        nCoins = 0
        try:
            nCoins = elsGameData[nQQID]["coins"]
        except BaseException as error:
            elsGameData[nQQID] = {}
            elsGameData[nQQID]["coins"] = 0
            elsGameData[nQQID]["signTime"] = 0
            nCoins = 0
            print("errorerror====>"+str(error))
        action.sendGroupText(ctx.FromGroupId, "用户:" + nQQID + "\n你剩余"+str(nCoins)+"个金币, \n可以用来看买家秀,让机器人骂人,续写小说 \n别再用光了")

    if strCont == "本群清零" or strCont == "重新开服" or strCont == "清空金币":
        userslist = action.getGroupMembers(ctx.FromGroupId)
        for x in userslist:
            uID = str(x["MemberUin"])
            try:
                elsGameData[uID]["coins"] = 0
                elsGameData[uID]["steal"] = 0
                elsGameData[uID]["signTime"] = 0
            except:
                a=1
        SaveElsGameData()
        action.sendGroupText(ctx.FromGroupId, "本群金币重置成功, 请签到领金币去吧")

    if strCont == "本群排行":
        userslist = action.getGroupMembers(ctx.FromGroupId)
        aaaRRR = []
        for x in userslist:
            uID = str(x["MemberUin"])
            try:
                acino = elsGameData[uID]["coins"]
                temAAA = {"nickNamme":x["NickName"], "memberUin":str(x["MemberUin"]), "coins":acino}
                aaaRRR.append(temAAA)
            except:
                a=1

        aaaRRR.sort(key=takecoinsEle, reverse=True)

        nLoopNum = 0
        strPPPPPPP = ""
        for xxx in aaaRRR:
            strPPPPPPP += "昵称:"+xxx["nickNamme"]+", 金币数:"+str(xxx["coins"])+"\n"
            nLoopNum += 1
            if nLoopNum >= 15:
                break

        action.sendGroupText(ctx.FromGroupId, strPPPPPPP)



    if strCont.startswith("赠送金币"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) != 3:
            action.sendGroupText(ctx.FromGroupId, "赠送错误!!! 输入 赠送金币 QQ号 金币数 来赠送")
        else:
            nMyCoins = 0
            try:
                nMyCoins = elsGameData[nQQID]["coins"]
            except:
                elsGameData[nQQID] = {}
                elsGameData[nQQID]["coins"] = 0
                elsGameData[nQQID]["signTime"] = 0
                nMyCoins = 0

            strQQ = str(args[1])
            nCoins = 0
            try:
                nCoins = int(args[2])
            except:
                action.sendGroupText(ctx.FromGroupId, "赠送错误!!! 别送什么乱七八糟的东西")
                return 1
            if nMyCoins < nCoins:
                action.sendGroupText(ctx.FromGroupId, "赠送错误!!! 自己就"+str(nMyCoins)+"个金币, 别想着送了")
            elif nCoins <= 0:
                action.sendGroupText(ctx.FromGroupId, "作弊扣1000000金币")
            else:
                try:
                    elsGameData[strQQ]["coins"] += nCoins
                except:
                    elsGameData[strQQ] = {}
                    elsGameData[strQQ]["coins"] = nCoins
                    elsGameData[strQQ]["signTime"] = 0

                elsGameData[nQQID]["coins"] -= nCoins
                SaveElsGameData()
                action.sendGroupText(ctx.FromGroupId, "赠送成功!!!"+ nQQID +" 你还剩"
                    +str(elsGameData[nQQID]["coins"])+"金币\n对方剩余"+str(elsGameData[strQQ]["coins"])+"个金币")

    if strCont.startswith("查询金币"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            nCoins = 0
            strQQQQ = args[1]
            try:
                nCoins = elsGameData[strQQQQ]["coins"]
            except BaseException as error:
                elsGameData[strQQQQ] = {}
                elsGameData[strQQQQ]["coins"] = 0
                elsGameData[strQQQQ]["signTime"] = 0
                nCoins = 0
                print("errorerror====>"+str(error))
            action.sendGroupText(ctx.FromGroupId, "用户:" + strQQQQ + "\n有剩余"+str(nCoins)+"个金币, 请好好评估再抢劫他")

    if strCont.startswith("发红包"):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) != 2:
            return 1
        sendCoins = 0
        try:
            sendCoins = int(args[1])
        except:
            return 1
        if sendCoins < 1000:
            action.sendGroupText(ctx.FromGroupId, "红包数量不得低于1000", atUser=ctx.FromUserId)
            return 1

        nMyCoins = 0
        try:
            nMyCoins = elsGameData[nQQID]["coins"]
        except:
            elsGameData[nQQID] = {}
            elsGameData[nQQID]["coins"] = 0
            elsGameData[nQQID]["signTime"] = 0
            nMyCoins = 0

        if sendCoins > nMyCoins:
            action.sendGroupText(ctx.FromGroupId, "金币不足, 你只有"+str(nMyCoins), atUser=ctx.FromUserId)
            return 1
        
        aaaa = 0
        qqqq = sendCoins
        for i in range(10):
            res11 = math.floor(random.random() * qqqq / 2)
            qqqq = qqqq - res11
            if i == 9:
                res11 = sendCoins - aaaa
            aaaa += res11
            hbData.append(res11)

        elsGameData[nQQID]["coins"] -= sendCoins
        SaveElsGameData()
        SaveHBData()
        action.sendGroupText(ctx.FromGroupId, "你的红包发出了,已经分成10份,共"+str(sendCoins)+"个金币", atUser=ctx.FromUserId)

    if strCont.startswith("抢红包") or strCont.startswith("领红包"):
        if len(hbData) <= 0:
            action.sendGroupText(ctx.FromGroupId, "红包领完了, 要抢就自己发", atUser=ctx.FromUserId)
            return 1
        curCC = hbData.pop(0)
        if curCC <= 0:
            curCC = 1
        
        try:
            elsGameData[nQQID]["coins"] += curCC
        except:
            elsGameData[nQQID] = {}
            elsGameData[nQQID]["coins"] = curCC
            elsGameData[nQQID]["signTime"] = 0

        SaveElsGameData()
        SaveHBData()
        action.sendGroupText(ctx.FromGroupId, "恭喜抢到了"+str(curCC)+"个金币, 剩余"+str(elsGameData[nQQID]["coins"])+"个金币", atUser=ctx.FromUserId)

def CheckCoins(strID: str, nCost1: int, nGroupID: int):
    global elsGameData

    nCost = nCost1*6
    
    playerData = {}
    try:
        playerData = elsGameData[strID]
    except:
        elsGameData[strID] = {}
        elsGameData[strID]["coins"] = 0
        elsGameData[strID]["signTime"] = 0
    playerData = elsGameData[strID]

    playerCoins = playerData["coins"]
    if(nCost > playerCoins):
        action.sendGroupText(nGroupID, "用户:"+strID+" 金币不够了, 这个功能"+str(nCost)+"金币一次")
        return False
    else:
        elsGameData[strID]["coins"] -= nCost
        SaveElsGameData()
        return True

if __name__ == '__main__':
    # ---------------------------------------------------------------------------------
    print("qidong")
    bot.run()

