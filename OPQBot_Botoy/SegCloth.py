
from PIL import Image
import numpy as np


# Initialize segmentation pipeline


def segment_clothing(img, segmenter,clothes= ["Upper-clothes", "Skirt", "Pants", "Dress", "Belt",  "Scarf", "Bra"]):
    # Segment image
    segments = segmenter(img)

    # Create list of masks
    mask_list = []
    for s in segments:
        # print("         ", s['label'])
        if(s['label'] in clothes):
            mask_list.append(s['mask'])
            
    # Paste all masks on top of eachother 
    final_mask = np.array(mask_list[0])
    for mask in mask_list:
        current_mask = np.array(mask)
        final_mask = final_mask + current_mask
            
    # Convert final mask from np array to PIL image
    final_mask = Image.fromarray(final_mask)

    # Apply mask to original image
    img.putalpha(final_mask)

    return img