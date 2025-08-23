from executables.Runnable import Runnable
from executables.Documentable import Documentable
from executables.Saveable import Saveable
from executables.Findable import Findable
from executables.RecursiveDeclarable import RecursiveDeclarable
from utils.Hookable import Hookable
from app.App import logger

class Executable(Runnable, Documentable, Saveable, RecursiveDeclarable, Hookable, Findable):
    def __init__(self):
        super().__init__()

        def __onerror(exception):
            logger.logException(exception, section=logger.SECTION_EXECUTABLES)

        self.add_hook("error", __onerror)
        #self.events.get("success").append(__onsuccess)
