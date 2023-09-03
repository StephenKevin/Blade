"""
Categorize photos by season.
按照时间（季节）对照片进行分类。

Dependence:
- https://pypi.org/project/filetype/
- https://pypi.org/project/Pillow/
"""

import datetime
import math
import os
import shutil

import filetype
from PIL import ExifTags, Image

PHOTO_DIR = r'path of your photos'  # 指定照片的文件夹


def get_phone_datetime(photo_path: str):
    """return the datetime of the photo"""
    image = Image.open(photo_path, 'r')
    image_exif = image.getexif()
    exif_datetime = image_exif.get(ExifTags.Base.DateTime)
    fmt = '%Y:%m:%d %H:%M:%S'
    image_datetime = datetime.datetime.strptime(exif_datetime, fmt)
    image.close()
    return image_datetime


photos = os.listdir(PHOTO_DIR)
count = 0
for photo in photos:
    src_path = os.path.join(PHOTO_DIR, photo)
    if os.path.isdir(src_path):
        continue
    if not filetype.is_image(src_path):
        continue
    else:
        photo_datetime = get_phone_datetime(src_path)
        qx = math.ceil(photo_datetime.month/3)
        season = f'{photo_datetime.year}Q{qx}'
        category = os.path.join(PHOTO_DIR, season)
        if not os.path.exists(category):
            os.makedirs(category)
        dst_path = os.path.join(category, photo)
        shutil.move(src_path, dst_path)
        count = count + 1


print(f'suceeded: {count}')
