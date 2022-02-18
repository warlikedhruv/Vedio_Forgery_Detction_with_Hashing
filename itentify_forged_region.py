import os
from PIL import Image
import image_slicer
from pathlib import Path
import numpy as np
import hashlib
from PIL import Image, ImageOps
import cv2

source_image_path = None
target_image_path = None

common_image_tiles_path = os.path.join(os.getcwd(), 'image_tiles')


def create_or_remove_tiles_dir(directory_name):
    directory_path = os.path.join('image_tiles', directory_name)
    if os.path.isdir(directory_path):
        [f.unlink() for f in Path(directory_path).glob("*") if f.is_file()]
    else:
        os.mkdir(directory_path)


def resize_image(image_path):
    basewidth = 300

    img = Image.open(image_path)

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(image_path)
    return True


def make_image_tiles(image_path, directory_name):
    img_format = ".jpg"

    directory_path = os.path.join(common_image_tiles_path, directory_name)

    image_tiles = image_slicer.slice(image_path, 25, save=False)
    image_slicer.save_tiles(image_tiles, directory=directory_path, prefix='slice')

    return True


def generate_hash_list_of_tiles(tiles_directory_name):
    tiles_directory = os.path.join(common_image_tiles_path, tiles_directory_name)
    files_list = os.listdir(tiles_directory)
    files_list.sort()

    hash_result = []
    for file in files_list:
        im = np.array(
            Image.open(tiles_directory + '/' + file).convert('L'))

        result = hashlib.md5(im.astype('uint8'))
        hash_result.append(result.hexdigest())

    return hash_result


def hash_compare_and_highlight(source_image_tiles_hash, target_image_tiles_hash, target_tiles_dir):
    tiles_directory = os.path.join(common_image_tiles_path, target_tiles_dir)
    target_image_tiles_paths = os.listdir(tiles_directory)
    target_image_tiles_paths.sort()
    # print(target_image_tiles_paths)
    COUNTER = 0
    # print(target_image_tiles_paths)
    # print(source_image_tiles_hash)
    # print(target_image_tiles_hash)
    for source_image_hash, target_image_hash in zip(source_image_tiles_hash, target_image_tiles_hash):
        if source_image_hash != target_image_hash:
            # img = Image.open(tiles_directory + "/" + target_image_tiles_paths[COUNTER])
            img = cv2.imread(tiles_directory + "/" + target_image_tiles_paths[COUNTER])
            dimensions = img.shape
            # img_with_border = ImageOps.expand(img, border=1, fill='green')
            # img_with_border = img_with_border.resize((width, height), Image.ANTIALIAS)
            # img_with_border.save(tiles_directory + "/" + target_image_tiles_paths[COUNTER])
            cv2.rectangle(img, (0, 0), (dimensions[1]-1, dimensions[0]-1), (0, 255, 0), 1)
            cv2.imwrite(tiles_directory + "/" + target_image_tiles_paths[COUNTER], img)
            # cv2.imshow('image', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        COUNTER += 1

    joined = image_slicer.open_images_in(tiles_directory)
    join = image_slicer.join(joined)

    rgb_im = join.convert('RGB')
    rgb_im.save(target_image_path)


def identify_and_highlight(source_frame_path, target_frame_path):
    global source_image_path, target_image_path

    source_image_path = source_frame_path
    target_image_path = target_frame_path

    resize_image(source_image_path)
    resize_image(target_image_path)

    source_tiles_dir_name = "source_" + source_frame_path.split("/")[-1].split(".", 1)[0]
    target_tiles_dir_name = "target_" + source_frame_path.split("/")[-1].split(".", 1)[0]

    create_or_remove_tiles_dir(source_tiles_dir_name)
    create_or_remove_tiles_dir(target_tiles_dir_name)

    make_image_tiles(source_image_path, source_tiles_dir_name)
    make_image_tiles(target_frame_path, target_tiles_dir_name)

    source_image_tiles_hash = generate_hash_list_of_tiles(source_tiles_dir_name)
    target_image_tiles_hash = generate_hash_list_of_tiles(target_tiles_dir_name)

    hash_compare_and_highlight(source_image_tiles_hash, target_image_tiles_hash, target_tiles_dir_name)



def main():
    import cv2
    # img = cv2.imread("source_frames/image0.jpg")
    # print(img.shape)

    # identify_and_highlight("source_frames/9_original.png", "target_frames/9_forged.png")
    identify_and_highlight("source_frames/original.png", "target_frames/target.png")
main()
