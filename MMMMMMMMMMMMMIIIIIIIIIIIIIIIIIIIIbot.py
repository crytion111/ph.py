from graia.ariadne.entry import Ariadne, Friend, MessageChain, config, Group, LogConfig
from graia.ariadne.message.element import Image, Plain, At, Voice
from graia.ariadne.message.parser.twilight import Twilight, Sparkle
from graia.ariadne.event.message import GroupMessage
import io
import os
import requests
from PIL import Image as ImagePIL
import base64
import time
import cpuinfo
import psutil
import datetime
import pynvml
from io import BytesIO

session = requests.Session()

import torch



model2 = torch.hub.load(
    "AK391/animegan2-pytorch:main",
    "generator",
    pretrained=True,
    device="cuda",
    progress=False
)


model1 = torch.hub.load("AK391/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v1",  device="cuda")
face2paint = torch.hub.load(
    'AK391/animegan2-pytorch:main', 'face2paint', 
    size=512, device="cuda",side_by_side=False
)
def AnimFace(img, ver):
    if ver == 'v1':
        out = face2paint(model2, img)
    else:
        out = face2paint(model1, img)
    return out

def image_to_base64(img, fmt='png'):
    output_buffer = BytesIO()
    img.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    # return f'data:image/{fmt};base64,' + base64_str
    return base64_str

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
    available_nc = round(
        (float(memory.available) / 1024 / 1024 / 1024), 3)  # 空闲内存
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
    boottime = datetime.datetime.fromtimestamp(
        boot).strftime("%Y-%m-%d %H:%M:%S")
    nowtime = datetime.datetime.fromtimestamp(
        now).strftime("%Y-%m-%d %H:%M:%S")
    up_time = str(
        datetime.datetime.utcfromtimestamp(now).replace(microsecond=0)
        - datetime.datetime.utcfromtimestamp(boot).replace(microsecond=0)
    )
    alltime = (boottime, nowtime, up_time)
    return alltime


def gpu_Info():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 这里的0是GPU id
    gpuName = str(pynvml.nvmlDeviceGetName(handle), encoding='utf-8')
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    all = (meminfo.total / 1024 / 1024)  # 第二块显卡总的显存大小
    usese = (meminfo.used / 1024 / 1024)  # 这里是字节bytes，所以要想得到以兆M为单位就需要除以1024**2
    free = (meminfo.free / 1024 / 1024)  # 第二块显卡剩余显存大小
    msg = "\n显卡名:"+gpuName+"  \n显存总容量:"+str(all)+"MB  \n已用显存:"+str(usese)+"MB"
    pynvml.nvmlShutdown()
    return msg


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

    gpuInfo = gpu_Info()

    return full_meg+"\n"+gpuInfo


# 图片转为Base64

def toBase64(imgUrl):
    req = session.get(imgUrl)
    img_str = base64.b64encode(req.content).decode()
    return "data:image/png;base64," + img_str


def img2img(imgBase64: str, prompt: str = ""):

    # print("resp=       ========== =>" + imgBase64)

    payload = {
        "init_images": [
            imgBase64
        ],
        "resize_mode": 2,
        "denoising_strength": 0.55,
        "prompt": prompt,
        "seed": -1,
        "batch_size": 1,
        "n_iter": 1,
        "steps": 28,
        "cfg_scale": 11,
        "width": 640,
        "height": 512,
        "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
        "s_noise": 1,
        "sampler_index": "Euler a"
    }
    resp = requests.post(
        url="http://127.0.0.1:7861/sdapi/v1/img2img", json=payload)
    # print("resp=       ========== =>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]
    return processed


def txt2img(prompt: str,
            negative_prompt: str = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
            steps: int = 28,
            sampler_index: str = "Euler a",
            seed: int = -1,
            wwwwww: int = 960,
            hhhhhh: int = 512,
            ):

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": min(steps, 50),
        "sampler_index": sampler_index,
        "cfg_scale": 11,
        "width": wwwwww,
        "height": hhhhhh,
        "seed": seed
    }

    resp = requests.post(
        url="http://127.0.0.1:7861/sdapi/v1/txt2img", json=payload)
    # print("resp==>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]
    return processed


