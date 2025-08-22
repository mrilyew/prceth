from declarable.ArgsComparer import ArgsComparer

class ArgsValidator:
    def validate(self, ext_args, input_args, cfg = {}):
        self.comparing = ext_args
        self.args = input_args

        cfg.check()

        decl = ArgsComparer(self.comparing, self.args, 'assert', cfg.is_free_args())

        return decl.dict()
