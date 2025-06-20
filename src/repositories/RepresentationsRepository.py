from app.App import logger
from pathlib import Path
from resources.Consts import consts
from repositories.ExecutableRepository import ExecutableRepository
from executables.representations.Representation import Representation
import importlib

class RepresentationsRepository(ExecutableRepository):
    class_type = Representation

    def __category(self):
        return ""

    def getList(self, show_hidden: bool = False, search_category: str = None):
        repo_type = self.class_type.__name__
        __exit = []

        return __exit
