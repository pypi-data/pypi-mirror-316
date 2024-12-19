import requests
def Global_variable(ip,port,url_host):
    # 本地代理
    proxy={
        'http':f'http://{ip}:{port}',
        'https':f'https://{ip}:{port}'
    }
    print(proxy)
    if int(port)>0 and int(port)<=65535:
        req_text=requests.get(url=url_host,proxies=proxy,timeout=5)
        if req_text.status_code==200:
            return req_text.text
        else:
            print('数据获取失败!')
    else:
        print('端口号不合法!')

def Global_variable(ip_s,port_s,url_host):
    while True:
        for index_s in ip_s:
            for port in port_s:
                dit={
                    'http:':f'http://{index_s}:{port}',
                    'https':f'https://{index_s}:{port}'
                }
            try:
                    if url_host=='':
                        print('不能传入空网址!')
                    else:
                        req=requests.get(url=url_host,proxies=dit,timeout=5)
                        if req.status_code==200:
                            print('请求成功!')
                        else:
                            print('请求失败!')
            except:
                    print('代理错误!代理IP非官方IP或者IP有问题!请重试!')