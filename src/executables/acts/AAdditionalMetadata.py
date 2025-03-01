from executables.acts.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils

class AAdditionalMetadata(BaseAct):
    name = 'AAdditionalMetadata'
    category = 'metadata'
    allow_type = 'entity'

    def execute(self, i, args=None):
        # todo videos, audios, docx
        return {}
