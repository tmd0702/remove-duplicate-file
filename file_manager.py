import os
import json
import hashlib
import pathlib
from multiprocessing import Pool
from config import Config
from shared_data import SharedData

class FileManager:
    def __init__(self, shared_data, config):
        """
         @brief Initialize the instance. This is called by __init__ and should not be called directly. You should not call this method directly unless you are using : py : class : ` waflib. Tools. SharedData ` to access shared data.
         @param shared_data A class that contains the shared data for the task.
         @param config A config object that contains the configuration for the task
        """
        self._config = config
        self.shared_data = shared_data
        self.dir_paths = list()

    def _is_file_size_duplicated(self, file_size):
        """
         @brief Checks if the file size is duplicated. This is used to prevent duplicate files from appearing in the list of files
         @param file_size The size of the file
         @return True if the file size is duplicated False if it is not in the list of files or if the file size is
        """
        # Returns True if the file size is in bytes.
        if self.shared_data.get_size(str(file_size)):
            return True
        else:
            return False
    def _get_file_size(self, file_path):
        """
         @brief Get the size of a file. This is a wrapper around os. stat. st_size to avoid having to re - calculate the size every time we need to do a get_file
         @param file_path The path to the file
         @return The size of the file in bytes or None if the file doesn't exist or is not a
        """
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size
        return file_size
    def _get_file_hash(self, file_path):
        """
         @brief Calculate md5 hash of file. This is used to verify file integrity in case of large files.
         @param file_path Path to file to hash. Must be absolute or relative to self. _root_path.
         @return MD5 hash of file as hex string. May be empty if file doesn't exist or is too large
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Read the data from the file.
            while True:
                data = f.read(self._config.get("BUFF_SIZE"))
                # If data is not empty break the loop.
                if not data:
                    break
                md5.update(data)
        md5_hash = md5.hexdigest()
        return md5_hash

    def _is_file_hash_duplicated(self, md5_hash):
        """
         @brief Check if file hash is duplicated. This is used to prevent duplicates in shared data. The hash is compared to the MD5 hash of the file being duplicated
         @param md5_hash MD5 hash of the file being duplicated
         @return True if the hash is duplicated False if it is not in the shared data or if it is not
        """
        # Returns True if the hash is valid for the shared data.
        if self.shared_data.get_hash(md5_hash):
            return True
        else:
            return False

    def remove_duplicate_file(self, file_path):
        """
         @brief Remove file_path if it is new. This method is called by FileManager when a file is removed from the storage
         @param file_path Path to the file
        """
        file_size, file_hash = self._get_file_size(file_path), self._get_file_hash(file_path)
        # if file_size and file_hash are duplicated
        if self._is_file_size_duplicated(file_size) and self._is_file_hash_duplicated(file_hash):
            print(f"Remove {file_path} due to duplication. Free {file_size} bytes")
            self.shared_data.add_total_removal_size(file_size / pow(1024, 3))
            self.shared_data.add_total_removal_count(1)
            os.remove(file_path)
        else:
            self.shared_data.set_hash(file_hash, True)
            self.shared_data.set_size(str(file_size), True)
            print(f"New file {file_path} detected")

    def construct_dir_paths(self, base_path):
        """
         @brief Construct list of directories to search for. This is recursive so we don't have to worry about recursion
         @param base_path base path to start
        """
        self.dir_paths.append(base_path)
        try:
            dir_list = os.listdir(base_path)
            print(dir_list)
        except:
            print("Access denied, skip")
            return
        # print(dir_list)
        # Recursively construct the directory paths for each directory.
        for name in dir_list:
            path = base_path + name
            # Construct the directory paths for the given path.
            if os.path.isdir(path):
                self.construct_dir_paths(path + "/")


    def loop_path(self, base_path):
        """
         @brief Loop through directory and check for files with same extension. This is used for cleaning up files that are in the same directory as the test file
         @param base_path path to the directory to
        """
        dir_list = os.listdir(base_path)
        # Remove duplicate files in the directory list.
        for name in dir_list:
            path = base_path + name
            # Remove duplicate file if it s a file extension.
            if os.path.isfile(path):
                file_extension = pathlib.Path(path).suffix[1:]
                # Remove duplicate files if they are already in the file_extension list.
                if file_extension in self._config.get("FILE_EXTENSIONS"):
                    self.remove_duplicate_file(path)

    def run(self):
        """
         @brief Scan directories and remove files that are no longer in the cache. This is run in a separate thread
        """
        # Construct the directory paths for the base_path.
        for base_path in self._config.get("BASE_PATH"):
            self.construct_dir_paths(base_path)
        self.dir_paths = list(set(self.dir_paths))
        print(f"Scanning {len(self.dir_paths)} directories with {os.cpu_count()} CPUs")
        pool = Pool()
        pool.map(self.loop_path, self.dir_paths)
        self.shared_data.write_cache("hash-dict.json", self.shared_data.get_hash_dict())
        self.shared_data.write_cache("size-dict.json", self.shared_data.get_size_dict())

        print(f"Removed {shared_data.get_total_removal_count()} files, free {shared_data.get_total_removal_size()} GB")

# This is the main function that is called from the main module.
if __name__ == "__main__":
    config = Config()
    shared_data = SharedData(config)
    file_manager = FileManager(shared_data, config)
    file_manager.run()