import json
import re
import shutil
import subprocess
import sys
from os import makedirs, mkdir, path

from common import (
    COMPILEDB_SCRIPT_FILE,
    COMPILEDB_SCRIPT_TEMPLATE,
    GITIGNORE_FILE,
    GITIGNORE_TEMPLATE,
    PROJECTS_FOLDER,
    Colors,
    print_format,
)
from InquirerPy.base.control import Choice
from InquirerPy.prompts.confirm import ConfirmPrompt as confirm
from InquirerPy.prompts.fuzzy import FuzzyPrompt as fuzzy
from InquirerPy.prompts.input import InputPrompt as text
from InquirerPy.prompts.list import ListPrompt as select


def main():
    print_format(Colors.HEADER, "PlatformIO - Create a new project")

    project_name: str = text(message="What will be the project name?").execute()

    if not project_name or not re.fullmatch(r"[A-Za-z0-9_-]+$", project_name):
        print_format(Colors.FAIL, "Project name must contain characters from A-Z (lower and upper case), 0-9 and underscores")
        sys.exit(1)

    project_folder = path.join(PROJECTS_FOLDER, project_name)

    if path.exists(project_folder):
        print_format(Colors.FAIL, f"Already exists an project named \"{project_name}\" in \"{PROJECTS_FOLDER}\"")
        sys.exit(1)

    print_format(Colors.CYAN, "Loading boards")

    try:
        boards = json.loads(subprocess.run(["pio", "boards", "--json-output"], capture_output=True, text=True, check=True).stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print_format(Colors.FAIL, f"Could not load the boards list: {e}")
        sys.exit(1)

    board: dict = fuzzy(
        message="Which board will be used?",
        choices=[Choice(value=b, name=f"{b['name']} ({b['id']})") for b in boards],
    ).execute()

    framework: str | None = None

    if board["frameworks"]:
        framework = select(message="Which framework will be used?", choices=board["frameworks"]).execute()

    monitor_speed: str = text(message="What will be the monitor speed (baud)?", default="115200").execute()

    if not monitor_speed.isdigit():
        print_format(Colors.FAIL, "Monitor speed must be a number")
        sys.exit(1)

    sample_code = confirm(message="Do you want sample code?", default=True).execute()
    run_compile_db = confirm(message="Do you generate compile commands after creating the project?", default=True).execute()

    command = ["pio", "project", "init", "--board", board["id"]]

    if framework:
        command += ["--project-option", f"framework={framework}"]

    command += ["--project-option", f"monitor_speed={monitor_speed}"]

    if sample_code:
        command.append("--sample-code")

    command += ["--project-option", f"extra_scripts=pre:scripts/{COMPILEDB_SCRIPT_FILE}"]

    print_format(Colors.CYAN, "Creating project")

    try:
        print_format(Colors.YELLOW, "  . Create project folder")
        makedirs(project_folder)

        scripts_folder = path.join(project_folder, "scripts")
        mkdir(scripts_folder)

        print_format(Colors.YELLOW, f"  . Copy template files to \"{project_name}\" folder")
        shutil.copyfile(COMPILEDB_SCRIPT_TEMPLATE, path.join(scripts_folder, COMPILEDB_SCRIPT_FILE))
        shutil.copyfile(GITIGNORE_TEMPLATE, path.join(project_folder, GITIGNORE_FILE))

        print_format(Colors.YELLOW, f"  . Run: {' '.join(command)}")
        subprocess.run(command, cwd=project_folder, check=True)

        print()
        print_format(Colors.GREEN, "Created.")
        print()

        if not run_compile_db:
            return

        compiledb_command = ("pio", "run", "--target", "compiledb")
        print_format(Colors.YELLOW, "  . Generate compile_commands")
        print_format(Colors.YELLOW, f"    . Run: {' '.join(compiledb_command)}")

        subprocess.run(compiledb_command, cwd=project_folder, check=True)
    except (OSError, subprocess.CalledProcessError) as e:
        print_format(Colors.FAIL, f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
