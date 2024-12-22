from typing import TypeAlias, Any, TypedDict

# ZuiFile = dict[{'name': str, 'ext': str, 'file_name': str, 'dir_name': str}]
ZuiFile = TypedDict(
    'ZuiFile', {'name': str, 'ext': str, 'file_name': str, 'dir_name': str})

ZuiExcelColumn = TypedDict('ZuiExcelColumn', {
    'field': str,
    'name': str,
    'type': str,
    'width': str,
    'format': str
}, total=False)
# ZuiExcelColumn: TypeAlias = dict[
#     {
#         'field': str,
#         'name': str,
#         # 'type': Optional[str],
#         # 'width': Optional[str],
#         # 'format': Optional[str]
#     }
# ]

ZuiExcelColumns: TypeAlias = list[ZuiExcelColumn]

ZuiExcelDataItem = dict[str, Any]

ZuiExcelData = list[ZuiExcelDataItem]

# ---
# Movie = TypedDict('Movie', {'name': str, 'year': int})
# Movie = TypedDict('Movie',
#                   {'name': str, 'year': int},
#                   total=True)
# Movie2 = TypedDict('Movie',
#                    {'name': str, 'year': int},
#                    total=False)

# m: Movie = dict(
#     name='Alien',
#     year=1979)

# m3: Movie = {'name': 'str', 'year': 12}
# m3.get('year', 1)

# m4 = dict(name='Alien', year=1979)
# m4.get('year1', 1)

# m2 = dict(
#     name='Alien',
#     year=1979)
