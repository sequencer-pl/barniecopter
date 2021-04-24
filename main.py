import logging

from config.config import ConfigParser
from logger.logger import logging_setup
from net.datasources import TAAPI, CMC


def process(configs):
    for name, config in configs.items():
        logging.debug(f"Processing config entry {name}")

        taapi = TAAPI(config)
        indicator = taapi.get_indicator_data()
        logging.debug(f"Indicator data: {indicator}")

        cmc = CMC(config)
        coin = cmc.get_price_and_volume()
        logging.debug(f"{name} in CMC: {coin}")


def run():
    logging_setup()
    configs = ConfigParser(['config/config.yaml', 'config/secrets.yaml']).read_configs()
    logging.debug(f"Read configs from files: {configs}")
    process(configs)


if __name__ == '__main__':
    run()
