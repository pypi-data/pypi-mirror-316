import requests
import random
# 这里文件后期可能会被弃用
import uuid
import os
def mac_id_random():
    # 生成一个随机的UUID
    raw_uuid = uuid.uuid4()
    # 将UUID转换为16字节格式
    hex_str = str(raw_uuid).replace('-', '')
    # 将16字节的UUID转换为mac地址的格式，即前六位是厂商ID，后六位是序列号
    mac = ":".join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
    # 返回格式化后的MAC地址
    return mac
def _path(file_path):
        if os.path.exists(file_path):
                print('文件存在!')
        else:
            os.mkdir(file_path)
def get_ip(ip_address,port):
        return 'http://'+ip_address+':'+port
    # 这是关于http的
def get_ips(ip_address,port):
        return 'https://'+ip_address+':'+port
def proxy_url(proxy_url,ip_address_url):
        # 指定的配置好的代理池
        proxies={
            'http':proxy_url,
            'https':proxy_url
        }
        response=requests.get(ip_address_url,proxies=proxies)
        return response.text
def proxy_file(proxy_file):
        # 读取代理池文件
        try:
            with open(proxy_file,'r') as f:
                lines=f.readlines()
            return lines
        except:
            print('ERROR IS NOT FILE FOUND !!!找不到指定文件!')
def Proxy_ua():
            ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
            ]
            user_agent = random.choice(ua_list)
            return user_agent