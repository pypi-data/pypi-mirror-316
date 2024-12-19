import requests
 
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