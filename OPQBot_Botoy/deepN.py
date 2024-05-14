
import io
import dlib
from SegCloth import segment_clothing
from transformers import pipeline

from hashlib import md5
import lama_cleaner
from pathlib import Path


from pathvalidate import sanitize_filepath
from io import BytesIO
import requests
import json
import time
import numpy as np
from PIL import ImageDraw, ImageFilter, ImageOps, ImageChops
from PIL import Image as ImagePIL
import base64
import cv2
from rembg import remove
from rembg.session_factory import new_session
import numpy as np
import random

curFileDir = Path(__file__).absolute().parent  # 当前文件路径


# 基础优化tag
basetag = "((best quality)), ((masterpiece)),((highres)), original, extremely detailed 8K wallpaper,"

# 基础排除tag
lowQuality = "((bra)),((belt)),((dress)),((pants)),((cloth)),cape,scarf,((bikini)),futa,multiple breasts,multiple nipples, (mutated hands and fingers:1.5 ), (long body :1.3),nsfw,logo,text,badhandv4,EasyNegative,ng_deepnegative_v1_75t,rev2-badprompt,verybadimagenegative_v1.3,negative_hand-neg,mutated hands and fingers,poorly drawn face,extra limb,missing limb,disconnected limbs,malformed hands,ugly, more than 2 nipples, missing nipples, different nipples, fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, gross proportions. short arm, (((missing arms))), missing thighs, missing calf, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts"
lowQuality22 = "nsfw,nude,naked,NSFW,nipple,pussy,futa,multiple breasts, (mutated hands and fingers:1.5 ), (long body :1.3),nsfw,logo,text,badhandv4,EasyNegative,ng_deepnegative_v1_75t,rev2-badprompt,verybadimagenegative_v1.3,negative_hand-neg,mutated hands and fingers,poorly drawn face,extra limb,missing limb,disconnected limbs,malformed hands,ugly, more than 2 nipples, missing nipples, different nipples, fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, gross proportions. short arm, (((missing arms))), missing thighs, missing calf, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts"

# lowQuality = "EasyNegative, muscular, (suntan:2), (sleeves:2), (tattoo:2), (sunglasses:2), (inverted nipples), (mutated:2), (worst quality:2), (low quality:2), (normal quality:2), lowres, blurry, ((nasolabial folds):1.2), 3d, anime, cartoon, cg, comic, drawing, bad detailed background, cropped, grayscale, jpeg artifacts, monochrome, non-linear background, out of frame, paintings, poorly drawn, semi-realistic, sepia, sketches, unclear architectural outline, asymmetric eyes, bad anatomy, cloned, crooked teeth, deformed, dehydrated, disfigured, double nipples, duplicate, extra arms, extra fingers, extra legs, extra limbs, long fingers, long neck, malformed limbs, missing arms, missing legs, missing teeth, more than five fingers on one hand:1.5, more than two arm per body:1.5, more than two leg per body:1.5, mutated, mutation, mutilated, odd eyes, ugly, (artist name:2), (logo:2), (text:2), (watermark:2), acnes, age spot, dark spots, fat, fused, giantess, glans, mole, obesity, skin blemishes, skin spots, animal ears, elf-ears, earrings, childish, morbid"

###########################################################################################################################


