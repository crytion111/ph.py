# -*- coding: utf-8 -*-

from iotbot import IOTBOT, Action, FriendMsg, GroupMsg, EventMsg
import iotbot.decorators as deco
from iotbot.refine import *
from retrying import retry
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from tinydb.operations import add
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
import hashlib
import uuid
import pathlib
from PIL import Image, ImageDraw, ImageFont
import urllib
import urllib.parse
from MyQR import myqr
import wave
import math
#import error
import struct
from base64 import b64encode
import cv2
import numpy as np
import jieba
import jieba.posseg as pseg
jieba.setLogLevel(20)

#------------------------------混乱#------------------------------
def transYin(x, y, aaa):
    if random.random() > aaa:
        return x
    if x in {',', '，', '。'}:
        return '❤'
    if x in {'!', '！', ' '}:
        return '..'
    if len(x) > 1 and random.random() < 0.5:
        return f'{x[0]}〇..❤{x}'
    else:
        if y == 'n' and random.random() < 0.5:
            x = '〇' * len(x)
        return f'..{x}'


def chs2yin(s, aaa=0.5):
    return ''.join([transYin(x, y, aaa) for x, y in pseg.cut(s)])
#----------------------------------------------------------------------------------





#------------------------------幻影坦克------------------------------
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
    base64_str = cv2.imencode('.png',out_pic)[1].tobytes()
    base64_str = base64.b64encode(base64_str)
    return base64_str
#----------------------------------------------------------------------------------




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


bot = IOTBOT(157199224, log=False)
action = Action(bot, queue=False)

bOpenThisBOT = True
dataCiliGroupData = {}

nAAAAAAAA = 91

nBBBBBB = 99999


nReciveTimes = 0


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

#maijiaxiu ---------------------------------------------------------------------------------------------------------------

def maijiaxiu(urlTB):
    html = requests.get(urlTB)
    with open('./MJX.png', 'wb') as file:
        file.write(html.content)


#----------------------------------------------------------------------------------------------------------------



# clclc---------------------------------------------------------------------------------
def ciliSou(strSearch, nmmm):
    urlss = "https://zhaobt500.xyz/s.php?q=" + strSearch
    strText = requests.get(urlss).text
    strTemp11 = strText

    textArr = []
    textTTTTArr = []
    sizeArr = []
    arr1 = strTemp11.split('cililianjie/')

    #print(len(arr1))

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


    #print(textArr[0])
    #print(textTTTTArr[0])

    nLength = len(textTTTTArr)
    if nmmm > nLength:
        nmmm = nLength

    if nLength > nmmm:
        nLength = nmmm
    strResult = ''
    for i in range(nLength):
        strUUU = textArr[i]
        strTTTI = textTTTTArr[i]
        strLine = "《" + strTTTI +"》大小:" + sizeArr[i] + " 地址：magnet:?xt=urn:btih:" + strUUU+" \n "
        strResult = strResult + strLine


    #print(strResult)
    return strResult

#-----------------------------------------------------------------------







#---------------------------------------------
ENSTRS = ("富强", "民主", "文明", "和谐", "自由", "平等",
          "公正", "法治", "爱国", "敬业", "诚信", "友善")

def decoder(string):
    len_str = len(string)
    if len_str % 16 != 0:
        return "jiemishibai1!!!!!!!!!"
    result = ''
    for x in range(0, len_str, 16):
        decode_char = string[x:x+16]
        temp_int = [ENSTRS.index(decode_char[y:y+2]) for y in range(0, 16, 2)]
        int_list = [temp_int[x]+temp_int[x+1] for x in range(0, 8, 2)]
        bin_temp = [bin(i).replace('0b', '') for i in int_list]
        binstr_list = []
        for b in bin_temp:
            if len(b) < 4:
                binstr_list.append(b.zfill(4))
            else:
                binstr_list.append(b)
        binstr = ''.join(binstr_list)
        result = result + chr(int(binstr, 2))
    return result
 
 
