import requests
import time
from DrissionPage import ChromiumPage
import re
import pandas as pd
import random
import uuid
import os
import pyautogui
import time
import hashlib
import time
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

def mp3_find(serch_text):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    url="http://music.163.com/api/search/get/"
    data = {
        's': serch_text,
        'type': 1,
        'offset': 0,
        'total': "true",
        'limit': 10
    }
    try:
        r=requests.post(url,headers=headers,data=data)
        print("网易云音乐列表链接正确！")
        json_result= r.json()
    except Exception as e:
        print("获取网易音乐列表时网络错误！",e)
        return
    song_list=json_result.get("result").get("songs")
    new_song_list=[]
    for i in song_list:
        new_song_dir={}
        new_song_dir["id"]=i.get("id")
        new_song_dir["name"]=i.get("name")
        new_song_dir["artists"]=""
        new_song_dir["fee"]=i.get("fee")
        for j in i.get("artists"):
            new_song_dir["artists"]+="/"+j.get("name")
            #拼接歌手
        new_song_dir["album"]=i.get("album").get("name")
        new_song_list.append(new_song_dir)
    return new_song_list

def mp3_id(nums):
    return 'https://music.163.com/#/song?id=1901371647'+nums
# 返回一个歌曲列表,自己在浏览器访问
def sums(value,value2,sum:str):
    if sum=='/':
        if value2==0:
            print('不能/0')
        else:
            return value/value2
    if sum=='+':
        return value+value2
    if sum=='-':
        return value-value2
    if sum=='*':
        return value*value2
def Image_list(value_text:str):
    page.listen.start('tn=resultjson_com')
    page.get(f'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=result&fr=&sf=1&fmq=1734579028976_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word={value_text}')
    req=page.listen.wait().response.body
    return req
    

def md5_re(value:str,value_md5):
    daipojie=hashlib.md5(value.encode())
    encrypted=daipojie.hexdigest()
    if encrypted==value_md5:
        return True
    else:
        print('失败!不正确!')
def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"  # 使用ip-api.com的API获取IP地理位置信息
    response = requests.get(url)
    data = response.json()
    if data["status"] == "success":
        country = data["country"]
        region = data["regionName"]
        city = data["city"]
        return f"{country}, {region}, {city}"
    else:
        return "未知IP!可能是局域网IP"
def md5_Key(message:str):
    try:
        md5 = hashlib.md5()  
        md5.update(message.encode('utf-8'))  
        return md5.hexdigest()  
    except:
        print('请下载库hashlib或者检查数据是否传入错误!')
def Jietugongju():
    # 等待1秒，确保鼠标悬停在想要截图的位置
    time.sleep(1)
 
    # 获取当前屏幕的截图，并将其保存为png文件
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

def Jietugongju_width_height(x,y,width,height):
    region_screenshot = pyautogui.screenshot(region=(x,y,width,height))
    region_screenshot.save('region_screenshot.png')

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
# 创建一个DataFrame
def text_json_list(data:str):
    try:
        data = data
        df = pd.DataFrame(data)
        df.to_csv('output.csv', index=False)
        return df
    except:
        print('数据错误!')

surnames = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
names = ['伟', '敏', '婷', '浩', '宇', '静', '磊', '娜', '杰', '丽']
def generate_random_str(randomlength=16):
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choices(base_str, k=randomlength))
def generate_random_name():
    surname = random.choice(surnames)
    name = random.choice(names)
    return surname + name
def generate_mock_json(id):
        return {
        "code": 0,
        "msg": "0",
        "message": "0",
        "ttl": 1,
        "data": {
            "unfollow_unread": str(id).zfill(6),
            "follow_unread": generate_random_name(),
            "unfollow_push_msg": 0,
            "dustbin_push_msg": 0,
            "dustbin_unread": 0,
            "biz_msg_unfollow_unread": 0,
            "biz_msg_follow_unread": 0,
            "custom_unread": 0,
            "key1": generate_random_str(),
            "key2": generate_random_str(),
        }
    }
