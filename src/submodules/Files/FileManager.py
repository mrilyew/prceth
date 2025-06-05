from pathlib import Path
import win32file, win32api, os, shutil

class FileManager():
    def __init__(self):
        pass

    def getFolderItems(self, path, offset = 0, limit = 50, extended = False):
        return_array = []

        with os.scandir(path) as entries:
            entries = list(entries)
            total_count = len(entries)
            cutted_entries = entries[offset:limit + offset]

            for entry in cutted_entries:
                return_array.append(FileInfo(entry, extended))
            
            return return_array, total_count, len(return_array), offset + limit < total_count
        
    def getFolderSize(self, dir):
        return sum(file.stat().st_size for file in Path(dir).rglob('*'))
        
    def createFile(self, filename, dir, content=None):
        path = dir + '\\' + filename
        stream = open(path, 'w', encoding='utf-8')
        if content != None:
            stream.write(content)
        
        stream.close()

    def newFile(self, path, content=None, write_mode = "wb"):
        stream = open(str(path), write_mode)
        if content != None:
            stream.write(content)
        
        stream.close()

    def moveFile(self, input_path, output_path):
        shutil.move(str(input_path), str(output_path))
    
    def copyFile(self, input_path, output_path):
        shutil.copy2(str(input_path), str(output_path))
    
    def symlinkFile(self, input_path, output_path):
        os.symlink(str(input_path), str(output_path))
    
    def rmdir(self, str_path):
        path = Path(str_path)
        
        for sub in path.iterdir():
            if sub.is_dir():
                self.rmdir(sub)
            else:
                sub.unlink()

        path.rmdir()

    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
    
file_manager = FileManager()
