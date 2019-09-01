import re
import sys
import time
import logging

from core.engine import config


class glogFormatter(logging.Formatter):
    """Форматирование вывода logging в стиле Google с++ glog."""

    LEVEL_MAP = {
        logging.FATAL: 'F',  # FATAL is alias of CRITICAL
        logging.ERROR: 'E',
        logging.WARN: 'W',
        logging.INFO: 'I',
        logging.DEBUG: 'D'
    }

    LOG_TEMPLATE = '[%c %04d-%02d-%02d %02d:%02d:%02d.%06d %s %s:%d] %s'

    def __init__(self):
        """."""
        logging.Formatter.__init__(self)

    def format(self, record):
        """Форматирование в стиле Google."""
        level = self.LEVEL_MAP.get(record.levelno, '?')
        try:
            message = record.msg % record.args
        except TypeError:
            message = record.msg
        date = time.localtime(record.created)
        record.getMessage = lambda: self.LOG_TEMPLATE % (
            level, date.tm_year, date.tm_mon, date.tm_mday,
            date.tm_hour, date.tm_min, date.tm_sec,
            (record.created - int(record.created)) * 1e6,
            record.process if record.process is not None else '?????',
            record.filename, record.lineno, message
        )
        return logging.Formatter.format(self, record)


class GLog:
    """Простой логгер в стиле Google с++ glog."""

    GLOG_REGEX = re.compile(r'''
        (?x) ^
        (?P<severity>[FEWID])
        (?P<month>\d\d)(?P<day>\d\d)\s
        (?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)
        \.(?P<microsecond>\d{6})\s+
        (?P<process_id>-?\d+)\s
        (?P<filename>[a-zA-Z<_][\w._<>-]+):(?P<line>\d+)
        \]\s
    ''')

    logger = logging.getLogger()
    handler = logging.StreamHandler(stream=sys.stdout)

    @classmethod
    def SetHandler(cls, new_handler):
        """Установка другого способа записи."""
        cls.logger.removeHandler(cls.handler)
        cls.handler = new_handler
        cls.handler.setFormatter(glogFormatter())
        cls.logger.addHandler(cls.handler)

    @classmethod
    def SetLevel(cls, level):
        """Установка нового уровня логирования."""
        if type(level) == int or re.match(r"\d+", level):
            level = {
                1: logging.CRITICAL,
                2: logging.ERROR,
                3: logging.WARNING,
                4: logging.INFO,
                5: logging.DEBUG
            }.get(int(level), logging.WARNING)
        cls.logger.setLevel(level)
        cls.logger.debug('Log level set to %s', level)

    error = logging.error
    warning = logging.warning
    info = logging.info
    debug = logging.debug
    exception = logging.exception


GLog.SetHandler(GLog.handler)
GLog.SetLevel(config.DEBUG_LEVEL)
