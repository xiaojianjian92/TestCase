import secrets

def generate_fs_uniquifier():
    return secrets.token_hex(16)  # 生成32字符的随机十六进制字符串