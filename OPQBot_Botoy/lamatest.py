
from pathlib import Path
from io import BytesIO
from PIL import Image as ImagePIL
import base64
from rembg import remove
from rembg.session_factory import new_session
import lama_cleaner


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
    return base64_str



sss123123 = new_session("u2net_human_seg")
def ShiBieHUNUN(input):
    mask = remove(input, session=sss123123, only_mask=False, alpha_matting=True)
    image_data = image_to_base64(mask)
    mask.save(outppp)
    return image_data



inooo = "./test.png"
outppp = "./1111111.png"

imgININ = ImagePIL.open(inooo)
ShiBieHUNUN(imgININ)


current_dir = Path(__file__).parent.absolute().resolve()
save_dir = current_dir / 'flagged'
lama_cleaner.PPPPP(inooo, outppp, save_dir)

