from app.App import logger
from executables.Runnable import Runnable
from executables.Documentable import Documentable
from executables.Saveable import Saveable
from executables.RecursiveDeclarable import RecursiveDeclarable

class Executable(Runnable, Documentable, Saveable, RecursiveDeclarable):
    events = {
        "beforeRun": [],
        "success": [],
        "afterSave": [],
        "error": [],
    }

    def __init__(self):
        def __onerror(exception):
            logger.logException(exception, section=logger.SECTION_EXECUTABLES)

        self.events.get("error").append(__onerror)
        #self.events.get("success").append(__onsuccess)

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict):
        _args = self.__class__.validate(args)
        self.preExecute(_args)

        return await self.execute(_args)

    # Events

    async def onError(self, exception: Exception):
        for __closure in self.events.get("error"):
            if __closure != None:
                continue

            await __closure(exception)

    async def onAfterSave(self, results):
        for __closure in self.events.get("afterSave"):
            if __closure != None:
                continue

            await __closure(results)

    async def onSuccess(self):
        for __closure in self.events.get("success"):
            if __closure != None:
                continue

            await __closure()
