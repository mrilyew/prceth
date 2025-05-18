from executables.acts.Base.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils

class AdditionalMetadata(BaseAct):
    name = 'AdditionalMetadata'
    category = 'metadata'

    async def execute(self, args=None):
        # TODO videos, audios, docx
        return {}
