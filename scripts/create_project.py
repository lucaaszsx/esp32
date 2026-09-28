import re
import subprocess
import sys
from os import makedirs, path

from common import PROJECTS_FOLDER, Colors, print_format
from InquirerPy.prompts.input import InputPrompt as text


def main():
    print_format(Colors.HEADER, "PlatformIO - Create a new project")
    
    project_name: str = text(message="What will be the project name?").execute()
    
    if not project_name or not re.fullmatch(r"[A-Za-z0-9_]+$", project_name):
        print_format(Colors.FAIL, "Project name must contain characters from A-Z (lower and upper case), 0-9 and underscores")
        sys.exit(1)
    
    project_folder = path.join(PROJECTS_FOLDER, project_name)
    
    if path.exists(project_folder):
        print_format(Colors.FAIL, f"Already exists an project named \"{project_name}\" in \"{PROJECTS_FOLDER}\"")
        sys.exit(1)
    
    print_format(Colors.CYAN, "Creating project")
    
    try:
        print_format(Colors.YELLOW, "  . Create project folder")
        makedirs(project_folder)
    
        print_format(Colors.YELLOW, "  . Run: pio project init")
        subprocess.run(["pio", "project", "init"], cwd=project_folder, check=True)
    
        print()
        print_format(Colors.GREEN, "Ok.")
    except (OSError, subprocess.CalledProcessError) as e:
        print_format(Colors.FAIL, f"Something went wrong: {e}")

if __name__ == "__main__":
    main()