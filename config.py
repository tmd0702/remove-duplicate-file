import json

class Config:
    def __init__(self):
        """
         @brief Loads the config. json file and stores it in self. config This is called by __init__
        """
        file_path = "configs/config.json"
        self.config = json.load(open(file_path, encoding='utf-8'))
        self._root_dir, _os_name = None, None

    def get(self, param):
        """
         @brief Get a parameter from the configuration. This is a shortcut for config [ param ]. The default implementation returns the value of the configuration parameter.
         @param param Name of the parameter to get. E. g.
         @return Value of the parameter or None if not set or the parameter doesn't exist in the configuration file
        """
        return self.config.get(param)

    def set_root_dir(self, root_dir):
        self._root_dir = root_dir

    def get_root_dir(self):
        return self._root_dir

    def set_os_name(self, os_name):
        self._os_name = os_name

    def get_os_name(self):
        return self._os_name