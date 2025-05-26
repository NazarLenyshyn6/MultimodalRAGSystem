"""Configures and provides a centralized logger for the project."""


import logging

LOGGING_FORMAT = '[%(asctime)s | %(name)s | %(levelname)s] -> %(message)s'

logging.basicConfig(level=logging.INFO,
                    format=LOGGING_FORMAT,
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(name='TheBatchMultimodalRAGLogger')