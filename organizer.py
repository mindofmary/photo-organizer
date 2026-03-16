import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

from image_tools import data_exif, perceptual_hash

MESES = {
1:"JAN",2:"FEV",3:"MAR",4:"ABR",
5:"MAI",6:"JUN",7:"JUL",8:"AGO",
9:"SET",10:"OUT",11:"NOV",12:"DEZ"
}

VIDEO_EXT = {".mp4",".mov"}

IMAGE_EXT = {
".jpg",".jpeg",".png",".heic",".dng",
".webp",".tiff",".bmp",".gif"
}

SUPPORTED = VIDEO_EXT | IMAGE_EXT


def hash_file(path):

    h = hashlib.sha256()

    with open(path,'rb') as f:

        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()


def file_date(path):

    return datetime.fromtimestamp(
        os.path.getmtime(path)
    )


def get_date(path):

    d = data_exif(path)

    if d:
        return d

    return file_date(path)


def collect_files(folder):

    files = []

    for root,_,fs in os.walk(folder):

        for f in fs:

            p = Path(root)/f

            if p.suffix.lower() in SUPPORTED:

                files.append(p)

    return files


def organize(origin,dest,progress=None):

    files = collect_files(origin)

    hashes = set()
    perceptual = []

    copied = 0
    duplicates = 0

    total = len(files)

    for i,path in enumerate(files):

        h = hash_file(path)

        if h in hashes:

            duplicates += 1
            continue

        hashes.add(h)

        ph = perceptual_hash(path)

        if ph:

            for existing in perceptual:

                if ph - existing < 5:
                    duplicates += 1
                    break

            perceptual.append(ph)

        date = get_date(path)

        folder = f"{MESES[date.month]} {str(date.year)[-2:]}"

        dest_dir = Path(dest)/folder

        dest_dir.mkdir(parents=True,exist_ok=True)

        shutil.copy2(path,dest_dir/path.name)

        copied += 1

        if progress:
            progress(i+1,total)

    return copied,duplicates,total