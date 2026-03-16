from PIL import Image
import imagehash
import exifread
from datetime import datetime


def perceptual_hash(path):

    try:

        img = Image.open(path)

        return imagehash.phash(img)

    except:

        return None


def data_exif(path):

    try:

        with open(path,'rb') as f:

            tags = exifread.process_file(
                f,
                stop_tag="EXIF DateTimeOriginal"
            )

        if "EXIF DateTimeOriginal" in tags:

            data = str(tags["EXIF DateTimeOriginal"])

            return datetime.strptime(
                data,
                "%Y:%m:%d %H:%M:%S"
            )

    except:
        pass

    return None