def base64_to_pillow(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = ImagePIL.open(image)
    return image


def image_to_base64(img, fmt='png'):
    output_buffer = BytesIO()
    img.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    # return f'data:image/{fmt};base64,' + base64_str
    return base64_str


def DrawRect(img: ImagePIL, face_rectangleArr, landmarkArr, bUseFace, bDeleteBG):
    # image_path = strPath
    # img = ImagePIL.open(image_path)
    # # img = ImagePIL.open("./test1.png")
    draw = ImageDraw.Draw(img)

    if bDeleteBG:
        wwwww = img.size[0]
        hhhhh = img.size[1]
        draw.rectangle([(0, 0),
                        (wwwww, hhhhh)], fill="white", outline="white", width=2)
    if not bUseFace:
        for face_rectangle in face_rectangleArr:
            left = face_rectangle['left'] - face_rectangle['width'] / 4
            trueLeft = left
            if left < 0:
                trueLeft = 0
            top = face_rectangle['top'] - face_rectangle['height'] / 1
            trueTop = top
            if top < 0:
                trueTop = 0
            width = face_rectangle['width'] * 1.25
            height = face_rectangle['height'] * 2
            # draw.rectangle([(trueLeft, trueTop),
            #                 (left+width, top+height)], fill="black", outline="black", width=2)
            draw.ellipse([(trueLeft, trueTop),
                          (left+width, top+height)], fill="black")
    else:
        # for landmark in landmarkArr:
        #     pointArr = []
        #     # print("landmark", landmark)
        #     for iii in landmark:
        #         pointArr.append([landmark[iii]["x"], landmark[iii]["y"]])
        for landmark in landmarkArr:
            pointArr = []
            # print("landmark", landmark)
            for n in range(0, 68):
                pointArr.append([landmark.part(n).x, landmark.part(n).y])
            hull = cv2.convexHull(np.array(pointArr))
            hhhh11 = hull.tolist()
            showPointArr = []
            for hhhh in hhhh11:
                showPointArr.append((hhhh[0][0], hhhh[0][1]))
            draw.polygon(showPointArr, fill="black", outline="black")

    strOutName = './faceout/'+'segmented-' + \
        str(time.time()) + str(random.randint(10000000, 111111111111111111))+"_00.png"
    img.save(strOutName)
    image_data = 'data:image/png;base64,' + image_to_base64(img)
    return strOutName, image_data


sss123123 = new_session("u2net_human_seg")


def ShiBieHUNUN(input):
    mask = remove(input, session=sss123123, only_mask=True, alpha_matting=True)
    # image_data = 'data:image/png;base64,' + image_to_base64(mask)
    image_data = image_to_base64(mask)
    return image_data


def ShiBiePeople(input) -> ImagePIL:
    mask = remove(input, session=sss123123,
                  only_mask=False, alpha_matting=True)
    # image_data = 'data:image/png;base64,' + image_to_base64(mask)
    # image_data = image_to_base64(mask)
    return mask


# 加载Dlib的人脸检测器和关键点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")  # 68点模型


def ShiBieHuman(strBase, bUseFace=False, bDeleteBG=False, imgININ=None):
    # http_urlface = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    # # key = "X5CYnsaJJCgMJXMPo9JGyHWfsqWx80gr"
    # # secret = "K1zHwlcl1RalyoLOH3vWLsouLDjPcl69"
    # key = "boI1KjcVhbhYdefReMRTnTpWilhF0LrH"  # 10000次正式的
    # secret = "lND9EZLv3G5vZrtRVdUi26V7JgIj_llf"
    # data222 = {
    #     "api_key": key,
    #     "api_secret": secret,
    #     "image_base64": strBase,
    #     'return_landmark': 2  # 2检测。返回 106 个人脸关键点。1检测。返回 83 个人脸关键点。0不检测
    # }
    # respface = requests.post(http_urlface, data=data222)
    # try:
    #     respfaceJSON = JSONDecoder().decode(respface.text)
    # except:
    #     print("ShiBieHuman======>", respface.text)
    #     return "MAX", "MAX", "MAX"

    image_data = base64.b64decode(strBase.split(',')[1])
    image = np.array(ImagePIL.open(BytesIO(image_data)))
    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用人脸检测器检测图像中的人脸
    faces = detector(gray)

    face_rectangleArr = []
    landmarkArr = []

    # 对每张检测到的人脸进行操作
    if faces:
        for face in faces:
            # 获取关键点
            landmarks = predictor(gray, face)
            landmarkArr.append(landmarks)
            # 绘制人脸矩形框
            face_rectangle = {
                "left": face.left(),
                "top": face.top(),
                "width": face.width(),
                "height": face.height()
            }
            face_rectangleArr.append(face_rectangle)

    # if respfaceJSON['faces']:
    #     nFacesNum = len(respfaceJSON['faces'])
    #     for i in range(nFacesNum):
    #         face_rectangle = respfaceJSON['faces'][i]['face_rectangle']
    #         landmark = respfaceJSON['faces'][i]['landmark']
    #         face_rectangleArr.append(face_rectangle)
    #         landmarkArr.append(landmark)

        strBBBBjjj = ShiBieHUNUN(imgININ)
        if strBBBBjjj:
            immm = base64_to_pillow(strBBBBjjj)
            strOutName, image_data = DrawRect(
                immm, face_rectangleArr, landmarkArr, bUseFace, bDeleteBG)
            return strOutName, image_data, ""
        else:
            return None, None, None
    else:
        return None, None, None


def img2imgAndMask(imgBase64, prompt, wwwww, height11, image_data, mask_blur, nCCType=2):
    payload = {
        "prompt": basetag + "," + prompt+", <lora:meinv123:0.7>,<lora:add_detail:0.7>, <lora:Grool LORA:0.6>, grool",
        "negative_prompt": lowQuality,
        "sampler_name": "DPM++ 2M SDE Karras",
        "sampler_index": "DPM++ 2M SDE Karras",
        "resize_mode": 2,
        "steps": 30,
        "cfg_scale": 10,
        "batch": 1,
        "width": wwwww,
        "height": height11,
        "init_images": [imgBase64],
        "mask":  image_data,
        "mask_blur": mask_blur,
        "mask_blur_x": mask_blur,
        "mask_blur_y": mask_blur,
        "seed": -1,  # 3690476257
        # 肤色问题 https://www.reddit.com/r/StableDiffusion/comments/1375wlb/inpainting_how_to_match_skin_tones/
        "denoising_strength": 0.92,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 64,
        "inpainting_fill": 1,
        "inpainting_mask_invert": 0,
        # "initial_noise_multiplier": 0.4,
        # "s_noise": 0.4,
        "alwayson_scripts": {
            "ControlNet": {
                "args": [
                    {
                        "input_image": imgBase64,
                        "model": "control_canny [9d312881]",
                        "module": "canny",
                        "weight": 1.2,
                        "lowvram": False,
                        "processor_res": 640,
                        "threshold_a": 150,
                        "threshold_b": 250,
                        "guidance": 1,
                        "guidance_start": 0,
                        "guidance_end": 1,
                        "pixel_perfect": True,
                        "control_mode": "Balanced",
                    },
                    {
                        "enabled": False,
                    },
                    {
                        "enabled": False,
                    },
                    {
                        "enabled": False,
                    },
                ]
            }
        }
    }
    if nCCType == 2:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_openpose [cab727d4]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "openpose_full"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1
    elif nCCType == 3:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11f1p_sd15_depth [cfd03158]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "depth_midas"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["lowvram"] = True

    elif nCCType == 4:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_softedge [a8575a2a]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "softedge_hed"

    elif nCCType == 5:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_scribble [d4ba51ff]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "scribble_hed"

    elif nCCType == 6:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_openpose [b46e25f5]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "openpose"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1
    elif nCCType == 7:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_seg [e1f51eb9]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "seg_ofcoco"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1

    elif nCCType == 8:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_inpaint [ebff9138]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "inpaint_global_harmonious"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1

    # print("payload==>", payload)

    resp = requests.post(
        # url="http://region-8.seetacloud.com:35202/sdapi/v1/img2img", json=payload)
        url="http://127.0.0.1:7860/sdapi/v1/img2img", json=payload)
    # print("resp=       ========== =>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]

    strPPP: str = prompt
    if (len(prompt) > 30):
        strPPP = prompt[0: 30]

    strPicName = strPPP + str(time.time()) + \
        str(random.randint(10000000, 111111111111111111))
    strName = sanitize_filepath(strPicName)
    # I assume you have a way of picking unique filenames
    filename = "./p2p/" + strName + '.png'
    imgdata = base64.b64decode(processed)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    return processed, filename


def img2imgAndMask22(imgBase64, prompt, wwwww, height11, image_data, mask_blur, nCCType=2):
    payload = {
        "prompt": basetag + "," + prompt+"",
        "negative_prompt": lowQuality22,
        "sampler_name": "DPM++ 2M SDE Karras",
        "sampler_index": "DPM++ 2M SDE Karras",
        "resize_mode": 2,
        "steps": 26,
        "cfg_scale": 7,
        "batch": 1,
        "width": wwwww,
        "height": height11,
        "init_images": [imgBase64],
        "mask":  image_data,
        "mask_blur": mask_blur,
        "mask_blur_x": mask_blur,
        "mask_blur_y": mask_blur,
        "seed": -1,  # 3690476257
        # 肤色问题 https://www.reddit.com/r/StableDiffusion/comments/1375wlb/inpainting_how_to_match_skin_tones/
        "denoising_strength": 1,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 64,
        "inpainting_fill": 1,
        "inpainting_mask_invert": 0,
        # "initial_noise_multiplier": 0.4,
        # "s_noise": 0.4,
        "alwayson_scripts": {
            "ControlNet": {
                "args": [
                    {
                        "input_image": imgBase64,
                        "model": "control_canny [9d312881]",
                        "module": "canny",
                        "weight": 1.2,
                        "lowvram": False,
                        "processor_res": 640,
                        "threshold_a": 150,
                        "threshold_b": 250,
                        "guidance": 1,
                        "guidance_start": 0,
                        "guidance_end": 1,
                        "pixel_perfect": True,
                        "control_mode": "Balanced",
                    },
                    {
                        "enabled": False,
                    },
                    {
                        "enabled": False,
                    },
                    {
                        "enabled": False,
                    },
                ]
            }
        }
    }
    if nCCType == 2:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_openpose [cab727d4]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "openpose_full"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1
    elif nCCType == 3:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11f1p_sd15_depth [cfd03158]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "depth_midas"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["lowvram"] = True

    elif nCCType == 4:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_softedge [a8575a2a]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "softedge_hed"

    elif nCCType == 5:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_scribble [d4ba51ff]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "scribble_hed"

    elif nCCType == 6:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_openpose [b46e25f5]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "openpose"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1
    elif nCCType == 7:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_seg [e1f51eb9]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "seg_ofcoco"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1

    elif nCCType == 8:
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["model"] = "control_v11p_sd15_inpaint [ebff9138]"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["module"] = "inpaint_global_harmonious"
        payload["alwayson_scripts"]["ControlNet"]["args"][0]["weight"] = 1

    # print("payload==>", payload)

    resp = requests.post(
        # url="http://region-8.seetacloud.com:35202/sdapi/v1/img2img", json=payload)
        url="http://127.0.0.1:7860/sdapi/v1/img2img", json=payload)
    # print("resp=       ========== =>"+str(resp))
    resp = resp.json()
    processed = resp["images"][0]

    strPPP: str = prompt
    if (len(prompt) > 30):
        strPPP = prompt[0: 30]

    strPicName = strPPP + str(time.time()) + \
        str(random.randint(10000000, 111111111111111111))
    strName = sanitize_filepath(strPicName)
    # I assume you have a way of picking unique filenames
    filename = "./p2p/" + strName + '.png'
    imgdata = base64.b64decode(processed)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    return processed, filename


# 局部重绘 v2 接口示例
host = "http://127.0.0.1:8888"


def inpaint_outpaint(params: dict) -> dict:
    response = requests.post(url=f"{host}/v2/generation/image-inpaint-outpaint",
                             data=json.dumps(params),
                             headers={"Content-Type": "application/json"})
    return response.json()


def fooocusimg2imgAndMask(imgBase64, image_data):
    imgBase64 = imgBase64.replace("data:image/png;base64,", "")
    image_data = image_data.replace("data:image/png;base64,", "")
    result = inpaint_outpaint(params={
        # "base_model_name": "halcyonSDXL_v13NSFW.safetensors",
        "base_model_name": "xxmix9realisticsdxl_v10.safetensors",
        "prompt": "nsfw,girl,(nude 1),pussy,breastes,nipple,xxmixgirl",
        "inpaint_additional_prompt": "nsfw,(nude 1),pussy,breastes,nipple",
        "input_image": imgBase64,
        "input_mask": image_data,
        "advanced_params": {
            "inpaint_disable_initial_latent": True,
            "inpaint_strength": 0.96,
        },
        "async_process": False})
    if result:
        url = result[0]["url"]

        return url


######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################


def ShiBieHUNUN222222222(input, outppp):
    mask = remove(input, session=sss123123, only_mask=True, alpha_matting=True)
    image_data = image_to_base64(mask)
    mask.save(outppp)
    return image_data


def GetNoManBG(inooo: str) -> str:
    outppp = inooo+"RESBG.png"

    imgININ = ImagePIL.open(inooo)
    ShiBieHUNUN222222222(imgININ, outppp)
    current_dir = Path(__file__).parent.absolute().resolve()
    save_dir = current_dir / 'flagged'
    Pathhhh = lama_cleaner.PPPPP(inooo, outppp, save_dir)
    return Pathhhh
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################
######################################################


def 外扩像素(image: ImagePIL) -> ImagePIL:
    border_width = 16
    image = image.convert('RGBA')
    gray_image = image.convert('L')
    contrast_enhanced_gray = ImageOps.autocontrast(gray_image)
    mask = contrast_enhanced_gray.point(lambda p: 255 if p > 128 else 0)
    mask = mask.convert('L')
    dilated_mask = mask.filter(ImageFilter.MaxFilter(border_width * 2 + 1))
    border_mask = ImageChops.difference(dilated_mask, mask)
    border_image = ImagePIL.new(
        'RGBA', image.size, (255, 255, 255, 255))  # solid yellow color
    final_image_with_border = ImagePIL.composite(
        border_image, image, border_mask)
    final_image_with_border = final_image_with_border.convert("RGBA")
    return final_image_with_border


# 人脸肤色


def detect_skin(image_path):
    # 加载人脸检测器
    detector = dlib.get_frontal_face_detector()
    # 加载图像
    image = cv2.imread(image_path)
    # 将图像转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 检测人脸
    faces = detector(gray_image)
    # 如果检测到人脸
    if len(faces) > 0:
        # 只取第一个检测到的人脸
        face = faces[0]
        # 提取人脸区域
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        face_roi = image[y:y+h, x:x+w]
        # 计算肤色区域的RGB值
        skin_color = cv2.mean(face_roi)
        skin_color_rgb = [int(skin_color[2]), int(
            skin_color[1]), int(skin_color[0])]
        return skin_color_rgb
    else:
        return [255, 238, 179]


def create_mask(image, radius=0, scale_factor=1, fuseMask=False, strOrgPath=None):
    # 打开图像文件
    # image = ImagePIL.open(image_path)
    # 转换图像为 RGBA 模式（如果不是的话）
    image = image.convert("RGBA")
    # 获取图像的像素数据
    data = image.getdata()
    # 创建一个新的像素列表，将透明区域变成黑色，其他区域变成白色
    new_data = []
    if fuseMask:
        if strOrgPath:
            skin_color_rgb = detect_skin(strOrgPath)
        for item in data:
            # 如果当前像素是完全透明的，则将其变成黑色
            if item[3] == 0:  # Alpha 通道为 0 表示完全透明
                new_data.append((0, 0, 0, 0))  # 透明
            else:
                new_data.append(
                    (skin_color_rgb[0], skin_color_rgb[1], skin_color_rgb[2], 255))  # 脸部的肤色
    else:
        for item in data:
            # 如果当前像素是完全透明的，则将其变成黑色
            if item[3] == 0:  # Alpha 通道为 0 表示完全透明
                new_data.append((0, 0, 0, 255))  # 黑色
            else:
                new_data.append((255, 255, 255, 255))  # 白色
    # 创建一个新的图像并将像素数据加载到其中
    mask_image = ImagePIL.new("RGBA", image.size)
    mask_image.putdata(new_data)
    # 使用高斯模糊对图像进行边缘平滑处理
    smoothed_mask = mask_image.filter(ImageFilter.GaussianBlur(radius))

    # 找到白色区域的边界框
    bbox = smoothed_mask.getbbox()
    # 放大白色区域
    if bbox:
        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top
        enlarged_bbox = (left - int((scale_factor - 1) * width / 2),
                         top - int((scale_factor - 1) * height / 2),
                         right + int((scale_factor - 1) * width / 2),
                         bottom + int((scale_factor - 1) * height / 2))
        # 创建一个空白的图像
        enlarged_mask = ImagePIL.new("RGBA", mask_image.size)
        # 将放大的白色区域合并到空白图像中
        enlarged_mask.paste(smoothed_mask.crop(bbox).resize(
            (enlarged_bbox[2] - enlarged_bbox[0], enlarged_bbox[3] - enlarged_bbox[1])), enlarged_bbox)
        # 将原始图像与放大的区域合并
        result_image = ImagePIL.alpha_composite(image, enlarged_mask)
    else:
        result_image = image
    return result_image


# sss = new_session("u2net_cloth_seg")

# 假设您的本地模型路径如下
local_model_path = "./mattmdjaga/segformer_b2_clothes"
# 使用本地模型初始化Segmentation Pipeline
segmenter = pipeline("image-segmentation", model=local_model_path)
# segmenter = pipeline(model="mattmdjaga/segformer_b2_clothes")


def ShiBieCloth(input):
    mask = remove(input, session=sss, only_mask=True, alpha_matting=True)
    cloth_seg_masks = np.split(np.array(mask), 3, axis=0)
    outImage = ImagePIL.fromarray(
        np.sum(cloth_seg_masks, axis=0).astype(np.uint8)).convert("L")

    image_data = 'data:image/png;base64,' + image_to_base64(outImage)
    outImage.save("./facein/cloth_"+str(time.time())+".png")
    return image_data


def ShiBieClothNew(input, image_in_path):
    result = segment_clothing(img=input, segmenter=segmenter)
    result.save('123.png')
    outImage = create_mask(result)
    outImage2 = 外扩像素(outImage)
    outImageFSMask = create_mask(result, 0, 1, True, image_in_path)
    image_data = 'data:image/png;base64,' + image_to_base64(outImage2)
    tttttt = str(time.time())
    strOutName = "./facein/cloth_"+tttttt+".png"
    outImage2.save(strOutName)
    return strOutName, image_data, outImageFSMask

######################################################

######################################################################


def checkStrisCN(strCn: str):
    if len(strCn) > 0:
        for ch in strCn:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
    return False


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def FanyiCNToEn(strCn: str):
    strAAA = strCn

    # Set your own appid/appkey.
    appid = '20230810001775819'
    appkey = '9YGgHTMU5UO8_HGelRXx'
    from_lang = 'auto'
    to_lang = 'en'
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + strCn + str(salt) + appkey)

    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': strCn, 'from': from_lang,
                   'to': to_lang, 'salt': salt, 'sign': sign}
        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        strAAA = result["trans_result"][0]["dst"]
    except BaseException as eeee:
        print("翻译错误" + str(eeee))
        return strAAA
    return strAAA

