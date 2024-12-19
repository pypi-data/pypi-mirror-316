from DrissionPage import ChromiumPage

page=ChromiumPage()
def Image_list(value_text:str):
    page.listen.start('tn=resultjson_com')
    page.get(f'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=result&fr=&sf=1&fmq=1734579028976_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word={value_text}')
    req=page.listen.wait().response.body
    return req
    
