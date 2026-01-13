def increment_last_number(input_str: str, increment_value: int) -> str:
    """对字符串最后一个数字进行增加"""
    # 寻找最后一个数字的结束位置
    end = -1
    for i in range(len(input_str) - 1, -1, -1):
        if input_str[i].isdigit():
            end = i
            break
    if end == -1:  # 没有数字
        print("没有数字")
        return input_str

    # 寻找最后一个数字的起始位置
    start = end
    while start >= 0 and input_str[start].isdigit():
        start -= 1
    start += 1  # 调整到正确的位置

    # 提取并处理数字
    original = input_str[start : end + 1]
    new_num = str(int(original) + increment_value)

    # 拼接新字符串
    return input_str[:start] + new_num + input_str[end + 1 :]


def get_mirror_name(name: str) -> str:
    if name.endswith(".L"):
        return name[:-2] + ".R"
    elif name.endswith(".R"):
        return name[:-2] + ".L"
    elif name.endswith("_L"):
        return name[:-2] + "_R"
    elif name.endswith("_R"):
        return name[:-2] + "_L"
    else:
        return name  # 不是规范的左右命名


def object_name_to_bone_name(object_name: str) -> str:
    if object_name.endswith("_L"):
        return object_name[:-2] + ".L"
    elif object_name.endswith("_R"):
        return object_name[:-2] + ".R"
    else:
        return object_name  # 不是规范的左右命名


def replace_start_keywords(keywords: str, name: str) -> str:
    """如果name有前缀关键字，返回替换前缀关键字的新字符串，传入空字符串则去除前缀关键字"""
    if not keywords:  # 关键词是空字符串
        if "-" in name:
            return name.split("-", 1)[1]  # 去掉前缀和 '-'
        return name  # 本来就没有 '-'

    if "-" in name:
        return keywords + name[name.find("-") :]

    return name  # 如果没有返回原名


def match_with_star(str1: str, str2: str) -> bool:
    """传入的两个字符串进行匹配，可变化的地方用*代替
    match_with_star("a*b*c", "axxxbxxxc")  # True
    """

    # 没有通配符，直接全等判断
    if "*" not in str1:
        return str1 == str2

    parts: list[str] = str1.split("*")

    position: int = 0

    # 处理第一个片段（如果不是以 * 开头，必须从头匹配）
    if parts[0]:
        if not str2.startswith(parts[0]):
            return False
        position = len(parts[0])

    # 处理中间片段
    for part in parts[1:-1]:
        if not part:
            continue
        idx = str2.find(part, position)
        if idx == -1:
            return False
        position = idx + len(part)

    # 处理最后一个片段（如果不是以 * 结尾，必须匹配结尾）
    if parts[-1]:
        return str2.endswith(parts[-1])

    return True
