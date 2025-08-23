from utils.ClassProperty import classproperty
from importlib.metadata import distributions
from app.App import logger

class Runnable:
    buffer = {}
    base_categories = ["template", "base"]
    available = ['web', 'cli']
    required_modules = []

    @classproperty
    def category(self)->str:
        class_full_name = self.__module__
        _ = class_full_name.split('.')

        return _[-2]

    @classproperty
    def category_with_name(self)->str:
        class_full_name = self.__module__
        _ = class_full_name.split('.')

        return _[-2] + "." + _[-1]

    # Comparisons

    @classmethod
    def isAbstract(cls):
        return cls.category.lower() in cls.base_categories

    @classmethod
    def isHidden(cls):
        return getattr(cls, "hidden", False) == True

    @classmethod
    def canBeExecuted(cls):
        '''
        Is this Executable can be runned or it's technical
        '''
        return cls.isAbstract() == False and cls.isHidden() == False

    @classmethod
    def canBeUsedAt(cls, at):
        return at in cls.available

    @classmethod
    def isConfirmable(cls):
        return getattr(cls, "PreExecute", None)

    @classmethod
    def isModulesInstalled(cls):
        all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
        satisf_libs = []

        for required_module in cls.required_modules:
            if required_module in all_installed:
                satisf_libs.append(required_module)

        return len(satisf_libs) == len(cls.required_modules)

    @classmethod
    def full_name(cls):
        return cls.category_with_name

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict):
        _args = self.__class__.validate(args)

        if getattr(self, "before_execute", None) != None:
            self.before_execute(_args)

        logger.log(message=f"Executed {self.full_name()}",section=logger.SECTION_EXECUTABLES,kind=logger.KIND_MESSAGE)

        return await self.execute(_args)
