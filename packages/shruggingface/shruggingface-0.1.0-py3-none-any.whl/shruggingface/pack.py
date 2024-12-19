import os
import tarfile

from . import env


def get_size(src_path=None):
    return _human_size(_get_size_bytes(src_path))


def _get_size_bytes(src_path=None):
    src_path = src_path or env.get() 

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(src_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return total_size


def _human_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def pack(output_path, src_path=None):
    src_path = src_path or env.get()

    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(src_path, arcname=os.path.basename(src_path))


def unpack(tar_path, dest_path=None):
    
    dest_path = dest_path or env.get()

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=dest_path)
