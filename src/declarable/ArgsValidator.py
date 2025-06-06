from resources.Exceptions import DeclaredArgumentsException
from declarable.DeclarableArgs import DeclarableArgs

class ArgsValidator:
    def checkCfg(self):
        MAIN_ARG_TYPE = self.cfg.get("type")

        if MAIN_ARG_TYPE == "and":
            for _arg in self.cfg.get("list"):
                if _arg not in self.args:
                    raise DeclaredArgumentsException(f"Argument \"{_arg}\" not passed")
        elif MAIN_ARG_TYPE == "or" or MAIN_ARG_TYPE == "strict_or":
            passed_list_need = 0
            for _arg in self.cfg.get("list", []):
                if _arg in self.args:
                    passed_list_need += 1

            if passed_list_need == 0:
                raise DeclaredArgumentsException(f"Need at least 1 required argument")

            if MAIN_ARG_TYPE == "strict_or" and passed_list_need > 1:
                raise DeclaredArgumentsException(f"Pass only 1 required argument (cuz \"strict_or\")")

    def validate(self, ext_args, input_args, cfg = {}):
        self.comparing = ext_args
        self.args = input_args
        self.cfg = cfg

        self.checkCfg()

        decl = DeclarableArgs(self.comparing, self.args, 'assert', self.cfg.get('free_args') == True)

        return decl.dict()
