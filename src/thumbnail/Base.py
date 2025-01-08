class BaseThumbnail:
    name = 'base'
    accept = ["based"]

    def __init__(self, input_file=None):
        self.input_file = input_file

    def run(self, params):
        pass