def encoder(string):
    result = ''
    binstr_list = [b.replace('0b', '') for b in [bin(ord(c)) for c in string]]
    for binstr in binstr_list:
        len_binstr = len(binstr)
        if len_binstr < 16:
            binstr = binstr.zfill(16)
        temp_list = [binstr[start:start+4] for start in range(0, 16, 4)]
        int_list = []
        for i in temp_list:
            i = int(i, 2)
            if i >= 11:
                int_list.append(11)
                int_list.append(i - 11)
            else:
                int_list.append(0)
                int_list.append(i)
        result = result + ''.join([ENSTRS[index] for index in int_list])
    return result
 

#---------------------------------------------













# --------------------------------------------------------------------------
def jiemi(strText):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    aaaa = {
        'text': strText
    }
    try:
        resultStr = ""
        r = json.loads(requests.post(url, data = aaaa).text)
        #print(str(r))
        name = r[0]['name']
        trans = r[0]['trans']
        resultStr = "\n缩写是"+ (name) + "\n 结果可能是" + (str(trans))
        #print(resultStr)
        return resultStr
    except:
        #print(str(err))
        return "解密失败！！！！！！！！！！！"


# --------------------------------------------------------------------------









#摩斯码 CODE----------------------------------------------------------------------------

def wv(t,f,v,wf):
    sr=8000
    '''
    t:写入时长
    f:声音频率
    v：音量
    wf：一个可以写入的音频文件
    sr：采样率
    '''
    tt=0
    dt=1.0/sr
    while tt<=t:
        s=math.sin(tt*math.pi*2*f)*v*32768 #采样，调节音量，映射到[-2^15,2^15)
        s=int(s)
        fd=struct.pack("h",s) #转换成8bit二进制数据
        wf.writeframes(fd) #写入音频文件
        tt+=dt #时间流逝
         
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
 
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
            if i == 2 :
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''
    return decipher
 
def mainMorse(msg, FromGroupId):
    
    ff=wave.open("./morse.wav","w")
    ff.setframerate(8000)
    ff.setnchannels(1)
    ff.setsampwidth(2)
 

    message = msg
    if u'\u0039' >= message >= u'\u0030' or u'\u005a' >= message >= u'\u0041' or u'\u007a'>= message >= u'\u0061': #判断是否只有数字字母
        li = encrypt(message.upper())
        #print (li)
        mo = []
        for i in li:
            if i=="-":
                mo.append("2")
                mo.append("0")
            elif i == ".":
                mo.append("1")
                mo.append("0")
            elif i==" ":
                mo.append("3")
        #print(mo)
        lo = []
        for i in mo:
            if i =="0" or i == "1":
                lo.append(1)
            elif i =="2" or i == "3":
                lo.append(3)
        #print(lo)
        note= {"1":600,"2":600,"3":0,"0":0} #600是滴答正玄波频率，如更改2个都改
        for i in range(len(mo)):
            wv(lo[i]/17.0,note[mo[i]], 0.8, ff) #改变17数值cw快慢
        ff.close()
        
        with open('./morse.wav', 'rb') as ffff: 
            dataffff = ffff.read()
            encodestr = base64.b64encode(dataffff) # 得到 byte 编码的数据
            action.send_group_voice_msg(FromGroupId, "", encodestr)
        return True
    else:
        result = decrypt(message)
        return False
        #print (result)


#-------------------------------------------------------------------------------------














#-----JIKI----------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------jiki一下
#from error import error

