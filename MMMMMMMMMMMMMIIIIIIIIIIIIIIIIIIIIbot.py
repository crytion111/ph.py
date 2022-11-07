from graia.ariadne.entry import Ariadne, Friend, MessageChain, config,Group,LogConfig
from graia.ariadne.message.element import Image, Plain,At
from graia.ariadne.message.parser.twilight import Twilight, Sparkle
from graia.ariadne.event.message import GroupMessage
import io
import os
import requests
from PIL import Image as ImagePIL
import base64
import time
from gradio.processing_utils import encode_pil_to_base64

session = requests.Session()

# 图片转为Base64
def toBase64(imgUrl):
    req = session.get(imgUrl)
    img_str =base64.b64encode(req.content).decode()
    return "data:image/png;base64," + img_str


def img2img(imgBase64:str, prompt:str = ""):

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
    resp = requests.post(url="http://127.0.0.1:7861/sdapi/v1/img2img", json=payload)
    # print("resp=       ========== =>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]
    return processed



def txt2img(prompt: str, 
            negative_prompt: str = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry", 
            steps: int = 28, 
            sampler_index: str = "Euler a", 
            seed: int = -1,
            wwwwww:int = 960,
            hhhhhh:int = 512,
            ):
    
    payload = {
        "prompt":prompt,
        "negative_prompt": negative_prompt,
        "steps": min(steps, 50),
        "sampler_index": sampler_index,
        "cfg_scale": 11,
        "width": wwwwww,
        "height": hhhhhh,
        "seed": seed
    }
    
    resp = requests.post(url="http://127.0.0.1:7861/sdapi/v1/txt2img", json=payload)
    # print("resp==>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]
    return processed














app = Ariadne(
    config(
        verify_key="ServiceVerifyKey",
        account=1209916110,
    ), log_config = LogConfig("INFO")
)


floatTxt2img = -1
floatCDCD = 20



@app.broadcast.receiver(GroupMessage)
async def group_message_listener(app: Ariadne, group: Group,  message: MessageChain, event:GroupMessage):

    global floatTxt2img
    global floatCDCD


    strCont = str(message)
    if "生成图" in strCont or "/ai text" in strCont:
        fNowTime = time.time()
        dtTime = fNowTime - floatTxt2img
        dtTime = int(dtTime)
        strCont = strCont.lower()
        if "nude" in strCont or "nipple" in strCont or "breast" in strCont or "pussy" in strCont or "nsfw" in strCont or "sex" in strCont or "ass" in strCont or "disrobe" in strCont:
            repl00 = MessageChain(At(event.sender.id), Plain("\n你想要色色?要我喊管理过来吗?"))
            return  app.send_message(group, repl00)
        if dtTime < floatCDCD:
            repl1 = MessageChain(At(event.sender.id), Plain("\n"+ str(floatCDCD)+" 秒CD一张图,等等再弄吧"+str(dtTime)))
            return  app.send_message(group, repl1)
        floatTxt2img = time.time()
        strSsss = strCont.replace("生成图", "")
        strSsss = strSsss.replace("/ai text", "")
        strSsss = strSsss.replace("，", ",")
        www = 960
        hhh = 512
        if "竖屏" in strCont:
            www = 512
            hhh = 960
        strSsss = strSsss.replace("竖屏", "")
        strSsss = strSsss.replace("横屏", "")
        
        repl2 = MessageChain(At(event.sender.id), Plain("\n收到,生成图片中,可能一分钟后成功...."))
        await app.send_message(group, repl2)

        img64 = txt2img(strSsss, wwwwww=www, hhhhhh=hhh)
        if len(strSsss) > 30:
            strSsss = strSsss[0 : 30]+"....."
        strRepl = "\n你要求的\n'"+strSsss+"'\n生成好了"
        repl3 = MessageChain(Image(base64 = img64), At(event.sender.id),Plain(strRepl))
        floatTxt2img = time.time()
        return  app.send_message(group, repl3)
    if "图生图" in strCont or "/ai image" in strCont:
        
        strCont = strCont.lower()
        if "nude" in strCont or "nipple" in strCont or "breast" in strCont or "pussy" in strCont or "nsfw" in strCont or "sex" in strCont or "ass" in strCont or "disrobe" in strCont:
            repl00 = MessageChain(At(event.sender.id), Plain("\n你想要色色?要我喊管理过来吗?"))
            return  app.send_message(group, repl00)

        imageArr = event.message_chain[Image]
        # print("=============>"+str(imageArr))
        if len(imageArr) == 1:
            strAlllll = ""
            strArr = event.message_chain[Plain]
            # print("=============>"+str(strArr))
            for strP in strArr:
                strAlllll += str(strP)
            # print("=======strAlllll======>" + strAlllll)
            strAlllll = strAlllll.replace("图生图", "")
            strAlllll = strAlllll.replace("/ai image", "")
            strUrlqq = imageArr[0].url
            # print("=======strUrlqq======> " + strUrlqq)
            html = toBase64(strUrlqq)

            repl2 = MessageChain(At(event.sender.id), Plain("\n收到,生成图片中,可能一分钟后成功...."))
            await app.send_message(group, repl2)
            img64 = img2img(html, strAlllll)
            strRepl = "\n你要求的\n'"+strAlllll+"'\n生成好了"
            repl3 = MessageChain(Image(base64 = img64), At(event.sender.id), Plain(strRepl))
            return  app.send_message(group, repl3)
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
            maxSize = max(imgTempSize) #图片的长边
            if maxSize > 1600:
                repl31 = MessageChain(At(event.sender.id), Plain("原图分辨率有边长超过1600,不再使用高清化"))
                return  app.send_message(group, repl31)
            strADB = "realesrgan-ncnn-vulkan.exe -i "+ strPathName +" -o output.png -n " + strRRRR
            os.system(strADB)
            strRepl = "\n画质提升好了,模型:"+ strRRRR +"\n点击查看原图看看效果\n默认使用真实世界模型\n发送'高清漫画'可以使用动漫专属模型"
            repl3 = MessageChain(Image(path = "output.png"), At(event.sender.id), Plain(strRepl))
            return  app.send_message(group, repl3)
            

    


Ariadne.launch_blocking()
