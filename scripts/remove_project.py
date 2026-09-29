import os
import shutil
import sys

from InquirerPy.prompts.confirm import ConfirmPrompt as confirm
from InquirerPy.prompts.input import InputPrompt as text
from InquirerPy.prompts.list import ListPrompt as list
from lib.common import PROJECTS_FOLDER, print_fail, print_success, print_warn


def main():
    project_list = os.listdir(PROJECTS_FOLDER) if os.path.exists(PROJECTS_FOLDER) else []
    
    if len(project_list) == 0:
        print_fail("There is no projects yet")
        sys.exit(1)
    
    project_name = list(message="What project you want to remove?", choices=project_list).execute()
    
    proceed1 = confirm(message=f"Do you really want to remove the project \"{project_name}\"? (this action is irreversible)").execute()
    
    if not proceed1:
        print_warn("Aborted")
        sys.exit(0)
    
    project_folder = os.path.join(PROJECTS_FOLDER, project_name)
    proceed2 = confirm(message=f"Think again if thats really what you want. The folder \"{project_folder}\" will be entirely deleted. Do you really want to delete the project? (last warning)").execute()
    
    if not proceed2:
        print_warn("Aborted")
        sys.exit(0)

    check = text(message="To confirm, enter the name of the project:").execute()
    if check != project_name:
        print_fail("Names do not match")
        sys.exit(1)
    
    try:
        print_warn(f"Deleting the project: {project_folder}")
        shutil.rmtree(project_folder)
    
        print_success("Project deleted")
    except OSError as e:
        print_fail(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()