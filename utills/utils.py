# -*- coding: utf-8 -*-
import logging
import logging.handlers


def logging_settings(max_bytes=7000, backup_count=6, file_handler=True):
    """
    Настройки ведения журнала
    """
    from settings import LOG_DIR, LOG_FILE
    format_message = '[%(asctime)s] %(message)s'
    formatter = logging.Formatter(format_message)
    if not file_handler:
        handler = logging.StreamHandler()
    else:
        handler = logging.handlers.RotatingFileHandler(filename=LOG_DIR / LOG_FILE,
                                                       maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    logging.root.setLevel(logging.WARNING)
    logging.root.handlers.clear()
    logging.root.addHandler(handler)
