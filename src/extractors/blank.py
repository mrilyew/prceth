from extractors.Base import BaseExtractor
from resources.globals import file_manager

class blank(BaseExtractor):
    name = 'blank'
    category = 'base'
    hidden = True
    params = {
        "format": {
            "desc_key": "extractor_key_desc_blank_format",
            "type": "string",
            "maxlength": 3
        },
        "text": {
            "desc_key": "extractor_key_desc_blank_text",
            "type": "string",
            "maxlength": -1
        }
    }

    def execute(self, args):
        format = args.get('format')
        text = args.get('text')
        if format == None:
            format = 'txt'
        
        original_name = 'blank.' + str(format)
        file_manager.createFile(filename=original_name,dir=self.temp_dir,content=text)
        if text == None:
            text = ''

        return {
            'format': str(format),
            'original_name': original_name,
            'filesize': len(text.encode('utf-8')),
        }
