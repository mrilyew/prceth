from executables.extractors.Base.Base import BaseExtractor
from repositories.ExecutableRepository import ExecutableRepository

class ExtractorsRepository(ExecutableRepository):
    class_type = BaseExtractor
