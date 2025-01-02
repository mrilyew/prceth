from resources.globals import win32file, win32api, os, shutil, Path

class FileInfo():
    def __init__(self, entry, extended = False):
        self.name = entry.name
        self.path = entry.path
        self.type = 'file'
        self.extended = extended
        if entry.is_dir():
            self.type = 'dir'
        elif entry.is_symlink():
            self.type = 'symlink'

        if extended == True:
            stat = entry.stat()
            self.size = stat.st_size
            self.created_time = stat.st_ctime
            self.modified_time = stat.st_mtime
            self.accessed_time = stat.st_atime
            self.owner = stat.st_uid
            self.group = stat.st_gid
            self.permissions = stat.st_mode

    def takeInfo(self):
        base = {
                "name": self.name,
                "path": self.path,
                "type": self.type,
                "extended": self.extended,
                "type": self.type
            }
        
        if(self.extended == True):
            base['size'] = self.size
            base['created_time'] = self.created_time
            base['modified_time'] = self.modified_time
            base['accessed_time'] = self.accessed_time
            base['owner'] = self.owner
            base['group'] = self.group
            base['permissions'] = self.permissions

        return base

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
    
file_manager = FileManager()
