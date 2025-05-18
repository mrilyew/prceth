from resources.Globals import consts, os, file_manager
from executables.acts.Base.Base import BaseAct

class ClearTemp(BaseAct):
    name = 'ClearTemp'
    category = 'storage'

    async def execute(self, args = {}):
        TMP_FILES_DIR = os.path.join(consts["tmp"], "files")

        for tmp_dir, _ in os.walk(TMP_FILES_DIR):
            file_manager.rmdir(tmp_dir)

        return {"success": True}
