import cv2
import os
import shutil
from PIL import Image

def resize_image(image_path):
    basewidth = 300

    img = Image.open(image_path)

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(image_path)
    return True


def check_directory_exists(save_file_directory):
    if os.path.isdir(os.path.join(os.getcwd(), save_file_directory)):
       shutil.rmtree(os.path.join(os.getcwd(), save_file_directory))
    os.mkdir(os.path.join(os.getcwd(), save_file_directory))


def getFrame(sec, count, vidcap, save_file_directory):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite(save_file_directory +"/image" + str(count) + ".jpg", image)
        resize_image(save_file_directory +"/image" + str(count) + ".jpg")# save frame as JPG file
    return hasFrames


def convert_video_to_image(filepath, save_file_directory):
    vidcap = cv2.VideoCapture(filepath)
    sec = 0
    frameRate = 1  # //it will capture image in each 0.5 second
    count = 0
    countstr = format(count, '05d')
    success = getFrame(sec=sec, count=countstr, vidcap=vidcap, save_file_directory=save_file_directory)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        countstr = format(count, '05d')
        success = getFrame(sec=sec, count=countstr, vidcap=vidcap, save_file_directory=save_file_directory)


def execute(video_file_path, save_file_directory):
    check_directory_exists(save_file_directory)
    convert_video_to_image(video_file_path, save_file_directory)
