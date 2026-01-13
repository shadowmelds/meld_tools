# Fix UnicodeDecodeError
# https://blender.stackexchange.com/questions/299978/how-to-fix-unicodedecodeerror?rq=1

STRING_CACHE = {}


def intern_enum_items(items):
    """解决选择非英文命名的目标时名称是乱码的问题
    使用方法：
    """

    def intern_string(s):
        if not isinstance(s, str):
            return s
        global STRING_CACHE
        if s not in STRING_CACHE:
            STRING_CACHE[s] = s
        return STRING_CACHE[s]

    return [tuple(intern_string(s) for s in item) for item in items]
