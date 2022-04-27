from termcolor import cprint
from src.models.base_db import BaseDb

import src.util.helper as _h
import inspect


class Log:
    def __init__(self, database: int):
        self.base = BaseDb(database=database)
        # Todo cron tab na promazání starých logů
        # full_log -> logi úplně vše
        # cli_log -> logi do konzole
        # db_log -> logi do databáze
        # self.console_log: bool = self.base.

    def info(self, msg: str = 'NO MESSAGE'):
        previous_frame = inspect.currentframe().f_back
        (filename, line_number,
         function_name, lines, index) = inspect.getframeinfo(previous_frame)
        cprint(f'[{_h.get_today()}] {function_name} - INFO {msg}', 'cyan')
        self.base.log_db(filename, function_name, int(line_number), 'INFO', msg)

    def warning(self, msg: str = 'NO MESSAGE'):
        previous_frame = inspect.currentframe().f_back
        (filename, line_number,
         function_name, lines, index) = inspect.getframeinfo(previous_frame)
        cprint(f'[{_h.get_today()}] {function_name} - WARNING {msg}', 'yellow')
        self.base.log_db(filename, function_name, int(line_number), 'WARNING', msg)

    def error(self, msg: str = 'NO MESSAGE'):
        previous_frame = inspect.currentframe().f_back
        (filename, line_number,
         function_name, lines, index) = inspect.getframeinfo(previous_frame)
        cprint(f'[{_h.get_today()}] {function_name} - ERROR {msg}', 'red')
        self.base.log_db(filename, function_name, int(line_number), 'ERROR', msg)
