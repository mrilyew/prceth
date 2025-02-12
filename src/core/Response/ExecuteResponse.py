class ExecuteResponse():
    def __init__(self, format, original_name, source, json_info, text = None, filesize = None, another_file = None):
        self.format = format
        self.original_name = original_name
        self.source = source
        self.filesize = filesize
        self.json_info = json_info
        self.text = text
        self.another_file = another_file
    
    def get_format(self):
        return str(self.format)
    
    def get_original_name(self):
        return self.original_name
    
    def get_filesize(self):
        return self.filesize
    
    def get_source(self):
        return self.source
    
    def get_json_info(self):
        return self.json_info
    
    def get_preview(self):
        return self.another_file
    
    def hasSource(self):
        return self.source != None
    
    def hasJsonInfo(self):
        return self.json_info != None
    
    def hasPreview(self):
        return self.another_file != None
