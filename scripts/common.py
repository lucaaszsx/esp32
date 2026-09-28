from enum import Enum
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECTS_FOLDER = path.abspath(path.join(BASE_DIR, "..", "projects"))
COMPILEDB_SCRIPT_FILE = "compiledb_include_toolchain.py"
COMPILEDB_SCRIPT_PATH = path.abspath(path.join(BASE_DIR, "..", "assets", COMPILEDB_SCRIPT_FILE))

class Colors(Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    FAIL = "\033[91m"

def format_msg(color, msg):
    msg = f"{color.value}{msg}\033[0m"
    return msg

def print_format(color, msg):
    print(format_msg(color, msg))
