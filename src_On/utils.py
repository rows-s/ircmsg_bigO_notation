def escape_tag_value(value: str) -> str:
    r"""
    Escapes value: ' ' -> '\s', ';' -> '\:', '\' -> '\\'.
    """
    return value.translate({ord('\\'): '\\\\', ord(' '): r'\s', ord(';'): r'\:'})


def unescape_tag_value(value: str) -> str:
    r"""
    Unescapes escaped value: '\s' -> ' ', '\:' -> ';', '\\' -> '\'.
    """
    return value.replace(r'\:', ';').replace(r'\s', ' ').replace('\\\\', '\\')