class Jiki:
	def __init__(self):
		self.headers = {
			"Content-Type":"application/json;charset=UTF-8",
			"Client":"web",
			"Client-Version":"2.1.66a",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
		}
		self.auto_complete = "https://api.jikipedia.com/go/auto_complete"
		self.api = "https://api.jikipedia.com/go/search_definitions"
		self.eval_cqp_data = ""

	def check(self, word):
		
		if len(word) > 10:
			return {"res":"不支持该类型消息", "error": 99}
		else:
			i = {}
			i["error"] = 0
			i["title"],i["res"] = self.jiki(word)
			i["complete"] = self.complete(word)
			return i

	def jiki(self,word):
		
		data = {
			"phrase":word,
			"page":1
		}
		try:
			resp = requests.post(self.api,headers=self.headers,data=json.dumps(data),timeout=10)
		except:
			return "", "查询错误 ERROR 机器人即将爆炸"
		resp.encoding = "utf8"
		try:
			resp = json.loads(resp.text)["data"]
			# resp = json.loads(resp.text)["data"][0]
			for i,j in enumerate(resp):
				# print(resp[i]["term"]["title"])
				if word == resp[i]["term"]["title"]:
					title = resp[i]["term"]["title"]
					# res = resp["content"].replace("]","")
					res = re.sub(r"\[.*?:","",resp[i]["content"].replace("]",""))
					break
			else:
				i = random.randint(1,len(resp))-1
				title = resp[i]["term"]["title"]
				# res = res[0]["content"].replace("]","")
				res = re.sub(r"\[.*?:","",resp[i]["content"].replace("]",""))
		except Exception as e:
			# print(e)
			return "","查找不到相关释义"
		else:
			return title,res
			# return res.replace("\n","")
		
	def complete(self,word):
		
		data = {
			"phrase":word
		}
		try:
			resp = requests.post(self.auto_complete,headers=self.headers,data=json.dumps(data),timeout=10)
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


























