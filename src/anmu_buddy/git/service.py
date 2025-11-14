from typing import Union, List

from anmu_buddy.core.file_utils import create_temp_file, delete_file
from anmu_buddy.core.git_utils import GitAutomation

class GitService():
    def __init__(self, ):
        self.git_automation = GitAutomation()

    def commit(self, files: Union[str, List[str], tuple[str, ...]], message_file:str)-> None:
        path_temp_file = create_temp_file()
        self.git_automation.commit_change(files= files, message_file= message_file)
        delete_file(path_temp_file)

    def push(
            self, 
            files: Union[str, List[str], tuple[str, ...]],  
            remote:str="origin", 
            branch:str=None,
        )-> None:
        path_temp_file = create_temp_file()
        current_branch = self.git_automation.sync_change(
            files= files, 
            message_file= path_temp_file, 
            remote= remote, 
            branch= branch,
        )
        delete_file(path_temp_file)
        return current_branch