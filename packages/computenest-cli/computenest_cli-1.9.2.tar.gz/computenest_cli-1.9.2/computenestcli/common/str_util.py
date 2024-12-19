import re


class StrUtil:
    def __init__(self):
        pass

    # 将输入参数改为计算巢部署物允许的格式
    @staticmethod
    def sanitize_name(name):
        # 只允许字母、数字、下划线、和中划线
        pattern = r'[^\w-]+'
        # 替换不符合的字符为下划线
        sanitized_name = re.sub(pattern, '_', name)
        return sanitized_name
