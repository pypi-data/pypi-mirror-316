import logging
import coloredlogs
import verboselogs


def setup_logger(level=None):
    if not level:
        level = logging.INFO
    verboselogs.install()
    coloredlogs.install(level=level)
    # coloredlogs.install(level=logging.DEBUG)
    # fmt = "%(name)s,%(message)s"
    # logging.basicConfig(level=logging.INFO, format=fmt)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    return logger
