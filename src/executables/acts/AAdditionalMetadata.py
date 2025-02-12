from executables.acts.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils

class AAdditionalMetadata(BaseAct):
    name = 'AAdditionalMetadata'
    allow_type = 'entity'
    type = 'entities'

    def execute(self, args=None):
        # todo videos, audios, docx
        return {}
