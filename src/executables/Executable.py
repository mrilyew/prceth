from executables.Runnable import Runnable
from executables.Documentable import Documentable
from executables.Saveable import Saveable
from executables.RecursiveDeclarable import RecursiveDeclarable
from utils.Hookable import Hookable
from app.App import logger

class Executable(Runnable, Documentable, Saveable, RecursiveDeclarable, Hookable):
    def __init__(self):
        super().__init__()

        def __onerror(exception):
            logger.logException(exception, section=logger.SECTION_EXECUTABLES)

        self.add_hook("error", __onerror)
        #self.events.get("success").append(__onsuccess)

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict):
        _args = self.__class__.validate(args)
        self.preExecute(_args)

        logger.log(message=f"Executed {self.full_name()}",section=logger.SECTION_EXECUTABLES,kind=logger.KIND_MESSAGE)

        return await self.execute(_args)
