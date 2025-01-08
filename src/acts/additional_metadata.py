from acts.Base import BaseAct
from hachoir.core import config
from resources.globals import utils, createParser, extractMetadata

class additional_metadata(BaseAct):
    name = 'additional_metadata'
    allow_type = 'entity'
    type = 'entities'

    def execute(self, args=None):
        # todo videos, audios, docx
        return {}
