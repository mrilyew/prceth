import asyncio

class Hookable:
    events = []

    def __init__(self):
        self._hooks = {}

    def hooks(self, category):
        return self._hooks.get(category)

    def add_hook(self, category, hook):
        if self._hooks.get(category) == None:
            self._hooks[category] = []

        self._hooks.get(category).append(hook)

    def remove_hook(self, category, hook):
        try:
            self._hooks.get(category).remove(hook)
        except Exception:
            pass

    def trigger(self, *args, **kwargs):
        asyncio.ensure_future(self.trigger_hooks(*args, **kwargs))

    async def trigger_hooks(self, category, *args, **kwargs):
        if self._hooks.get(category) == None:
            self._hooks[category] = []

        for hook in self._hooks.get(category):
            try:
                await hook(*args, **kwargs)
            except:
                pass
