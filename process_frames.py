import os

import numpy as np
from PIL import Image, ImageOps
import hashlib
from itentify_forged_region import identify_and_highlight


def make_image_hash(image_path):
    im = np.array(Image.open(image_path).convert('L'))
    result = hashlib.md5(im.astype('uint8'))
    return result.hexdigest()


def compare_frames(source_frame_path, target_frame_path):
    source_frame_hash = make_image_hash(source_frame_path)
    target_frame_hash = make_image_hash(target_frame_path)

    if source_frame_hash != target_frame_hash:
        print("False")
        identify_and_highlight(source_frame_path, target_frame_path)
    else:
        print("True")


def process_frames(source_frames_path, target_frames_path):
    source_frames_img = os.listdir(source_frames_path)
    target_frames_img = os.listdir(target_frames_path)
    source_frames_img.sort()
    target_frames_img.sort()
    for source_image, target_image in zip(source_frames_img, target_frames_img):
        compare_frames(os.path.join(source_frames_path, source_image), os.path.join(target_frames_path, target_image))
