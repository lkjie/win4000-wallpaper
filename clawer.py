import logging
import requests
from lxml import etree
import json
from multiprocessing.dummy import Pool
import sys

'''
'http://www.win4000.com/mobile_detail_153000_1.html'
http://www.win4000.com/mobile_detail_ 153000 - 154050
'''
seed_url_FMT = 'http://www.win4000.com/mobile_detail_%d_1.html'
seed_url_FMT2 = 'http://www.win4000.com/mobile_detail_%d_%d.html'


def task(pageid):
    surl = seed_url_FMT % pageid
    allnum = getdetails(surl)
    for j in range(2, allnum + 1):
        getdetails(seed_url_FMT2 % (pageid, j))
        # json.dump(jpglist, open('results.json', 'a'), ensure_ascii=False, indent=4)


def getdetails(url, need_num=True):
    try:
        page = requests.get(url)
        html_data = etree.HTML(page.text)
        content = html_data.xpath('//*[@id="pic-meinv"]/a/img')
        if not content:
            return
        jpgurl = content[0].attrib['url']
        title = content[0].attrib['title'] + str(html_data.xpath('//*[@class="ptitle"]/span/text()')[0])
        res = dict(title=title,
                   url=jpgurl,
                   source=url)
        '''
        download picture
        '''
        r = requests.get(jpgurl)
        with open('./images/%s.jpg'%title, 'wb') as f:
            f.write(r.content)
        logging.info(res)
        if need_num:
            return int(html_data.xpath('//*[@class="ptitle"]/em/text()')[0])
    except Exception as e:
        logging.error(e)



def main():
    p = Pool(processes=10)  # 创建5条进程

    for i in range(154000, 154050):
        p.apply_async(task, args=(i,))  # 向进程池添加任务

    p.close()  # 关闭进程池，不再接受请求
    p.join()  # 等待所有的子进程结束


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=open('log', 'w'))
    main()