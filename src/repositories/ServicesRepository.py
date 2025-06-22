from executables.services import BaseService
from repositories.ExecutableRepository import ExecutableRepository

class ServicesRepository(ExecutableRepository):
    class_type = BaseService
