import cv2
import os
import shutil


def check_directory_exists(save_file_directory):
    if os.path.isdir(os.path.join(os.getcwd(), save_file_directory)):
       shutil.rmtree(os.path.join(os.getcwd(), save_file_directory))
    os.mkdir(os.path.join(os.getcwd(), save_file_directory))


def getFrame(sec, count, vidcap, save_file_directory):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite(save_file_directory +"/image" + str(count) + ".jpg", image)  # save frame as JPG file
    return hasFrames


def convert_video_to_image(filepath, save_file_directory):
    vidcap = cv2.VideoCapture(filepath)
    sec = 0
    frameRate = 1  # //it will capture image in each 0.5 second
    count = 0
    success = getFrame(sec=sec, count=count, vidcap=vidcap, save_file_directory=save_file_directory)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec=sec, count=count, vidcap=vidcap, save_file_directory=save_file_directory)


def execute(video_file_path, save_file_directory):
    check_directory_exists(save_file_directory)
    convert_video_to_image(video_file_path, save_file_directory)
