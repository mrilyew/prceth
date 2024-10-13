from plugins.BasePlugins import BaseUploadPlugin

class blank(BaseUploadPlugin):
    name = 'base.blank'
    format = 'format=%;text=%'
    works = 'all'
    category = 'base'

    def run(self, args=None):
        format = args.get('format')
        text = args.get('text')
        if format == None:
            format = 'txt'
        
        original_name = 'blank.' + str(format)
        path = self.temp_dir + '\\' + original_name

        stream = open(path, 'w', encoding='utf-8')
        if text != None:
            stream.write(text)
        
        stream.close()
        if text == None:
            text = ''
        
        return {
            'format': str(format),
            'original_name': original_name,
            'filesize': len(text.encode('utf-8')),
        }