#nude
def NudeOnePerson(image_in_path: str, strPromoto: str):
    imgININ = ImagePIL.open(image_in_path)
    strBase64Org = "data:image/png;base64," + \
        image_to_base64(imgININ)
    # strBase64Org = "data:image/png;base64," + downloaded_file
    bUseFace = False
    bUseCloth = True
    bShowMask = False
    bMaskPureColor = False
    bUseDick = False
    bDelectBG = False
    if strPromoto and ("识别面部" in strPromoto):
        strPromoto = strPromoto.replace("识别面部 ", "")
        strPromoto = strPromoto.replace("识别面部", "")
        bUseFace = True
        bUseCloth = False
    if strPromoto and ("识别衣服" in strPromoto):
        strPromoto = strPromoto.replace("识别衣服 ", "")
        strPromoto = strPromoto.replace("识别衣服", "")
        bUseCloth = True
    if strPromoto and ("旧算法" in strPromoto):
        strPromoto = strPromoto.replace("旧算法 ", "")
        strPromoto = strPromoto.replace("旧算法", "")
        bUseCloth = False
    if strPromoto and ("显示遮罩" in strPromoto):
        strPromoto = strPromoto.replace("显示遮罩 ", "")
        strPromoto = strPromoto.replace("显示遮罩", "")
        bShowMask = True
    if strPromoto and ("纯色" in strPromoto):
        strPromoto = strPromoto.replace("纯色 ", "")
        strPromoto = strPromoto.replace("纯色", "")
        bMaskPureColor = True
    if strPromoto and ("删除背景" in strPromoto):
        strPromoto = strPromoto.replace("删除背景 ", "")
        strPromoto = strPromoto.replace("删除背景", "")
        bDelectBG = True
        bUseCloth = False

    image_data = None
    strOutName = ""
    bTank = False
    nMaskB = 1
    outImageFSMask = None
    if not bUseCloth:
        try:
            if bDelectBG:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bDelectBG, imgININ)
            else:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bUseDick, imgININ)
        except BaseException as eee:
            print("识别面部错误!!!!!!!!!!!!====>", eee)
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
        if image_data == "MAX":
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
    else:
        strOutName, image_data, outImageFSMask = ShiBieClothNew(
            imgININ, image_in_path)
        nMaskB = 8

    if image_data:
        useCustom = False
        strAlllll = "NSFW,nsfw,(naked 1.5),(nude girl 1.5),(no cloth 2),breasts,pussy,pink nipples,"
        strAlllll2222 = ""

        nCCtype = 2
        if strPromoto and len(strPromoto) >= 1:
            try:
                nMaskB = int(strPromoto)
                if (nMaskB <= 0):
                    nMaskB = 0
                if nMaskB > 64:
                    nMaskB = 64
            except BaseException:
                if len(strPromoto) > 1:
                    if checkStrisCN(strPromoto):
                        strPromoto = FanyiCNToEn(strPromoto)
                    strAlllll += strPromoto
                    useCustom = True
                else:
                    strAlllll = strAlllll + strAlllll2222
            print("额外关键词===>", strPromoto)
        else:
            strAlllll = strAlllll + strAlllll2222

        if bUseDick:
            strAlllll += ",<lora:posingWithBBC_v10:0.8>, woman posing with big bbc penis"
        bCan = True
        if bCan:
            resultPath = ""
            try:
                if True:
                    resultPath22 = ""
                    urlFFFFF = ""

                    strBBBB = strBase64Org.replace(
                        "data:image/png;base64,", "")
                    immm = base64_to_pillow(strBBBB)

                    if outImageFSMask and bMaskPureColor:
                        x, y = outImageFSMask.size
                        immm.paste(outImageFSMask, box=(
                            0, 0, x, y), mask=outImageFSMask)
                        immm.save("tempMask.png")
                        strBase64Org = "data:image/png;base64," + \
                            image_to_base64(immm)

                    imgTempSize = immm.size
                    www = 1024
                    hhh = 720
                    if imgTempSize[0] < imgTempSize[1]:
                        www = 720
                        hhh = 1024
                    img64, resultPath22 = img2imgAndMask(
                        strBase64Org, strAlllll, www, hhh, image_data, nMaskB, nCCtype)
                    return img64, resultPath22
                    # if not bUseCloth:
                    #     res1111 = ImagePIL.open(resultPath22)
                    #     noBGMan = ShiBiePeople(res1111)
                    #     strBGBG = GetNoManBG(image_in_path)
                    #     # print("image_in_path=>", image_in_path, strBGBG)
                    #     new_image = ImagePIL.open(strBGBG)
                    #     no_bg_image = noBGMan
                    #     x, y = no_bg_image.size
                    #     new_image.paste(no_bg_image, box=(
                    #         0, 0, x, y), mask=no_bg_image)
                    #     new_image.save("./p2p/IIIIII.png")

                    #     return new_image, "./p2p/IIIIII.png"
                    # else:
                    #     return img64, resultPath22
            except:
                return 0, 0

    return 0, 0

