import hashlib
def md5_Key(message:str):
    try:
        md5 = hashlib.md5()  
        md5.update(message.encode('utf-8'))  
        return md5.hexdigest()  
    except:
        print('请下载库hashlib或者检查数据是否传入错误!')