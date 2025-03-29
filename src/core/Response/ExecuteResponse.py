class ExecuteResponse():
    def __init__(self, infe = {}):
        self.source = infe.get("source")
        self.internal_content = infe.get("internal_content")
        self.indexation_content = infe.get("indexation_content")
        self.main_file = infe.get("main_file")
        self.another_file = infe.get("another_file")
        self.hash = infe.get("hash")
        self.return_type = infe.get("return_type")
        self.unlisted = infe.get("unlisted")
        self.entities = infe.get("entities", [])
        self.suggested_name = infe.get("suggested_name", None)
        self.suggested_description = infe.get("suggested_description", None)
        self.linked_files = infe.get("linked_files", None)
    
    def get_format(self):
        return str(self.format)
    
    def get_original_name(self):
        return self.original_name
    
    def get_filesize(self):
        return self.filesize
    
    def get_source(self):
        return self.source
    
    def get_internal_content(self):
        return self.internal_content
        
    def get_summary(self):
        return self.summary
    
    def get_hash(self):
        return self.hash
    
    def get_rt(self):
        return self.return_type

    def hasSource(self):
        return self.source != None
    
    def hasIndexationContent(self):
        return self.indexation_content != None

    def hasInternalContent(self):
        return self.internal_content != None
    
    def hasPreview(self):
        return self.another_file != None

    def hasHash(self):
        return self.hash != None

    def hasFormat(self):
        return getattr(self, "format", None) != None
    
    def isUnlisted(self):
        return getattr(self, "unlisted", False) == True