#bikini
def NudeOnePerson22(image_in_path: str, strPromoto: str):
    imgININ = ImagePIL.open(image_in_path)
    strBase64Org = "data:image/png;base64," + \
        image_to_base64(imgININ)
    # strBase64Org = "data:image/png;base64," + downloaded_file
    bUseFace = False
    bUseCloth = True
    bShowMask = False
    bMaskPureColor = False
    bUseDick = False
    bDelectBG = False
    if strPromoto and ("识别面部" in strPromoto):
        strPromoto = strPromoto.replace("识别面部 ", "")
        strPromoto = strPromoto.replace("识别面部", "")
        bUseFace = True
        bUseCloth = False
    if strPromoto and ("识别衣服" in strPromoto):
        strPromoto = strPromoto.replace("识别衣服 ", "")
        strPromoto = strPromoto.replace("识别衣服", "")
        bUseCloth = True
    if strPromoto and ("旧算法" in strPromoto):
        strPromoto = strPromoto.replace("旧算法 ", "")
        strPromoto = strPromoto.replace("旧算法", "")
        bUseCloth = False
    if strPromoto and ("显示遮罩" in strPromoto):
        strPromoto = strPromoto.replace("显示遮罩 ", "")
        strPromoto = strPromoto.replace("显示遮罩", "")
        bShowMask = True
    if strPromoto and ("纯色" in strPromoto):
        strPromoto = strPromoto.replace("纯色 ", "")
        strPromoto = strPromoto.replace("纯色", "")
        bMaskPureColor = True
    if strPromoto and ("删除背景" in strPromoto):
        strPromoto = strPromoto.replace("删除背景 ", "")
        strPromoto = strPromoto.replace("删除背景", "")
        bDelectBG = True
        bUseCloth = False

    image_data = None
    strOutName = ""
    bTank = False
    nMaskB = 1
    outImageFSMask = None
    if not bUseCloth:
        try:
            if bDelectBG:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bDelectBG, imgININ)
            else:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bUseDick, imgININ)
        except BaseException as eee:
            print("识别面部错误!!!!!!!!!!!!====>", eee)
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
        if image_data == "MAX":
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
    else:
        strOutName, image_data, outImageFSMask = ShiBieClothNew(
            imgININ, image_in_path)
        nMaskB = 8

    if image_data:
        useCustom = False
        # <lora:Mk_kzy_v1.1:0.86>,<lora:Slingshot_AllLayer:0.2>
        # strAlllll = "swimsuit,bikini,<lora:Mk_kzy_v1.1:0.6>,"
        strAlllll = "swimsuit,bikini,underwear"

        nCCtype = 2
        if strPromoto and len(strPromoto) >= 1:
            try:
                nMaskB = int(strPromoto)
                if (nMaskB <= 0):
                    nMaskB = 0
                if nMaskB > 64:
                    nMaskB = 64
            except BaseException:
                if len(strPromoto) > 1:
                    if checkStrisCN(strPromoto):
                        strPromoto = FanyiCNToEn(strPromoto)
                    strAlllll += ("(" + strPromoto+" 1.3)")
                    useCustom = True
                else:
                    strAlllll = strAlllll
            print("额外关键词===>", strPromoto)
        else:
            strAlllll = strAlllll

        bCan = True
        if bCan:
            resultPath = ""
            try:
                if True:
                    resultPath22 = ""
                    urlFFFFF = ""

                    strBBBB = strBase64Org.replace(
                        "data:image/png;base64,", "")
                    immm = base64_to_pillow(strBBBB)

                    if outImageFSMask and bMaskPureColor:
                        x, y = outImageFSMask.size
                        immm.paste(outImageFSMask, box=(
                            0, 0, x, y), mask=outImageFSMask)
                        immm.save("tempMask.png")
                        strBase64Org = "data:image/png;base64," + \
                            image_to_base64(immm)

                    imgTempSize = immm.size
                    www = 1024
                    hhh = 720
                    if imgTempSize[0] < imgTempSize[1]:
                        www = 720
                        hhh = 1024
                    img64, resultPath22 = img2imgAndMask22(
                        strBase64Org, strAlllll, www, hhh, image_data, nMaskB, nCCtype)
                    return img64, resultPath22
                    # if not bUseCloth:
                    #     res1111 = ImagePIL.open(resultPath22)
                    #     noBGMan = ShiBiePeople(res1111)
                    #     strBGBG = GetNoManBG(image_in_path)
                    #     # print("image_in_path=>", image_in_path, strBGBG)
                    #     new_image = ImagePIL.open(strBGBG)
                    #     no_bg_image = noBGMan
                    #     x, y = no_bg_image.size
                    #     new_image.paste(no_bg_image, box=(
                    #         0, 0, x, y), mask=no_bg_image)
                    #     new_image.save("./p2p/IIIIII.png")
                    #     return new_image, "./p2p/IIIIII.png"
                    # else:
                    #     return img64, resultPath22
            except:
                return 0, 0

    return 0, 0

