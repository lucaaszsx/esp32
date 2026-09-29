import json
import subprocess
import sys
from pathlib import Path

from common import PROJECTS_FOLDER, Colors, print_format


def find_project(directory: str) -> Path:
    root = Path(PROJECTS_FOLDER)
    start = Path(directory).resolve()

    if root not in start.parents:
        print_format(Colors.FAIL, f"\"{start}\" is not inside \"{root}\"")
        sys.exit(1)

    for path in (start, *start.parents):
        if path == root:
            break
        if (path / "platformio.ini").is_file():
            return path

    print_format(Colors.FAIL, f"platformio.ini not found between {start} and {root}")
    sys.exit(1)


def pio_call(directory: str, args: list[str]):
    project = find_project(directory)
    return subprocess.call(["pio", *args], cwd=project)

def pio_output(directory: str, args: list[str]) -> str:
    project = find_project(directory)
    return subprocess.run(["pio", *args], cwd=project, stdout=subprocess.PIPE, text=True, check=True).stdout

def pio_load_conf(directory: str):
    project = find_project(directory)

    try:
        conf = json.loads(pio_output(directory, ["project", "config", "--json-output"]))
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print_format(Colors.FAIL, f"Could not load project configuration from {project.name}: {e}")
        sys.exit(1)

    return conf

def main():
    sys.exit(pio_call(sys.argv[1], sys.argv[2:]))

if __name__ == "__main__":
    main()
