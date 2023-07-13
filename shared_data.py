import json
from config import Config
from multiprocessing import Manager

class SharedData:
    def __init__(self, config):
        """
         @brief Initialize the cache. This is called by __init__ and should not be called directly. The config is a dictionary of key / value pairs that can be used to configure the cache.
         @param config The configuration dictionary to use for this cache instance
        """
        self._config = config
        self._hash_dict = Manager().dict()
        self._size_dict = Manager().dict()
        self._total_removal_size = Manager().Value(float, 0.0)
        self._total_removal_count = Manager().Value("i", 0)
        self._total_moved_size = Manager().Value(float, 0.0)
        self._total_moved_count = Manager().Value("i", 0)
        # If the cache is readable, this method will construct the dictionaries
        if self._config.get("IS_CACHE_READABLE"):
            self._construct_dicts()

    def _construct_dicts(self):
        """
         @brief Construct hash and size dictionaries from cache. This is called from __init__ and should not be called
        """
        try:
            hash_cache = json.load(open(f"{self._config.get_root_dir()}cache/hash-dict.json", "r"))
            size_cache = json.load(open(f"{self._config.get_root_dir()}cache/size-dict.json", "r"))
            self._hash_dict = Manager().dict(hash_cache)
            self._size_dict = Manager().dict(size_cache)
        except:
            print("Caches not found")

    def get_total_removal_size(self):
        """
         @brief Gets the total removal size of the file. This is the size of the file that will be removed from the storage when the file is deleted.
         @return The total removable size of the file or 0 if the file does not exist or is not removable
        """
        return self._total_removal_size.value

    def get_total_removal_count(self):
        """
         @brief Gets the total removal count. This is used to determine how many items in the item list are removed from the item's list of items.
         @return The total removals count in the item list or 0 if there are no removals in the item
        """
        return self._total_removal_count.value

    def add_total_removal_size(self, addition):
        """
         @brief Add a number of bytes to the total removal size. This is used to prevent memory leaks and for debugging
         @param addition The number of bytes to
        """
        self._total_removal_size.value += addition

    def add_total_removal_count(self, addition):
        """
         @brief Add a number to the total removal count. This is used to prevent accidental garbage collection of a job that is about to be deleted
         @param addition The number to add
        """
        self._total_removal_count.value += addition

    def get_total_moved_count(self):
        return self._total_moved_count.value

    def get_total_moved_size(self):
        return self._total_moved_size.value

    def _add_total_moved_count(self, addition):
        self._total_moved_count.value += addition

    def _add_total_moved_size(self, addition):
        self._total_moved_size.value += addition

    def get_hash_dict(self):
        """
         @brief Gets the hash_dict of this V1alpha1VirtualMachineSnapshotSpec. # noqa : E501 A dictionary of hash values keyed by UUID
         @return The hash_dict of this V1alpha1VirtualMachineSnapshotSpec
        """
        return self._hash_dict

    def get_size_dict(self):
        """
         @brief Gets the size_dict of this V1alpha1MetricStatus. # noqa : E501 Specifies the size of the metric in MiB.
         @return The size_dict of this V1alpha1MetricStatus or None if not set or unknown ( default : None
        """
        return self._size_dict

    def set_hash(self, hash_key, value):
        """
         @brief Set a hash value. This is used to save the state of the file when it is loaded.
         @param hash_key The key to store the hash value under.
         @param value The value to store under the key ( must be a string
        """
        self._hash_dict[hash_key] = value

    def get_hash(self, hash):
        """
         @brief Get the value associated with the hash. This is used to determine if there is a cache entry that has the same hash or not
         @param hash The hash to look up
         @return The value associated with the hash or None if not found ( no cache entry is found for the hash
        """
        return self._hash_dict.get(hash)

    def set_size(self, size_key, value):
        """
         @brief Set the size of the file. This is a helper for : meth : ` set_file ` to be used in order to set the size of the file in bytes.
         @param size_key The key for the size. It must be a string of the form ` ` file_name. size ` ` e. g.
         @param value The size of the file in bytes. It must be a string of the form ` ` file_name. size
        """
        self._size_dict[size_key] = value

    def get_size(self, size):
        """
         @brief Get size of file. This is used to determine the size of a file based on its size in bytes.
         @param size Size of file in bytes. Can be any of the following : 1.
         @return Size of file in bytes
        """
        return self._size_dict.get(size)

    def write_cache(self, cache_file, value):
        """
         @brief Write a value to the cache. This is used to cache values that need to be recomputed in the next run
         @param cache_file Name of the cache file
         @param value Value to write to the cache ( dict or list
        """
        # Save the value to cache file if the cache file is writable
        if self._config.get("IS_CACHE_WRITABLE"):
            with open(f"{self._config.get_root_dir()}cache/{cache_file}", "w") as outfile:
                json.dump(value.copy(), outfile)