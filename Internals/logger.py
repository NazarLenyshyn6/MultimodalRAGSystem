"""Project logger."""

import logging

LOGGING_FORMAT = '[%(asctime)s | %(name)s | %(levelname)s] -> %(message)s'

logging.basicConfig(level=logging.INFO,
                    format=LOGGING_FORMAT,
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger('python_pytorch_profiling_logger')