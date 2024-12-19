import os


def name():
    """
    Infer the name of the project from the env var, git repo or pwd.
    """
    cache_dir = get()
    if ".cache/huggingface" not in cache_dir:
        return os.path.basename(os.path.dirname(cache_dir))

    if not os.path.exists(".git/config"):
        return os.path.basename(os.getcwd())

    for line in open(".git/config"):
        line = line.strip()
        if "url =" in line and ".git" in line:
            repo = line.rsplit("/", 1)[-1]
            return repo.replace(".git", "")

    return os.path.basename(os.getcwd())


def set(path=None):
    if not path:
        path = get()

    resolved_path = os.path.abspath(path)
    os.environ['HF_HOME'] = resolved_path
    os.environ['HF_HUB_CACHE']= resolved_path + '/hub'


def set_project(name=None):
    if not name:
        name = name()

    path = '~/.cache/shruggingface'
    set(path + '/' + name)


def create():
    path = get()
    os.makedirs(path, exist_ok=True)


def get():
    path = os.getenv("HF_HOME", "~/.cache/huggingface/hub/")
    if not path.endswith('/'):
        path = path + '/'
    return os.path.expanduser(path)


def exists():
    path = get()
    return os.path.isdir(path)
