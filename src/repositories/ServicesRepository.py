from executables.services.Base.Base import BaseService
from repositories.ExecutableRepository import ExecutableRepository

class ServicesRepository(ExecutableRepository):
    class_type = BaseService
