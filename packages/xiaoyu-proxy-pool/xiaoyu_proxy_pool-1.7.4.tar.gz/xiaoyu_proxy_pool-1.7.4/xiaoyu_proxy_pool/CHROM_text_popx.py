from DrissionPage import ChromiumPage

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

