import os

from . import env
from . import pack
from . import pull


def init(project_name: str, cache_url: str):
    """
    Initialize the project dir with the given cache url.
    If the project's cache doesn't exist, it'll be downloaded.
    """
    env.set_project(project_name)

    if env.exists():
        return
    
    env.create()
    tgz = pull.pull(cache_url)
    try:
        pack.unpack(tgz)
    finally:
        os.unlink(tgz)
