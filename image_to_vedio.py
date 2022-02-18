import cv2
import os


def convert(frames_dir, frames):
    video_name = "output.avi"
    frame = cv2.imread(os.path.join(frames_dir, frames[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    for image in frames:
        video.write(cv2.imread(os.path.join(frames_dir, image)))
    cv2.destroyAllWindows()
    video.release()


def convert_image_to_video(frames_dir_path):
    frames = os.listdir(frames_dir_path)
    frames.sort()
    # print(frames)
    convert(frames_dir_path, frames)
