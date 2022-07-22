import logging

import coloredlogs


def get_logger(name=__name__, level=logging.INFO):
    """Returns logger.

    Args:
        name (str): module name.
        level (int): logging level.

    Returns:
        logger (logging.RootLogger): logger.
    """
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(level)

    # log handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # formatter
    formatter = coloredlogs.ColoredFormatter(
        fmt="[%(asctime)s] [%(levelname)s] [func] %(funcName)s [line] %(lineno)d: %(message)s",
        datefmt="%Y-%d-%d %H:%M:%S",
        level_styles={
            "critical": {"color": "red", "bold": True},
            "error": {"color": "red"},
            "warning": {"color": "yellow"},
            "notice": {"color": "magenta"},
            "info": {},
            "debug": {"color": "green"},
            "spam": {"color": "green", "faint": True},
            "success": {"color": "green", "bold": True},
            "verbose": {"color": "blue"},
        },
        field_styles={
            "asctime": {"color": "green"},
            "levelname": {"color": "cyan", "bold": True},
            "funcName": {"color": "blue"},
            "lineno": {"color": "blue", "bold": True},
        },
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
