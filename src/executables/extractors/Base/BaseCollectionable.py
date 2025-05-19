from executables.extractors.Base.Base import BaseExtractor

class BaseCollectionable(BaseExtractor):
    def _collection(self):
        return {
            "suggested_name": "N/A",
            "suggested_description": "N/A",
            "source": "api:null",
            "declared_created_at": None,
        }
