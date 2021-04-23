import yaml


class ConfigParser:
    def __init__(self, config_files):
        self.config_files = config_files

    def read_configs(self):
        configs = {}
        for file in self.config_files:
            cnf = self.read_config(file)
            configs.update(cnf)
        return configs

    @staticmethod
    def read_config(file):
        with open(file) as f:
            return yaml.safe_load(f)
