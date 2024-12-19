import requests

def Files_date(url:str,value:str):
    with open(value,'rb') as file:
        file_s=file.read()
    req=requests.post(url,files={'file': file_s})
    try:
        if req.status_code==200:
            print('文件提交成功!')
        else:
            print(f'文件提交失败!,状态码:',{req.status_code},'原因为:',{req.text})
    except:
        print('发生错误信息!')