#jk
def NudeOnePerson33(image_in_path: str, strPromoto: str):
    # strPromoto += "旧算法"
    imgININ = ImagePIL.open(image_in_path)
    strBase64Org = "data:image/png;base64," + \
        image_to_base64(imgININ)
    # strBase64Org = "data:image/png;base64," + downloaded_file
    bUseFace = False
    bUseCloth = True
    bShowMask = False
    bMaskPureColor = False
    bUseDick = False
    bDelectBG = False
    if strPromoto and ("识别面部" in strPromoto):
        strPromoto = strPromoto.replace("识别面部 ", "")
        strPromoto = strPromoto.replace("识别面部", "")
        bUseFace = True
        bUseCloth = False
    if strPromoto and ("识别衣服" in strPromoto):
        strPromoto = strPromoto.replace("识别衣服 ", "")
        strPromoto = strPromoto.replace("识别衣服", "")
        bUseCloth = True
    if strPromoto and ("旧算法" in strPromoto):
        strPromoto = strPromoto.replace("旧算法 ", "")
        strPromoto = strPromoto.replace("旧算法", "")
        bUseCloth = False
    if strPromoto and ("显示遮罩" in strPromoto):
        strPromoto = strPromoto.replace("显示遮罩 ", "")
        strPromoto = strPromoto.replace("显示遮罩", "")
        bShowMask = True
    if strPromoto and ("纯色" in strPromoto):
        strPromoto = strPromoto.replace("纯色 ", "")
        strPromoto = strPromoto.replace("纯色", "")
        bMaskPureColor = True
    if strPromoto and ("删除背景" in strPromoto):
        strPromoto = strPromoto.replace("删除背景 ", "")
        strPromoto = strPromoto.replace("删除背景", "")
        bDelectBG = True
        bUseCloth = False

    image_data = None
    strOutName = ""
    bTank = False
    nMaskB = 1
    outImageFSMask = None
    if not bUseCloth:
        try:
            if bDelectBG:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bDelectBG, imgININ)
            else:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bUseDick, imgININ)
        except BaseException as eee:
            print("识别面部错误!!!!!!!!!!!!====>", eee)
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
        if image_data == "MAX":
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
    else:
        strOutName, image_data, outImageFSMask = ShiBieClothNew(
            imgININ, image_in_path)
        nMaskB = 8

    if image_data:
        useCustom = False
        strAlllll = "school Uniform,,JK_style,short-sleeved JK_shirt,JK_suit, <lora:jk uniform:0.7>,"
        strAlllll2222 = ""

        nCCtype = 2
        if strPromoto and len(strPromoto) >= 1:
            try:
                nMaskB = int(strPromoto)
                if (nMaskB <= 0):
                    nMaskB = 0
                if nMaskB > 64:
                    nMaskB = 64
            except BaseException:
                if len(strPromoto) > 1:
                    if checkStrisCN(strPromoto):
                        strPromoto = FanyiCNToEn(strPromoto)
                    strAlllll += strPromoto
                    useCustom = True
                else:
                    strAlllll = strAlllll + strAlllll2222
            print("额外关键词===>", strPromoto)
        else:
            strAlllll = strAlllll + strAlllll2222

        bCan = True
        if bCan:
            resultPath = ""
            try:
                if True:
                    resultPath22 = ""
                    urlFFFFF = ""

                    strBBBB = strBase64Org.replace(
                        "data:image/png;base64,", "")
                    immm = base64_to_pillow(strBBBB)

                    if outImageFSMask and bMaskPureColor:
                        x, y = outImageFSMask.size
                        immm.paste(outImageFSMask, box=(
                            0, 0, x, y), mask=outImageFSMask)
                        immm.save("tempMask.png")
                        strBase64Org = "data:image/png;base64," + \
                            image_to_base64(immm)

                    imgTempSize = immm.size
                    www = 1024
                    hhh = 720
                    if imgTempSize[0] < imgTempSize[1]:
                        www = 720
                        hhh = 1024
                    img64, resultPath22 = img2imgAndMask22(
                        strBase64Org, strAlllll, www, hhh, image_data, nMaskB, nCCtype)
                    # if not bUseCloth:
                    #     res1111 = ImagePIL.open(resultPath22)
                    #     noBGMan = ShiBiePeople(res1111)
                    #     strBGBG = GetNoManBG(image_in_path)
                    #     # print("image_in_path=>", image_in_path, strBGBG)
                    #     new_image = ImagePIL.open(strBGBG)
                    #     no_bg_image = noBGMan
                    #     x, y = no_bg_image.size
                    #     new_image.paste(no_bg_image, box=(
                    #         0, 0, x, y), mask=no_bg_image)
                    #     new_image.save("./p2p/IIIIII.png")
                    #     return new_image, "./p2p/IIIIII.png"
                    # else:
                    #     return img64, resultPath22
                    return img64, resultPath22
            except:
                return 0, 0

    return 0, 0

