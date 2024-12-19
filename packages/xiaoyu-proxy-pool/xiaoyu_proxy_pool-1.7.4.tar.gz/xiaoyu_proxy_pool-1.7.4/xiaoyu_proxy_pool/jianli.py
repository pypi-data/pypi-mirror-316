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

import requests
import re

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
