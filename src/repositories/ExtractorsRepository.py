from executables.extractors import BaseExtractor
from repositories.ExecutableRepository import ExecutableRepository

class ExtractorsRepository(ExecutableRepository):
    class_type = BaseExtractor
