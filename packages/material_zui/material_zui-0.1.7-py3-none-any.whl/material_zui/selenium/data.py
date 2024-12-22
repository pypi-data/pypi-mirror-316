from typing import TypedDict


TitleInfo = TypedDict('TitleInfo', {
    'title': str, 'caption': str, 'yt_description': str, 'tags': list[str], 'hash_tags': list[str]
})
