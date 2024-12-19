def zidonghua_s(ip,port):
    if int(port)>0 and (port)<=65530:
        return f'http://{ip}:{port}'
    else:
        print('端口号不合法!')

def zidonghua(ip,port):
    if int(port)>0 and (port)<=65530:
        return f'https://{ip}:{port}'
    else:
        print('端口号不合法!')

def zidonghua_scanf_s(ip,port,value,value2):
    if value=='':
        print('参数数据不合法!')
    if value2=="":
        if int(port)>0 and (port)<=65530:
            return f'http://{ip}:{port}/{value}'
        else:
            print('端口号不合法!')
    if value2=="" and value=="":
        if int(port)>0 and (port)<=65530:
            return f'http://{ip}:{port}'
        else:
            print('端口号不合法!')
    else:
        if int(port)>0 and (port)<=65530:
            return f'http://{ip}:{port}/{value}?{value2}'
        else:
            print('端口号不合法!')


def zidonghua_scanf_ss(value:str,value2:str,value3):
    if value=='' and value2=='':
        return '数据错误!'
    if value3=="":
        return f'https://{value}/{value2}'
    else:
        return f'https://{value}/{value2}?{value3}'