app = Ariadne(
    config(
        verify_key="ServiceVerifyKey",
        account=1209916110,
    ), log_config=LogConfig("INFO")
)
app.log_config.clear()


floatTxt2img = -1
floatCDCD = 20


@app.broadcast.receiver(GroupMessage)
async def group_message_listener(app: Ariadne, group: Group,  message: MessageChain, event: GroupMessage):

    global floatTxt2img
    global floatCDCD
    strCont = str(message)

    if At(1209916110) in message:
        if "帮助" in strCont:
            repl00 = MessageChain(Plain("\n1,发送pet获取头像表情包功能的菜单\n\n2,发送'生成图'或者'/ai text'加英文英文英文英文英文英文英文英文英文英文英文关键词,使用AI合成图\n\n"+
                "3,发送'图生图'或者'/ai image'加一张图片和英文英文英文英文英文英文英文英文英文英文英文关键词描述,使用AI的以图合成图功能\n\n4,发送'高清'加一张图片,使用AI的超分辨率功能,提升4倍分辨率\n\n"+
                "5,发送'动漫化'加一张图,使用AI的动漫风格合成功能\n\n6,发送'系统信息'查看机器人使用状态\n\n以上功能不需要@机器人\n\n以上功能不需要@机器人\n\n以上功能不需要@机器人\n\n"))
            return app.send_message(group, repl00, quote = message)

    
    if "生成图" in strCont or "/ai text" in strCont:
        fNowTime = time.time()
        dtTime = fNowTime - floatTxt2img
        dtTime = int(dtTime)
        strCont = strCont.lower()
        if "nude" in strCont or "nipple" in strCont or "breast" in strCont or "pussy" in strCont or "nsfw" in strCont or "sex" in strCont or "ass" in strCont or "disrobe" in strCont:
            repl00 = MessageChain(Plain("\n你想要色色?要我喊管理过来吗?"))
            return app.send_message(group, repl00, quote = message)
        if dtTime < floatCDCD:
            leftTime = floatCDCD-dtTime
            repl1 = MessageChain(Plain(
                "\n" + str(floatCDCD)+" 秒CD一张图,等等再弄吧,还剩"+str(leftTime)+"秒"))
            return app.send_message(group, repl1, quote = message)
        floatTxt2img = time.time()
        strSsss = strCont.replace("生成图 ", "")
        strSsss = strCont.replace("生成图", "")
        strSsss = strSsss.replace("/ai text ", "")
        strSsss = strSsss.replace("/ai text", "")
        strSsss = strSsss.replace("，", ",")
        www = 960
        hhh = 512
        if "竖屏" in strCont:
            www = 512
            hhh = 960
        strSsss = strSsss.replace("竖屏", "")
        strSsss = strSsss.replace("横屏", "")
        if len(strSsss) >= 1:
            ch = strSsss[0]
            if u'\u4e00' <= ch <= u'\u9fff':
                return app.send_message(group, "日你妈弱智, 发英文关键词", quote = message)
        if len(strSsss) >= 2:
            ch = strSsss[1]
            if u'\u4e00' <= ch <= u'\u9fff':
                return app.send_message(group, "日你妈弱智, 发英文关键词", quote = message)

        repl2 = MessageChain(At(event.sender.id),
                             Plain("\n收到,生成图片中,可能一分钟后成功...."))
        await app.send_message(group, repl2)

        img64 = txt2img(strSsss, wwwwww=www, hhhhhh=hhh)
        # if len(strSsss) > 30:
        #     strSsss = strSsss[0: 30]+"....."
        strRepl = "\n你要求的图生成好了"
        repl3 = MessageChain(Image(base64=img64), Plain(strRepl))
        floatTxt2img = time.time()
        return app.send_message(group, repl3, quote = message)
    if "图生图" in strCont or "/ai image" in strCont:

        strCont = strCont.lower()
        if "nude" in strCont or "nipple" in strCont or "breast" in strCont or "pussy" in strCont or "nsfw" in strCont or "sex" in strCont or "ass" in strCont or "disrobe" in strCont:
            repl00 = MessageChain(Plain("\n你想要色色?要我喊管理过来吗?"))
            return app.send_message(group, repl00, quote = message)

        imageArr = event.message_chain[Image]
        # print("=============>"+str(imageArr))
        if len(imageArr) == 1:
            strAlllll = ""
            strArr = event.message_chain[Plain]
            # print("=============>"+str(strArr))
            for strP in strArr:
                strAlllll += str(strP)
            # print("=======strAlllll======>" + strAlllll)
            strAlllll = strAlllll.replace("图生图 ", "")
            strAlllll = strAlllll.replace("图生图", "")
            strAlllll = strAlllll.replace("/ai image ", "")
            strAlllll = strAlllll.replace("/ai image", "")
            strUrlqq = imageArr[0].url

            
            if len(strAlllll) >= 1:
                ch = strAlllll[0]
                if u'\u4e00' <= ch <= u'\u9fff':
                    return app.send_message(group, "日你妈弱智, 发英文关键词", quote = message)
            if len(strAlllll) >= 2:
                ch = strAlllll[1]
                if u'\u4e00' <= ch <= u'\u9fff':
                    return app.send_message(group, "日你妈弱智, 发英文关键词", quote = message)

            # print("=======strUrlqq======> " + strUrlqq)
            html = toBase64(strUrlqq)

            repl2 = MessageChain(At(event.sender.id),Plain("\n收到,生成图片中,可能一分钟后成功...."))
            await app.send_message(group, repl2)
            img64 = img2img(html, strAlllll)
            strRepl = "\n你要求的图生成好了"
            repl3 = MessageChain(Image(base64=img64), Plain(strRepl))
            return app.send_message(group, repl3, quote = message)
    if "画质" in strCont or "高清" in strCont:
        imageArr = event.message_chain[Image]
        # print("=============>"+str(imageArr))
        if len(imageArr) == 1:
            strRRRR = "realesrgan-x4plus"
            if "漫" in strCont:
                strRRRR = "realesrgan-x4plus-anime"
            nAAAAAAAA = time.time()
            strUrlqq = imageArr[0].url
            html = requests.get(strUrlqq)
            strPathName = './realesrgan/' + str(nAAAAAAAA) + '.png'
            with open(strPathName, 'wb') as file:
                file.write(html.content)

            imgTemp = ImagePIL.open(strPathName)
            imgTempSize = imgTemp.size
            maxSize = max(imgTempSize)  # 图片的长边
            if maxSize > 1600:
                repl31 = MessageChain(
                    At(event.sender.id), Plain("原图分辨率有边长超过1600,不再使用高清化"))
                return app.send_message(group, repl31)
            strADB = "realesrgan-ncnn-vulkan.exe -i " + \
                strPathName + " -o output.png -n " + strRRRR
            os.system(strADB)
            strRepl = "\n画质提升好了,模型:" + strRRRR + \
                "\n点击查看原图看效果\n默认使用真实世界模型\n发送'高清漫画'可以使用动漫专属模型"
            repl3 = MessageChain(Image(path="output.png"),Plain(strRepl))
            return app.send_message(group, repl3, quote = message)
    if "系统信息" in strCont:
        strRepl = sysinfo()
        repl3 = MessageChain(At(event.sender.id), Plain(strRepl))
        return app.send_message(group, repl3)
    if "动漫化" in strCont:
        imageArr = event.message_chain[Image]
        if len(imageArr) == 1:
            try:
                nAAAAAAAA = time.time()
                strUrlqq = imageArr[0].url
                html = requests.get(strUrlqq)
                strPathName = './anim/' + str(nAAAAAAAA) + '.png'
                with open(strPathName, 'wb') as file:
                    file.write(html.content)
                imgTemp = ImagePIL.open(strPathName)
                strMod = "v1"
                if "v2" in strCont:
                    strMod = "v2"
                plImg = AnimFace(imgTemp, strMod)
                image_data = image_to_base64(plImg)
                strRepl = "好了, 默认v1模型, 可以发送'动漫化v2'使用另一个模型"
                repl3 = MessageChain(Image(base64=image_data), Plain(strRepl))
                return app.send_message(group, repl3, quote = message)
            except:
                return app.send_message(group, "出错了,换张图吧", quote = message)




Ariadne.launch_blocking()
