from pathlib import Path
import shutil
import hashlib
from datetime import datetime
from image_tools import data_exif, perceptual_hash
import os

MESES = {1:"JAN",2:"FEV",3:"MAR",4:"ABR",5:"MAI",6:"JUN",
         7:"JUL",8:"AGO",9:"SET",10:"OUT",11:"NOV",12:"DEZ"}

VIDEO_EXT = {".mp4",".mov"}
IMAGE_EXT = {".jpg",".jpeg",".png",".heic",".dng",".webp",".tiff",".bmp",".gif"}
SUPPORTED = VIDEO_EXT | IMAGE_EXT


def hash_file(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def file_date(path):
    return datetime.fromtimestamp(path.stat().st_mtime)


def get_date(path):
    d = data_exif(path)
    if d:
        return d
    return file_date(path)


def collect_files(folder):
    folder = Path(folder)
    files = []
    for root,_,fs in os.walk(folder):
        for f in fs:
            p = Path(root)/f
            if p.suffix.lower() in SUPPORTED:
                files.append(p)
    return files


def relative_path(base, path):
    """Caminho relativo para manter estrutura de subpastas"""
    return path.relative_to(base)


def nome_unico(dest):
    base = dest.stem
    ext = dest.suffix
    pasta = dest.parent
    i = 1
    novo = dest
    while novo.exists():
        novo = pasta / f"{base}_{i}{ext}"
        i += 1
    return novo


def organize(origin, dest, progress=None):
    origin = Path(origin)
    dest = Path(dest)

    files = collect_files(origin)

    hashes = set()
    copied = 0
    duplicates = 0
    total = len(files)

    for i, path in enumerate(files):

        h = hash_file(path)
        if h in hashes:
            duplicates += 1
            if progress: progress(i+1,total)
            continue
        hashes.add(h)

        date = get_date(path)
        month_year = f"{MESES[date.month]} {str(date.year)[-2:]}"

        # Mantém caminho relativo da origem
        rel_path = relative_path(origin, path)
        dest_path = dest / month_year / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        dest_path = nome_unico(dest_path)

        shutil.copy2(path, dest_path)
        copied += 1

        if progress: progress(i+1,total)

    return copied, duplicates, total