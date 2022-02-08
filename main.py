import os.path

from video_to_image import execute as video_2_image_executor
from process_frames import process_frames
from image_to_vedio import convert_image_to_video

def main():
    video_2_image_executor("data/test_1.mp4", "target_frames")
    video_2_image_executor("data/test_1.mp4", "source_frames")
    # process_frames(os.path.join(os.getcwd(), "source_frames"), os.path.join(os.getcwd(), "target_frames"))
    #convert_image_to_video("target_frames")

if __name__ == "__main__":
    main()
