import os
import hashlib
import pathlib
from multiprocessing import Pool, Process
from config import Config

config = Config()

class FileManager:
    def __init__(self):
        """
         @brief Initialize the hash set and size set. This is called when __init__ is called and should not be called
        """
        self.hash_set = set()
        self.size_set = set()
        self.total_size = 0
        self.counter = 0

    def _is_file_size_duplicated(self, file_path):
        """
         @brief Checks if file_path is duplicated. If it is it adds the size to size_set and returns True.
         @param file_path Path to file to check.
         @return True if file_path is duplicated False otherwise. Note that this method does not check if the file is a directory
        """
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size
        self.total_size += file_size
        # Returns true if the size of the file is in the size set.
        if file_size in self.size_set:
            return True
        else:
            self.size_set.add(file_size)
            return False
    def _get_file_hash(self, file_path):
        """
         @brief Calculate md5 hash of file. This is used to verify file integrity in case of large files.
         @param file_path Path to file to hash. Must be absolute or relative to config. BUFF_SIZE
         @return String of hex digest
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Read the data from the file and update the md5 hash.
            while True:
                data = f.read(config.get("BUFF_SIZE"))
                # If data is not empty break the loop.
                if not data:
                    break
                md5.update(data)
        md5_hash = md5.hexdigest()
        return md5_hash

    def _is_file_hash_duplicated(self, file_path):
        """
         @brief Checks if hash of file_path is already in hash_set. If not it adds it to hash_set
         @param file_path path to file to check
         @return True if file_path has already been added False if it has not been added and is not a duplicate
        """
        md5_hash = self._get_file_hash(file_path)
        # Returns true if the hash is in the hash set.
        if md5_hash in self.hash_set:
            return True
        else:
            self.hash_set.add(md5_hash)
            return False

    def remove_duplicate_file(self, file_path):
        """
         @brief Remove file if size or hash is duplicated. Also add to hash set. This is used to prevent duplication of files when we have a lot of files
         @param file_path Path to file to
        """
        # Add a new file to the hash set.
        if self._is_file_size_duplicated(file_path) and self._is_file_hash_duplicated(file_path):
            print(f"Remove {file_path} due to duplication")
            os.remove(file_path)
        else:
            md5_hash = self._get_file_hash(file_path)
            self.hash_set.add(md5_hash)
            print(f"New file {file_path} detected")

    def _execute_loop_path_process(self, path, is_join=False):
        """
         @brief Execute loop path process. This is a wrapper for : meth : ` LoopPath. execute `.
         @param path Path to be executed. It can be a list of paths or a single path
         @param is_join If True the process will
        """
        p = Process(target=self.loop_path, args=(path,))
        p.start()
        # join if join is set to true
        if is_join:
            p.join()

    def loop_path(self, base_path):
        """
         @brief Loop through directory and check for files. This is used for loop_files and loop_dirs.
         @param base_path Base path to search for files and
        """
        dir_list = os.listdir(base_path)
        # Process all files in dir_list and add them to the counter.
        for name in dir_list:
            path = base_path + name

            # Process a path and add a file to the loop.
            if os.path.isdir(path):
                self._execute_loop_path_process(path + '/')
            elif os.path.isfile(path):
                self.counter += 1
                file_extension = pathlib.Path(path).suffix[1:]
                # Remove duplicate file if it s a file extension
                if file_extension in config.get("FILE_EXTENSIONS"):
                    self.remove_duplicate_file(path)

    def run(self):
        """
         @brief Run the loop path process and return the exit code. This is called by the run () method of the Loop
        """
        self._execute_loop_path_process(config.get("BASE_PATH"), True)


# This function is called from the main module.
if __name__ == "__main__":
    file_manager = FileManager()
    file_manager.run()
    print(f"Total size: {file_manager.total_size}")
    print(f"Total file nums: {file_manager.counter}")

