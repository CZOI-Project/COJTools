def format_number(num):
    # 判断数字是否已经有小数部分
    if num != int(num):
        # 如果有小数部分，保留一位小数
        return round(num, 1)
    else:
        # 如果没有小数部分，保留整数
        return int(num)


def get_time_text(num):
    if num <= 9999:
        return f"{num}ms"
    else:
        return f"{format_number(num / 1000)}s"


def get_mem_text(num):
    if num <= 999:
        return f"{num}KB"
    else:
        return f"{format_number(num / 1024)}MB"
