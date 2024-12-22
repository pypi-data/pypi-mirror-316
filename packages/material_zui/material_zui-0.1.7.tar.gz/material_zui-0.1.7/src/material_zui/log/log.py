import json
from logging import FileHandler, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from tarfile import DEFAULT_FORMAT
from typing import Any, Iterable, Optional
from pandas import DataFrame

from material_zui.dict import is_dict
from material_zui.list import is_list

from .data import DEFAULT_FORMAT, DEFAULT_LEVEL


# https://codelearn.io/sharing/logging-python-system-talk-module
class ZuiLog:
    """
    @level priority: DEBUG --> INFO --> WARNING --> ERROR --> CRITICAL
    @stream_level: log to console
    @file_level: log to file
    @rotating_file_level: log to file and rotating by number
        @backupCount: max file backup, default `10`
        @maxBytes: max file size, default `2.000 Bytes`
    @time_rotating_file_level: log to file and rotating specific time
        - default log file with format: `zui_log.2023-08-21_09-32.log`

        @when: when to split log file, input values: `S = Seconds`, `M - Minutes`, `H - Hours`, `D - Days`, `midnight` - roll over at midnight, `W{0-6}` - roll over on a certain day; `0` - Monday; `...`
        @interval: time to change log file name
    """

    __logger = getLogger(__name__)
    __stream_handler = None
    __file_handler = None
    __rotating_file_handler = None
    __time_rotating_file_handler = None

    debug = __logger.debug
    info = __logger.info
    warning = __logger.warning
    error = __logger.error
    critical = __logger.critical

    def __init__(
        self,
        log_format: str = DEFAULT_FORMAT,
        log_level: int = DEFAULT_LEVEL,
        stream_level: int = DEFAULT_LEVEL,
        file_level: Optional[int] = None,
        rotating_file_level: Optional[int] = None,
        time_rotating_file_level: Optional[int] = None,
        file_log_name: str = "",
        maxBytes: int = 2000,
        backupCount: int = 10,
        when: str = "midnight",
        interval: int = 1,
    ) -> None:
        self.set_config(
            log_format,
            log_level,
            stream_level,
            file_level,
            rotating_file_level,
            time_rotating_file_level,
            file_log_name,
            maxBytes,
            backupCount,
            when,
            interval,
        )

    def set_config(
        self,
        log_format: str = DEFAULT_FORMAT,
        log_level: int = DEFAULT_LEVEL,
        stream_level: int = DEFAULT_LEVEL,
        file_level: Optional[int] = None,
        rotating_file_level: Optional[int] = None,
        time_rotating_file_level: Optional[int] = None,
        file_log_name: str = "",
        maxBytes: int = 2000,
        backupCount: int = 10,
        when: str = "midnight",
        interval: int = 1,
    ) -> None:
        self.__formatter = Formatter(log_format) if log_format else None

        self.set_stream_handler(stream_level)
        self.set_file_handler(file_log_name, file_level)
        self.set_rotating_file_handler(
            file_log_name, maxBytes, backupCount, rotating_file_level
        )
        self.set_time_rotating_file_handler(
            file_log_name, when, interval, time_rotating_file_level
        )

        if log_level:
            self.__logger.setLevel(log_level)

    def set_status(self, disabled: bool) -> None:
        self.__logger.disabled = disabled

    def set_stream_handler(self, level: Optional[int] = None) -> None:
        if self.__stream_handler:
            self.__logger.removeHandler(self.__stream_handler)
        if level:
            self.__stream_handler = StreamHandler()
            self.__stream_handler.setLevel(level)
            if self.__formatter:
                self.__stream_handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__stream_handler)

    def set_file_handler(self, file_log_name: str, level: Optional[int] = None) -> None:
        if self.__file_handler:
            self.__logger.removeHandler(self.__file_handler)
        if file_log_name and level:
            self.__file_handler = FileHandler(file_log_name)
            self.__file_handler.setLevel(level)
            if self.__formatter:
                self.__file_handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__file_handler)

    def set_rotating_file_handler(
        self,
        file_log_name: str,
        maxBytes: int = 2000,
        backupCount: int = 10,
        level: Optional[int] = None,
    ) -> None:
        if self.__rotating_file_handler:
            self.__logger.removeHandler(self.__rotating_file_handler)
        if file_log_name:
            self.__rotating_file_handler = RotatingFileHandler(
                file_log_name, maxBytes=maxBytes, backupCount=backupCount
            )
            self.__rotating_file_handler.namer = self.namer
            if self.__formatter:
                self.__rotating_file_handler.setFormatter(self.__formatter)
            if level:
                self.__rotating_file_handler.setLevel(level)
            self.__logger.addHandler(self.__rotating_file_handler)

    def set_time_rotating_file_handler(
        self,
        file_log_name: str,
        when: str = "midnight",
        interval: int = 1,
        level: Optional[int] = None,
    ) -> None:
        if self.__time_rotating_file_handler:
            self.__logger.removeHandler(self.__time_rotating_file_handler)
        if file_log_name:
            self.__time_rotating_file_handler = TimedRotatingFileHandler(
                file_log_name, when, interval
            )
            self.__time_rotating_file_handler.namer = self.namer
            if self.__formatter:
                self.__time_rotating_file_handler.setFormatter(self.__formatter)
            if level:
                self.__time_rotating_file_handler.setLevel(level)
            self.__logger.addHandler(self.__time_rotating_file_handler)

    def namer(self, default_name: str) -> str:
        base_filename, ext, date = default_name.split(".")
        return f"{base_filename}.{date}.{ext}"

    def list_to_dict(
        self, data: list[dict[Any, Any]], default_value: Any = ""
    ) -> dict[str, list[Any]]:
        data_table: dict[str, list[Any]] = {}
        if data:
            for index, item in enumerate(data):
                for key in item:
                    list_value = data_table.get(key)
                    value = item.get(key) or default_value
                    if list_value != None:
                        list_value.append(value)
                    else:
                        data_table[key] = [
                            *[default_value for _ in range(index)],
                            value,
                        ]
            list_count_value = [len(list_value) for list_value in data_table.values()]
            max_count_value = max(list_count_value)
            for key in data_table:
                list_value = data_table[key]
                count_list_value = len(list_value)
                if count_list_value < max_count_value:
                    data_table[key] = [
                        *list_value,
                        *[
                            default_value
                            for _ in range(max_count_value - count_list_value)
                        ],
                    ]
        return data_table

    # def to_data_frame(self, data: dict[str, list[Any]]) -> DataFrame:
    #     return DataFrame(data)

    def dict_to_data_frame(
        self, data: list[dict[Any, Any]], default_value: Any = ""
    ) -> DataFrame:
        list_data = self.list_to_dict(data, default_value)
        return DataFrame(list_data)

    def print_table(
        self, data: DataFrame | dict[Any, Any] | Iterable[dict[Any, Any]]
    ) -> None:
        df = DataFrame(data)
        print(df)

    def print_table_obj(
        self, data: list[dict[Any, Any]], default_value: Any = ""
    ) -> None:
        """
        @default_value: for case empty field data
        """
        data_table = self.dict_to_data_frame(data, default_value)
        self.print_table(data_table)

    def debug_table(self, data: list[dict[Any, Any]], default_value: Any = "") -> None:
        data_table = self.dict_to_data_frame(data, default_value)
        self.debug(data_table)

    def info_table(self, data: list[dict[Any, Any]], default_value: Any = "") -> None:
        data_table = self.dict_to_data_frame(data, default_value)
        self.info(data_table)

    def warning_table(
        self, data: list[dict[Any, Any]], default_value: Any = ""
    ) -> None:
        data_table = self.dict_to_data_frame(data, default_value)
        self.warning(data_table)

    def error_table(self, data: list[dict[Any, Any]], default_value: Any = "") -> None:
        data_table = self.dict_to_data_frame(data, default_value)
        self.error(data_table)

    def critical_table(
        self, data: list[dict[Any, Any]], default_value: Any = ""
    ) -> None:
        data_table = self.dict_to_data_frame(data, default_value)
        self.critical(data_table)

    def fprint(self, value: Any, indent: int = 2) -> None:
        """
        Format print for easy to eye with `list` and `dict` type
        """
        if is_list(value):
            for index, item in enumerate(value):
                print(index, item)
        elif is_dict(value):
            pretty_obj = json.dumps(value, indent=indent)
            print(pretty_obj)
        else:
            print(value)
