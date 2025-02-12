class BaseThumbnail:
    name = 'base'
    accept = ["based"]

    def __init__(self, save_dir=None):
        self.save_dir = save_dir

    def run(self, params):
        pass
    
    def acceptsFormat(self, format):
        return format in self.accept
