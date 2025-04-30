from executables.acts.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils

class AdditionalMetadata(BaseAct):
    name = 'AdditionalMetadata'
    category = 'metadata'
    allow_type = 'entity'

    async def execute(self, i, args=None):
        # TODO videos, audios, docx
        return {}
