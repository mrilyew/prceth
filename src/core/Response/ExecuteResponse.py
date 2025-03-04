class ExecuteResponse():
    def __init__(self, infe = {}):
        self.format = infe.get("format")
        self.original_name = infe.get("original_name")
        self.source = infe.get("source")
        self.filesize = infe.get("filesize")
        self.json_info = infe.get("json_info")
        self.text = infe.get("text")
        self.another_file = infe.get("another_file")
        self.hash = infe.get("hash")
        self.return_type = infe.get("return_type")
        self.unlisted = infe.get("unlisted")
        self.summary = infe.get("summary")
        self.no_file = infe.get("no_file")
    
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
