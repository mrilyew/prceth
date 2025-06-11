from executables.Runnable import Runnable
from declarable.ArgumentsTypes import IntArgument, StringArgument
from app.App import config
import importlib

class Thumbnail(Runnable):
    category = 'base'
    accepts = {
        'type': 'mime',
        'value': ['base']
    }

    def declare():
        params = {}
        params['width'] = IntArgument({
            "default": config.get("thumbnail.width")
        })
        params['height'] = IntArgument({
            "default": config.get("thumbnail.height")
        })
        params['path'] = StringArgument({
            "assertion": {
                "not_null": True
            }
        })

        return params

    def execute(self, i = {}):
        pass

    def canBeRun(self, check_ability):
        return check_ability in self.accepts.get('values')

    def safeExecute(self, args: dict):
        return self.execute(self.validate(args))

    @staticmethod
    def getByMime(mime_type):
        mime = mime_type.split('/')
        mime_name = mime[0]

        class_name = f"{mime_name.capitalize()}Thumbnail"
        class_obj = importlib.import_module(f"thumbnails.mimes.{class_name}")

        if class_obj == None:
            return None

        return getattr(class_obj, class_name)
