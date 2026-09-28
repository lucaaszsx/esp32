import subprocess
import sys
from pathlib import Path

from common import PROJECTS_FOLDER, Colors, print_format


def main():
    root = Path(PROJECTS_FOLDER)
    start = Path(sys.argv[1]).resolve()

    if root not in start.parents:
        sys.exit(f"{start} is not inside {root}")

    for path in (start, *start.parents):
        if path == root:
            break
        if (path / "platformio.ini").is_file():
            print_format(Colors.GREEN, "platformio.ini found")
            sys.exit(subprocess.call(["pio", *sys.argv[2:]], cwd=path))

    print_format(Colors.FAIL, f"platformio.ini not found between {start} and {root}")
    sys.exit(1)

if __name__ == "__main__":
    main()