def nick_name_id(rand_name_id):
    if rand_name_id<1:
         print('ERROR_参数有误!')
    else:
        print('文件生成成功!')
        data = {"code": "200", "msg": "success", "data": [generate_mock_json(i+1) for i in range(rand_name_id)]}
        return data


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


    
def mp3_find(serch_text):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    url="http://music.163.com/api/search/get/"
    data = {
        's': serch_text,
        'type': 1,
        'offset': 0,
        'total': "true",
        'limit': 10
    }
    try:
        r=requests.post(url,headers=headers,data=data)
        print("网易云音乐列表链接正确！")
        json_result= r.json()
    except Exception as e:
        print("获取网易音乐列表时网络错误！",e)
        return
    song_list=json_result.get("result").get("songs")
    new_song_list=[]
    for i in song_list:
        new_song_dir={}
        new_song_dir["id"]=i.get("id")
        new_song_dir["name"]=i.get("name")
        new_song_dir["artists"]=""
        new_song_dir["fee"]=i.get("fee")
        for j in i.get("artists"):
            new_song_dir["artists"]+="/"+j.get("name")
            #拼接歌手
        new_song_dir["album"]=i.get("album").get("name")
        new_song_list.append(new_song_dir)
    return new_song_list

def mp3_id(nums):
    return 'https://music.163.com/#/song?id=1901371647'+nums
# 返回一个歌曲列表,自己在浏览器访问


VERSION:int=1.74
DESCRIPTION:str='一个强大的工具集合包'
DESCRIPTION_Name:str='作者:小鱼程序员 欢迎下载使用!期待各位的友善建议,如果有啥优化建议,以及功能,可以提交到732355054@qq.com邮箱'

from pyquery import PyQuery as pq
INDEX_URL = "https://www.51386.com/"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
INDEX_URL = "https://www.51386.com/"
def jianli_Scode():
    url="https://www.51386.com/jlmb/"
    res = requests.request("GET",url=url, headers=HEADER)
    res.encoding = "utf-8"
    return res.text
def get_download_url(code):
    doc = pq(code)
    content = doc(".jlmblist")
    resume_dict = {}
    for resume in content.items():
        title = resume("a").attr("title")
        url = resume("a").attr("href")
        resume_dict[title] = f"{INDEX_URL}{url}?act=succ"
    return resume_dict



def get_resume_url(url):
    headers ={
        "referer": "https://www.51386.com/jlmb/4020.html?act=down"
    }
    res = requests.request("GET", url, headers=headers)
    try:
        deal = re.compile(r'"color:#08c" href="(?P<oss_url>.*?)">点击这里</a>',re.S)
        result = deal.search(res.text)
        oss_url = result.group("oss_url")
    except Exception as e:
        print(f"正则获取oss_url失败,{e}")
    return oss_url

def chrome():
    return 'https://googlechromelabs.github.io/chrome-for-testing/'

page=ChromiumPage()


class Text_Dip:
    index_page=0
    # 滑动类网页
    def Text_线程值(text_xpath,url_host):
        page.get(url=url_host)
        if Text_Dip.index_page==0:
            for indexIP in page.eles(f'x:{text_xpath}'):
                print(indexIP.text)
        else:
            return False

    def image_线程池1(text_xpath,url_host):
        page.get(url=url_host)
        if Text_Dip.index_page==0:
             for indexIP1 in page.eles(f'x:{text_xpath}'):
                print(indexIP1.attr('src'))
        else:
            return False

    def 综合数据处理(text_xpath,url_host):
        page.get(url=url_host)
        if Text_Dip.index_page==0:
            for indexIP1 in page.eles(f'x:{text_xpath}'):
                dit={
                    '个人信息':indexIP1.text,
                    '数据链接':indexIP1.attr('href'),
                    '图片链接':indexIP1.attr('src')
                }
        else:
            return False


