class DocumentationManager:
    lang = 'en'

    def resolveTranslationDict(self, locale_dict: dict)->str:
        return locale_dict.get(self.lang)

    def loadDocs(self, docs_dict):
        self.docs = docs_dict
