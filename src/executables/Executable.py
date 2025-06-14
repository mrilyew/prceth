from app.App import logger
from executables.Runnable import Runnable
from executables.Documentable import Documentable
from executables.Saveable import Saveable
from executables.RecursiveDeclarable import RecursiveDeclarable

class Executable(Runnable, Documentable, Saveable, RecursiveDeclarable):
    events = {
        "success": [],
        "afterSave": [],
        "error": [],
    }

    def __init__(self):
        def __onerror(exception):
            logger.logException(exception, section="Executables")

        self.events.get("error").append(__onerror)
        #self.events.get("success").append(__onsuccess)

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict):
        return await self.execute(self.__class__.validate(args))

    # Events

    async def onError(self, exception: Exception):
        for __closure in self.events.get("error"):
            await __closure(exception)

    async def onAfterSave(self, entities):
        for __closure in self.events.get("afterSave"):
            await __closure(entities)

    async def onSuccess(self):
        for __closure in self.events.get("success"):
            await __closure()
