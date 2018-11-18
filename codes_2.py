# 获取瓜子二手车车辆信息
# 写入MySQL

import requests
import re
# 使用正则来获取数据
import pymysql
# 写入数据库

# 与数据库建立连接
db = pymysql.connect(host='localhost', user='root', database='secar', password='1234', port=3306)
cursor = db.cursor()

cursor.execute('create database secar;')
# 如果存在了这个数据库
# 在执行时会报错‘已存在库’
db.commit()
cursor.execute('use secar;')
cursor.execute('drop table if exists secarta')
# 这句是判断是否存在数据表，如果存在，删了原来的，在下边重新创建
cursor.execute('create table secarta(id int(10) unsigned not null auto_increment primary key,'
               '车型 varchar(60) not null,'
               '里程 varchar(30) not null,'
               '价格 varchar(30) not null);')
db.commit()
# 注意写 commit()

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Referer': 'https://www.guazi.com/ningde/buy/o2i7/',
    'Host': 'www.guazi.com',
    'Cookie': 'cityDomain=ningde; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%2'
              '2%3A%22tbmkbturl%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%2'
              '2%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_camp'
              'aign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2'
              'C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22'
              'ca_transid%22%3Anull%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2'
              'C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_fla'
              'g%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%224909a78'
              '7-18cf-400d-bb2d-22b26fa9e908%22%2C%22sessionid%22%3A%22270cd450-9b'
              'f2-444f-8c51-0a15e2bb2358%22%7D; clueSourceCode=10103000312%2300; uu'
              'id=4909a787-18cf-400d-bb2d-22b26fa9e908; antipas=BW5813910s815829917'
              'Ee83X721w; preTime=%7B%22last%22%3A1542525378%2C%22this%22%3A1542525'
              '346%2C%22pre%22%3A1542525346%7D; ganji_uuid=6743652156044486307993; s'
              'essionid=270cd450-9bf2-444f-8c51-0a15e2bb2358; lg=1; close_finance_popup=2018-11-18'
}
# url = 'https://www.guazi.com/ningde/buy/o1i7/'
urllist = list(map(lambda x: 'https://www.guazi.com/ningde/buy/o{}i7/'.format(x), [n for n in range(1, 6)]))
# 创建url列表
info = []
# 存放所有正则获取的信息

# 获取每页的信息并存入列表


def getinfo(url):
    ht = requests.get(url, headers=head)
    ht.encoding = 'utf-8'
    hts = ht.text
    res = re.findall(r'<a title="(.*?)" hr(.|\n)*?">\|</span>(.*?)</div>(.|\n)*?<p>(.*?)<span>万</span></p>', hts)
    return res

# 信息汇总


def main():
    global info
    for link in urllist:
        info += getinfo(link)
    return info


infolist = main()
# 写入数据库
# 注意查看信息列表里的内容
for item in infolist:
    a = item[0]
    b = item[2]
    c = item[4]
    sql = 'insert into secarta(车型,里程,价格) values(%s,%s,%s)'
    cursor.execute(sql, (a, b, c))
    db.commit()
    # f.write('{},{},{},{},{},{}\n'.format('车型', item[0], '里程', item[2], '价格', item[4]))
db.close()
# 注意关闭数据库
