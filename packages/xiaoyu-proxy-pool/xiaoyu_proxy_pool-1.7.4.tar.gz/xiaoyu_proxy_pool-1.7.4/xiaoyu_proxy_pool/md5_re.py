import hashlib
def md5_re(value:str,value_md5):
    daipojie=hashlib.md5(value.encode())
    encrypted=daipojie.hexdigest()
    if encrypted==value_md5:
        return True
    else:
        print('失败!不正确!')