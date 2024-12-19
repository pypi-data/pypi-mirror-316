import re
def JSON_words(text):
    # 正则表达式来匹配英文单词
    word_pattern = re.compile(r'\w+')
    # 正则表达式来匹配中文字符
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    words = word_pattern.findall(text)
    chinese_chars = chinese_pattern.findall(text)
    return words, chinese_chars

 
def is_chinese_s(text):
    return bool(re.match('^[\u4e00-\u9fff]+$', text))