#-------------PH PIC----------------------------------------------------------
#-----------------------------------------------------------------------------
#-------------------------------------------------------------------------------

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
        font_width / len(text) * RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH
    )
    image_width = font_width + 2 * left_blank
    image_height = font_height + offset_y + blank_height * 2
    image = Image.new("RGBA", (image_width, image_height), BOX_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((left_blank, blank_height), text, fill=RIGHT_TEXT_COLOR, font=font)

    # 圆
    magnify_time = 10
    magnified_radii = radii * magnify_time
    circle = Image.new(
        "L", (magnified_radii * 2, magnified_radii * 2), 0
    )  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, magnified_radii * 2, magnified_radii * 2), fill=255)  # 画白色圆形

    # 画4个角（将整圆分离为4个部分）
    magnified_alpha_width = image_width * magnify_time
    magnified_alpha_height = image_height * magnify_time
    alpha = Image.new("L", (magnified_alpha_width, magnified_alpha_height), 255)
    alpha.paste(circle.crop((0, 0, magnified_radii, magnified_radii)), (0, 0))  # 左上角
    alpha.paste(
        circle.crop((magnified_radii, 0, magnified_radii * 2, magnified_radii)),
        (magnified_alpha_width - magnified_radii, 0),
    )  # 右上角
    alpha.paste(
        circle.crop(
            (magnified_radii, magnified_radii, magnified_radii * 2, magnified_radii * 2)
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














#--AI CHAT--------------------------------------------------------------------------------#--------------------------------------------------------------------------------------#---------------------------------------------------------------------------------

uid = '1'
def chatAI(text='hello'):
    TULING_KEY = '059f9782bab24de6a63d4083590a803b'
    
    url = 'http://www.tuling123.com/openapi/api'
    payloads = {
        'key': TULING_KEY,
        'info': text,
        'userid': uid,
    }
    try:
        r = json.loads(requests.post(url, data = payloads).text)
        return r['text']
    except:
        return "error_chatAI"















#----------------RECIVE-------------------------#--------------------------------------------------------------------------------------#---------------------------------------------------------------------------------
@bot.on_group_msg
@deco.only_this_msg_type('TextMsg')
def receive_group_msg(ctx: GroupMsg):
    global bOpenThisBOT
    global dataCiliGroupData
    global nReciveTimes

    strGID = str(ctx.FromGroupId)
    strCont = ctx.Content

    if 157199224 == ctx.FromUserId:
        return 1
    nReciveTimes = nReciveTimes + 1
    #logger.success('nReciveTimes= ' + str(nReciveTimes))
    
    if random.random() < 0:
        re = chs2yin(strCont, 0)
        action.send_group_text_msg(ctx.FromGroupId, re)

    if strCont == "关闭磁力" and ctx.FromUserId == 1973381512:
        dataCiliGroupData[strGID] = False
        action.send_group_text_msg(ctx.FromGroupId, "本群磁力已关闭", ctx.FromUserId)

    if strCont == "开启磁力" and ctx.FromUserId == 1973381512:
        dataCiliGroupData[strGID] = True
        action.send_group_text_msg(ctx.FromGroupId, "本群磁力已开启", ctx.FromUserId)

#clici
    if strCont.startswith("磁力搜"):
        bbb = False
        try:
            bbb = dataCiliGroupData[strGID]
        except :
            bbb = False

        if bbb == False:
            action.send_group_text_msg(ctx.FromGroupId, "磁力关掉了, 请联系主人, 找不到就算了", ctx.FromUserId)
            return 1
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strSs = args[1]
            strRRqq = ciliSou(strSs, 6)
            action.send_group_text_msg(ctx.FromGroupId, strRRqq)
        elif len(args) == 3:
            strSs = args[1]
            nMMM = int(args[2])
            strRRqq = ciliSou(strSs, nMMM)
            action.send_group_text_msg(ctx.FromGroupId, strRRqq)


#PORNHUB PIC---------------------------------------------------------------------------------------
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
        action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", picBase64Buf, "", timeout=15)
# WIKI------------------------------------------
    elif strCont.startswith("找梗 ") or strCont.startswith("百度一下 ") or strCont.startswith("梗 "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            jikidata = jkjk.check(args[1])
            if jikidata["error"] == 0:
                action.send_group_text_msg(ctx.FromGroupId, "\n"+jikidata["title"]+"\n"+jikidata["res"], ctx.FromUserId)
            else:
                action.send_group_text_msg(ctx.FromGroupId, "\n"+"查询错误 ERROR 机器人即将爆炸!!!!!!!!!!!!", ctx.FromUserId)
# QR CODE------------------------------
    elif strCont.startswith("二维码制作 ") or strCont.startswith("qr "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            index = random.randint(1, 40)
            strWords = args[1]
            if is_contain_chinese(strWords):
                action.send_group_text_msg(ctx.FromGroupId, "\n"+"不能包含中文!!!!!!!!!!!!", ctx.FromUserId)
            else:
                #strWord2 = to_unicode(strWords)
                try:
                    myqr.run(words = strWords, colorized = True, save_name = "./QQRR.png")
                    with open('./QQRR.png', 'rb') as f:  # 以二进制读取图片
                        data = f.read()
                        encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                        action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)
                        
                except:
                    print("二维码制作 Error")


# 摩斯 CODE------------------------------
    elif strCont.startswith("摩斯码 ") or strCont.startswith("ms "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strWords = args[1]
            if not is_contain_chinese(strWords):
                try:
                    mainMorse(strWords, ctx.FromGroupId)
                except:
                    print("摩斯码 Error")
            else:
                action.send_group_text_msg(ctx.FromGroupId, "\n"+"不能包含中文!!!!!!!!!!!!", ctx.FromUserId)


# 加密通话 ------------------------------
    elif strCont.startswith("解密 ") or strCont.startswith("解谜 ") or strCont.startswith("翻译翻译 "):
        args = [i.strip() for i in strCont.split(" ") if i.strip()]
        if len(args) == 2:
            strWords = args[1]
            try:
                strR = jiemi(strWords)
                action.send_group_text_msg(ctx.FromGroupId, strR, ctx.FromUserId)
            except:
                action.send_group_text_msg(ctx.FromGroupId, "解密 Error", ctx.FromUserId)
        else:
           action.send_group_text_msg(ctx.FromGroupId, "\n"+"输入错误!!!!!!!!!!!!", ctx.FromUserId)
    elif strCont.find("买家秀") > -1:
        indexInt = random.randint(1, 6)
        taobaoUrl = "https://api.uomg.com/api/rand.img3"
        if indexInt == 1:
            taobaoUrl = "https://api.ghser.com/tao"
        elif indexInt == 2: 
            taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=胖次猫"
        else :
            taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=七了个三"
        #action.send_group_pic_msg(ctx.FromGroupId, taobaoUrl, False, ctx.FromUserId, "OK!!!!", "", "", timeout=15)
        maijiaxiu(taobaoUrl)
        with open('./MJX.png', 'rb') as f:  # 以二进制读取图片
            data = f.read()
            encodestr = base64.b64encode(data) # 得到 byte 编码的数据
            action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)       
    elif strCont.find("幻影坦克") > -1:

        #ran2 = random.randint(0, len(original_list2))
        #picUrl = original_list2[ran2]
        
        nIndex = random.randint(1, 379)
        strUUUR = "http://crytion.top:82/setu/ecy/A_" + str(nIndex)+".jpg"
        html = requests.get(strUUUR)
        with open('./2.png', 'wb') as file:
            file.write(html.content)

        rrrr = random.randint(1, 40)
        f1 = "./jk/"+ str(rrrr) +'.jpg'  # 上层
        f2 = '2.png'  # 下层
        savePath = r'T1.png'  # 保存路径
        try:
            base64_str = make(f1, f2, savePath)
            action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", base64_str, "", timeout=15)
        except:
            action.send_group_text_msg(ctx.FromGroupId, "\n"+"合成错误，抱歉!!!!!!!!!!!!", ctx.FromUserId)
        


@bot.on_group_msg
@deco.not_botself
@deco.only_this_msg_type('AtMsg')
def receive_AT_group_msg(ctx: GroupMsg):
    objCtx = json.loads(ctx.Content)
    strCont = objCtx['Content']
    atUserID = objCtx['UserID'][0]

    #print("#asdasda==" + str(strCont.find("买家秀")))

    if(atUserID == 157199224):
        # 模特 ------------------------------
        if strCont.find("买家秀") > -1:
            indexInt = random.randint(1, 6)
            taobaoUrl = "https://api.uomg.com/api/rand.img3"
            if indexInt == 1:
                taobaoUrl = "https://api.ghser.com/tao"
            elif indexInt == 2: 
                taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=胖次猫"
            else :
                taobaoUrl = "https://api.uomg.com/api/rand.img3?sort=七了个三"
            maijiaxiu(taobaoUrl)
            with open('./MJX.png', 'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)
        elif strCont.find("加密") > -1:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 3:
                str111 = encoder(args[2])
                action.send_group_text_msg(ctx.FromGroupId, str111)
            else:
                action.send_group_text_msg(ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        elif strCont.find("解密") > -1 or strCont.find("翻译翻译") > -1 :
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            if len(args) == 3:
                str222 = jiemi(args[2])
                action.send_group_text_msg(ctx.FromGroupId, str222)
            else:
                action.send_group_text_msg(ctx.FromGroupId, "输入的格式错误!", ctx.FromUserId)
        else:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]
            text = "ERROR!!! "
            if len(args) == 2:
                text = chatAI(args[1])
                action.send_group_text_msg(ctx.FromGroupId, text, ctx.FromUserId)

        
    


@bot.on_group_msg
@deco.not_botself
@deco.only_this_msg_type('PicMsg')
def receive_PIC_group_msg(ctx: GroupMsg):
    
    global nAAAAAAAA
    global nBBBBBB

    objCtx = json.loads(ctx.Content)
    strCont = ""
    picArr = []
    try:
        strCont = objCtx['Content']
        picArr = objCtx['GroupPic']
    except :
        strCont = ""
    

    nIndex = 1
    if strCont == "制作幻影坦克" and len(picArr) == 2:

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
            action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", base64_str, "", timeout=15)
        except:
            action.send_group_text_msg(ctx.FromGroupId, "\n"+"合成错误，抱歉!!!!!!!!!!!!", ctx.FromUserId)
        

    elif strCont.startswith("脱衣") and len(picArr) == 1:
        nAAAAAAAA = nAAAAAAAA + 1

        if strCont == "脱衣":
            strUrlqq = picArr[0]["Url"]
            html = requests.get(strUrlqq)
            with open('./11/'+ str(nAAAAAAAA) +'.png', 'wb') as file:
                file.write(html.content)
            strADB = "./dreampower run --input 11/"+ str(nAAAAAAAA) +".png --output 11/" + str(nAAAAAAAA) + "ot.png --cpu --n-cores 4 --experimental-color-transfer --auto-resize --nsize 1 --bsize 1.6 --hsize 1 --vsize 1"
            os.system(strADB)

            print (time.strftime("FINISH!!!!!!!!! %Y-%m-%d %H:%M:%S", time.localtime()))
            with open("./11/"+ str(nAAAAAAAA) +"ot.png", 'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)

        else:
            args = [i.strip() for i in strCont.split(" ") if i.strip()]

            #print("assssssssssssdasd" + str(len(args)))

            if len(args) == 7:
                strTypeaa = " --auto-resize "
                if args[1] == "2":
                    strTypeaa = " --auto-resize-crop "
                elif args[1] == "3":
                    strTypeaa = " --auto-rescale "
                strAAAA = " --experimental-color-transfer "
                if args[6] == "0":
                    strAAAA = " "

                strUrlqq = picArr[0]["Url"]
                html = requests.get(strUrlqq)
                with open('./11/'+ str(nAAAAAAAA) +'.png', 'wb') as file:
                    file.write(html.content)
                
                strADB = "./dreampower run --input 11/"+ str(nAAAAAAAA) +".png --output 11/" + str(nAAAAAAAA) + "ot.png --cpu --n-cores 4 "+ strTypeaa + strAAAA +"--bsize "+ args[2] +"  --nsize "+ args[3] +" --vsize "+ args[4] +" --hsize "+ args[5]
                os.system(strADB)

                print (time.strftime("FINISH!!!!!!!!! %Y-%m-%d %H:%M:%S", time.localtime()))
                with open("./11/"+ str(nAAAAAAAA) +"ot.png", 'rb') as f:  # 以二进制读取图片
                    data = f.read()
                    encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                    action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)
                    
            else:
                action.send_group_text_msg(ctx.FromGroupId, "参数少了!需要: 脱衣 图片缩放类型 Boob大小 Ru头大小 Vagina大小 yin毛大小 是否使用原图颜色 \n 比如: 脱衣 1 1.5 1 1 0.9 1", ctx.FromUserId)
            
    elif strCont.startswith("放大qwe") and len(picArr) == 1:
        nBBBBBB = nBBBBBB + 1
        strUrlqq = picArr[0]["Url"]
        html = requests.get(strUrlqq)
        with open('./223/'+ str(nBBBBBB) +'.png', 'wb') as file:
            file.write(html.content)
            strADB = "./realesrgan-ncnn-vulkan -i 223/"+ str(nBBBBBB) +".png -o 223/" + str(nBBBBBB) + "ot.png"
            os.system(strADB)
            print (time.strftime("放大成功!!!!!!!!! %Y-%m-%d %H:%M:%S", time.localtime()))
            with open("./223/"+ str(nBBBBBB) +"ot.png", 'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                action.send_group_pic_msg(ctx.FromGroupId, "", False, ctx.FromUserId, "OK!!!!", encodestr, "", timeout=15)
            




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

