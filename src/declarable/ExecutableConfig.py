from resources.Exceptions import DeclaredArgumentsException

class ExecutableConfig:
    def __init__(self, content):
        self.content = content

    def ignores(self):
        return self.content.get("ignore", [])

    def is_free_args(self):
        return self.content.get("free_args")

    def check(self):
        MAIN_ARG_TYPE = self.content.get("type")

        if MAIN_ARG_TYPE == "and":
            for _arg in self.content.get("list"):
                if _arg not in self.args:
                    raise DeclaredArgumentsException(f"Argument \"{_arg}\" not passed")
        elif MAIN_ARG_TYPE == "or" or MAIN_ARG_TYPE == "strict_or":
            passed_list_need = 0
            for _arg in self.content.get("list", []):
                if _arg in self.args:
                    passed_list_need += 1

            if passed_list_need == 0:
                raise DeclaredArgumentsException(f"Need at least 1 required argument")

            if MAIN_ARG_TYPE == "strict_or" and passed_list_need > 1:
                raise DeclaredArgumentsException(f"Pass only 1 required argument (cuz \"strict_or\")")
