class ExecuteResponse():
    def __init__(self, original_name, source, json_info, format = None, text = None, filesize = None, another_file = None, unlisted = False, return_type = "entity", summary = None, no_file = False):
        self.format = format
        self.original_name = original_name
        self.source = source
        self.filesize = filesize
        self.json_info = json_info
        self.text = text
        self.another_file = another_file
        self.hash = None
        self.return_type = return_type
        self.unlisted = unlisted
        self.summary = summary
        self.no_file = no_file
    
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
        
    def get_summary(self):
        return self.summary
    
    def get_hash(self):
        return self.hash
    
    def get_rt(self):
        return self.return_type

    def hasSource(self):
        return self.source != None
    
    def hasJsonInfo(self):
        return self.json_info != None
    
    def hasPreview(self):
        return self.another_file != None

    def hasHash(self):
        return self.hash != None

    def hasFormat(self):
        return getattr(self, "format", None) != None
    
    def isUnlisted(self):
        return getattr(self, "unlisted", False) == True
