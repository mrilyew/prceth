from executables.Saveable import Saveable

class ThumbnailMethod(Saveable):
    def __init__(self, outer):
        self.outer = outer

    def create(self, item, params)->list:
        pass