#hanfu
def NudeOnePerson44(image_in_path: str, strPromoto: str):
    # strPromoto += "旧算法"
    imgININ = ImagePIL.open(image_in_path)
    strBase64Org = "data:image/png;base64," + \
        image_to_base64(imgININ)
    # strBase64Org = "data:image/png;base64," + downloaded_file
    bUseFace = False
    bUseCloth = True
    bShowMask = False
    bMaskPureColor = False
    bUseDick = False
    bDelectBG = False
    if strPromoto and ("识别面部" in strPromoto):
        strPromoto = strPromoto.replace("识别面部 ", "")
        strPromoto = strPromoto.replace("识别面部", "")
        bUseFace = True
        bUseCloth = False
    if strPromoto and ("旧算法" in strPromoto):
        strPromoto = strPromoto.replace("旧算法 ", "")
        strPromoto = strPromoto.replace("旧算法", "")
        bUseCloth = False
    if strPromoto and ("显示遮罩" in strPromoto):
        strPromoto = strPromoto.replace("显示遮罩 ", "")
        strPromoto = strPromoto.replace("显示遮罩", "")
        bShowMask = True
    if strPromoto and ("纯色" in strPromoto):
        strPromoto = strPromoto.replace("纯色 ", "")
        strPromoto = strPromoto.replace("纯色", "")
        bMaskPureColor = True
    if strPromoto and ("汉服" in strPromoto):
        bMaskPureColor = True
        # bUseFace = True
        bUseCloth = True
    if strPromoto and ("识别衣服" in strPromoto):
        strPromoto = strPromoto.replace("识别衣服 ", "")
        strPromoto = strPromoto.replace("识别衣服", "")
        bUseCloth = True
    if strPromoto and ("删除背景" in strPromoto):
        strPromoto = strPromoto.replace("删除背景 ", "")
        strPromoto = strPromoto.replace("删除背景", "")
        bDelectBG = True
        bUseCloth = False

    image_data = None
    strOutName = ""
    bTank = False
    nMaskB = 1
    outImageFSMask = None

    if not bUseCloth:
        try:
            if bDelectBG:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bDelectBG, imgININ)
            else:
                strOutName, image_data, strName2 = ShiBieHuman(
                    strBase64Org, bUseFace, bUseDick, imgININ)
        except BaseException as eee:
            print("识别面部错误!!!!!!!!!!!!====>", eee)
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
        if image_data == "MAX":
            strOutName, image_data, outImageFSMask = ShiBieClothNew(
                imgININ, image_in_path)
            nMaskB = 8
    else:
        strOutName, image_data, outImageFSMask = ShiBieClothNew(
            imgININ, image_in_path)
        nMaskB = 8

    if image_data:
        useCustom = False
        strAlllll = "school Uniform,,JK_style,short-sleeved JK_shirt,JK_suit, <lora:jk uniform:0.7>,"

        nCCtype = 2

        if strPromoto and ("汉服" in strPromoto):
            strPromoto = strPromoto.replace("汉服", "", 1)
            if len(strPromoto) > 1 and checkStrisCN(strPromoto):
                strPromoto = FanyiCNToEn(strPromoto)
            strAlllll = "<lora:hanfu40-beta-3:0.88>,hanfu,tang style," + strPromoto
        else:
            if strPromoto and len(strPromoto) >= 1:
                if checkStrisCN(strPromoto):
                    strPromoto = FanyiCNToEn(strPromoto)
                strAlllll = strPromoto
                useCustom = True
            else:
                strAlllll = strAlllll

        print("关键词===>", strAlllll)

        bCan = True
        if bCan:
            resultPath = ""
            try:
                if True:
                    resultPath22 = ""
                    urlFFFFF = ""

                    strBBBB = strBase64Org.replace(
                        "data:image/png;base64,", "")
                    immm = base64_to_pillow(strBBBB)

                    if outImageFSMask and bMaskPureColor:
                        x, y = outImageFSMask.size
                        immm.paste(outImageFSMask, box=(
                            0, 0, x, y), mask=outImageFSMask)
                        immm.save("tempMask.png")
                        strBase64Org = "data:image/png;base64," + \
                            image_to_base64(immm)

                    imgTempSize = immm.size
                    www = 1024
                    hhh = 720
                    if imgTempSize[0] < imgTempSize[1]:
                        www = 720
                        hhh = 1024
                    img64, resultPath22 = img2imgAndMask22(
                        strBase64Org, strAlllll, www, hhh, image_data, nMaskB, nCCtype)
                    if not bUseCloth and bDelectBG:
                        res1111 = ImagePIL.open(resultPath22)
                        noBGMan = ShiBiePeople(res1111)
                        strBGBG = GetNoManBG(image_in_path)
                        new_image = ImagePIL.open(strBGBG)
                        no_bg_image = noBGMan
                        x, y = no_bg_image.size
                        
                        print("no_bg_image.size, new_image.size =>   ",  no_bg_image.size, new_image.size)
                        
                        new_image.paste(no_bg_image, box=(
                            0, 0, x, y), mask=no_bg_image)
                        new_image.save("./p2p/IIIIII.png")           
                        # 将图像保存到字节流
                        buffered = io.BytesIO()
                        new_image.save(buffered, format="PNG")  # 指定图像格式
                        # 将字节流转换为Base64字符串
                        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        return img_str, "./p2p/IIIIII.png"
                    else:
                        return img64, resultPath22
                    return img64, resultPath22
            except:
                return 0, 0

    return 0, 0




def NudeOnePersonFooocus(image_in_path: str):
    imgININ = ImagePIL.open(image_in_path)
    strBase64Org = "data:image/png;base64," + image_to_base64(imgININ)
    strOutName, image_data, outImageFSMask = ShiBieClothNew(imgININ, image_in_path)
    if image_data!=None:
        url = fooocusimg2imgAndMask(strBase64Org, image_data)
        return url