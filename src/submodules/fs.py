from resources.globals import shutil, Path

class Files():
    def __init__(self):
        pass

    def createFile(self, filename, dir, content=None):
        path = dir + '\\' + filename
        stream = open(path, 'w', encoding='utf-8')
        if content != None:
            stream.write(content)
        
        stream.close()

    def moveFile(self, input_path, output_path):
        file_size = input_path.stat()
        shutil.move(str(input_path), str(output_path))

        return {
            'filesize': int(file_size.st_size)
        }
    
    def copyFile(self, input_path, output_path):
        file_size = input_path.stat()
        shutil.copy2(str(input_path), str(output_path))

        return {
            'filesize': int(file_size.st_size)
        }

files_utils = Files()
