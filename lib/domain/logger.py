from colorama import init as colorama_init, Fore

colorama_init()


class LoggerLevels:
    ValidLevels = [
        'DEBUG',
        'INFO ',
        'WARN ',
        'ERROR'
    ]

    ERROR = 3
    WARN = 2
    INFO = 1
    DEBUG = 0

    @classmethod
    def log_string(cls, level):
        if not cls.valid(level):
            raise ValueError(f'Invalid log level: {level}')

        return cls.ValidLevels[level]

    @classmethod
    def valid(cls, level):
        return level is cls.ERROR\
               or level is cls.WARN\
               or level is cls.INFO\
               or level is cls.DEBUG


class Logger:
    LoggingLevel = LoggerLevels.INFO

    @classmethod
    def _get_log_message(cls, color, level, msg):
        return f'{color}{LoggerLevels.log_string(level)}{Fore.RESET} > {msg}'

    @classmethod
    def log(cls, color, level, msg):
        if cls.LoggingLevel > level:
            return
        print(cls._get_log_message(color=color, level=level, msg=msg))

    @classmethod
    def error(cls, s):
        cls.log(color=Fore.RED, level=LoggerLevels.ERROR, msg=s)

    @classmethod
    def warn(cls, s):
        cls.log(Fore.YELLOW, LoggerLevels.WARN, s)

    @classmethod
    def info(cls, s):
        cls.log(color=Fore.GREEN, level=LoggerLevels.INFO, msg=s)

    @classmethod
    def debug(cls, s):
        cls.log(color=Fore.MAGENTA, level=LoggerLevels.DEBUG, msg=s)
