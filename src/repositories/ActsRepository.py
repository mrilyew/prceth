from executables.acts.Base.Base import BaseAct
from repositories.ExecutableRepository import ExecutableRepository

class ActsRepository(ExecutableRepository):
    class_type = BaseAct
