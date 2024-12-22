from logging import DEBUG
from .log import ZuiLog

zui_log = ZuiLog(
    time_rotating_file_level=DEBUG, when="m", file_log_name="log/zui_log.log"
)

debug = zui_log.debug
info = zui_log.info
warning = zui_log.warning
error = zui_log.error
critical = zui_log.critical

debug_table = zui_log.debug_table
info_table = zui_log.info_table
warning_table = zui_log.warning_table
error_table = zui_log.error_table
critical_table = zui_log.critical_table

print_table = zui_log.print_table
print_table_obj = zui_log.print_table_obj
fprint = zui_log.fprint
