class ExecutableConfig:
    def __init__(self, content):
        self.content = content

    def ignores(self):
        return self.content.get("ignore", [])

    def is_free_args(self):
        return self.content.get("free_args")
