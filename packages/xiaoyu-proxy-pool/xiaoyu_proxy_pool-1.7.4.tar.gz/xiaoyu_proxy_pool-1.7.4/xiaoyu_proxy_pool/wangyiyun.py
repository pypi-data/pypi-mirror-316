import requests
import time
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