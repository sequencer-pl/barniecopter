import logging

from config.config import ConfigParser
from logger.logger import logging_setup


def run():
    logging_setup()
    c = ConfigParser(['config/config.yaml', 'config/secrets.yaml']).read_configs()
    logging.info(f'It works! {c}')


if __name__ == '__main__':
    run()
