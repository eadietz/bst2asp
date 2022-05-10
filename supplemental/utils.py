import os

import psutil
from loguru import logger
import hashlib


class AbortException(Exception):
    pass


class TimeoutException(AbortException):
    pass


class InterruptException(AbortException):
    pass


def handler(signum, frame):
    logger.error('signum %s' % signum)
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        logger.error('Child pid is {}\n'.format(child.pid))
        logger.error('Killing child.')
        try:
            os.kill(child.pid, 15)
        except OSError as e:
            logger.warning('Process might already be gone. See error below.')
            logger.warning('%s' % str(e))

    logger.warning('SIGNAL received')
    if signum == 15:
        raise TimeoutException('signal')
    else:
        raise InterruptException('signal')


def nothing(signum, frame):
    logger.warning('SIGNAL received\n')
    logger.warning('SIGNAL ignored...\n')


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()
