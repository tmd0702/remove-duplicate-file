import json

class Config:
    def __init__(self):
        """
         @brief Loads the config. json file and stores it in self. config This is called by __init__
        """
        file_path = "configs/config.json"
        self.config = json.load(open(file_path, encoding='utf-8'))
    def get(self, param):
        """
         @brief Get a parameter from the configuration. This is a shortcut for config [ param ]. The default implementation returns the value of the configuration parameter.
         @param param Name of the parameter to get. E. g.
         @return Value of the parameter or None if not set or the parameter doesn't exist in the configuration file
        """
        return self.config.get(param)