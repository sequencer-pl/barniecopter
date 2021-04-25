import yaml
from mergedeep import merge


class ConfigParser:
    MANDATORY_KEYS = {
        'TAAPI': ['base_url', 'exchange', 'indicator', 'symbol', 'interval', 'api_key'],
        'CMC': ['base_url', 'endpoint', 'symbol', 'x-cmc-pro-api-key']
    }

    def __init__(self, config_files):
        self.config_files = config_files

    def read_configs(self):
        configs = {}
        for file in self.config_files:
            cnf = self.read_config(file)
            merge(configs, configs, cnf)
        self.validate(configs)
        return configs

    @staticmethod
    def read_config(file):
        with open(file) as f:
            return yaml.safe_load(f)

    def validate(self, configs):
        for item, sites in configs.items():
            if set(sites.keys()) != set(self.MANDATORY_KEYS.keys()):
                e = f"{item} should contain {self.MANDATORY_KEYS.keys()}"
                raise ValidationError(e)
            for site, params in sites.items():
                diff = set(params).symmetric_difference(set(self.MANDATORY_KEYS[site]))
                if diff:
                    e = f"Lack or improper key {', '.join(diff)} in {site} entry"
                    raise ValidationError(e)


class ValidationError(Exception):
    pass
