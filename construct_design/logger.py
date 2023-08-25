import logging
import sys

# logging #####################################################################


def setup_applevel_logger(logger_name="SETUP", is_debug=False, file_name=None):
    """
    Set up the logger for the app
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    # pylint: disable=C0103
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        # pylint: disable=C0103
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_logger(module_name, logger_name="SETUP"):
    """
    Get the logger for the module
    """
    return logging.getLogger(logger_name).getChild(module_name)
