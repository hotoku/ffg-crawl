_IS_DEBUG = False


def set_debug_flag(flag: bool):
    global _IS_DEBUG
    _IS_DEBUG = flag


def is_debug():
    return _IS_DEBUG
