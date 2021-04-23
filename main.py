import logging

from config.config import ConfigParser
from logger.logger import logging_setup

if __name__ == '__main__':
    logging_setup()
    c = ConfigParser(['config/config.yaml', 'config/secrets.yaml']).read_configs()
    logging.info(f'It works! {c}')
