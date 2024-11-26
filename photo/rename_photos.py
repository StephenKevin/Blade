"""
Rename photos by datetime.
使用日期时间对照片重新命名。

Dependence:
- https://pypi.org/project/filetype/
- https://pypi.org/project/Pillow/

"""

import datetime
import os
import string

import filetype
from PIL import ExifTags, Image

PHOTO_DIR = r'path of your photos'  # 指定照片所在的文件夹

NAME_FORMAT = '%Y-%m-%dT%H%M%S'     # 指定照片新命名使用的日期格式


def get_phone_datetime(photo_path: str):
    """return the datetime of the photo"""
    image = Image.open(photo_path, 'r')
    image_exif = image.getexif()
    exif_datetime = image_exif.get(ExifTags.Base.DateTime)
    fmt = '%Y:%m:%d %H:%M:%S'
    image_datetime = datetime.datetime.strptime(exif_datetime, fmt)
    image.close()
    return image_datetime


def rename_photos(photos_dir):
    photos = os.listdir(photos_dir)
    count = 0
    pass_count = 0
    for photo in photos:
        src_path = os.path.join(photos_dir, photo)
        if not filetype.is_image(src_path):
            continue
        photo_datetime = get_phone_datetime(src_path)
        dst_name = photo_datetime.strftime(NAME_FORMAT)
        ext = os.path.splitext(src_path)[1]
        dst_path = os.path.join(photos_dir, dst_name + ext)
        if src_path != dst_path:
            if not os.path.exists(dst_path):
                os.rename(src_path, dst_path)
                count = count + 1
                print(src_path, '--->>>', dst_path)
            else:
                for sss in string.ascii_uppercase:
                    dst_path = os.path.join(photos_dir, dst_name + sss + ext)
                    if src_path != dst_path:
                        if not os.path.exists(dst_path):
                            os.rename(src_path, dst_path)
                            count = count + 1
                            print(src_path, '--->>>', dst_path)
                            break
                        else:
                            continue
                    else:
                        pass_count = pass_count + 1
                        print(src_path, 'passed')
                        break
        else:
            print(src_path, 'passed')
            pass_count = pass_count + 1

    print(f'suceeded: {count}')
    print('passed:', pass_count)


if __name__ == 'main':
    rename_photos(PHOTO_DIR)

