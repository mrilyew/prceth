from resources.Globals import consts, os, Path, shutil
from executables.acts.Base.Base import BaseAct
from db.Entity import Entity

class MoveBrokenTempDirs(BaseAct):
    name = 'MoveBrokenTempDirs'
    category = 'storage'
    accepts = 'string'

    async def execute(self, i: str, args):
        TMP_FILES_DIR = os.path.join(consts["tmp"], "files")
        DESTINATION = i

        for root, _, files in os.walk(TMP_FILES_DIR):
            for file in files:
                src_path = os.path.join(root, file)

                if os.path.dirname(src_path) == DESTINATION or file == ".gitkeep":
                    continue

                base, extension = os.path.splitext(file)
                counter = 1
                new_file = file
                dst_path = os.path.join(DESTINATION, new_file)
                while os.path.exists(dst_path):
                    new_file = f"{base}_{counter}{extension}"
                    dst_path = os.path.join(DESTINATION, new_file)
                    counter += 1

                shutil.move(src_path, dst_path)

        return {"destination": DESTINATION}
