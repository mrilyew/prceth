from plugins.BasePlugins import BaseUploadPlugin
from resources.globals import consts, settings

class link(BaseUploadPlugin):
    name = 'base.link'
    format = '%'
    works = 'all'
    category = 'base'

    def run(self, args):
        pass
