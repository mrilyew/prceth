from resources.globals import win32file, win32api, os

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

class PartitionInfo():
    def __init__(self, drive_name = ""):
        drive_type = win32file.GetDriveType(drive_name)
        if drive_type in [win32file.DRIVE_REMOVABLE, win32file.DRIVE_FIXED]:
            volume_info = win32api.GetVolumeInformation(drive_name)
            free_bytes, total_bytes, _ = win32file.GetDiskFreeSpaceEx(drive_name)

            self.name = volume_info[0]
            self.fs = volume_info[4]
            self.device = drive_name
            self.mount_point = drive_name
            self.total = total_bytes
            self.free = free_bytes
            self.used = total_bytes - free_bytes

    def takeInfo(self):
        return {
            'device': self.device,
            'mount_point': self.mount_point,
            'fs': self.fs,
            'usage': {
                'total': self.total,
                'used': self.used,
                'free': self.free,
                'ratio': round((self.used / self.total) * 100, 3),
            }
        }

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
    
    def getPartitions(self):
        return_array = []
        drive_names = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        for drive_name in drive_names:
            return_array.append(PartitionInfo(drive_name))

        return return_array
    
file_manager = FileManager()
