def escape_tag_value(value: str) -> str:
    r"""
    Escapes value: ' ' -> '\s', ';' -> '\:', '\' -> '\\'.
    '\r' and '\n' (CR and LF) don't need to be escaped.
    """
    return value.translate({ord('\\'): '\\\\', ord(' '): r'\s', ord(';'): r'\:'})
