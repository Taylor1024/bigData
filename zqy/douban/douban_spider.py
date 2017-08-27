import requests
from bs4 import BeautifulSoup
from PIL import Image
import time
import numpy as np
import re


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'
}

session = requests.Session()
session.headers.update(headers)

url = 'https://accounts.douban.com/login'

# 豆瓣的用户名以及登录密码 
username = input('请输入你的用户名：')
password = input('请输入你的密码：')
# example
# username = '15062984159'
# password = 'zang805892567'


def get_captcha(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    captcha_link = soup.select('#captcha_image')[0]['src']
    # captcha_link = soup.find('img',{'id': 'captcha_image'}).attrs['src']
    captcha_id = soup.select('div.captcha_block > input')[1]['value']
    # captcha_id = soup.find('input', {'name': 'captcha-id'}).attrs['value']
    return captcha_id, captcha_link


def login(username, password, source='index_nav', redir='https://www.douban.com/', login='登录'):
    # params = {'source': 'movie', 'redir': 'https://movie.douban.com/', 'form_email': username,
    #        'form_password': password, 'login': '登录'}
    data = {                    #需要传去的数据
        'source':source,
        'redir':redir,
        'form_email':username,
        'form_password':password,
        'login':login,
    }

    captcha_id, captcha_link = get_captcha(url)
    if captcha_id:
        img_html = session.get(captcha_link)
        with open('captcha.jpg','wb') as f:
            f.write(img_html.content)
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print('打开错误')
        captcha = input("请输入验证码： ")
        data['captcha-id'] = captcha_id
        data['captcha-solution'] = captcha
    html = session.post(url, data=data, headers=headers)
    print(session.cookies.items())
    # print(html.text)


def get_page(page_num=0):
    login(username, password)
    now_time = time.strftime('%Y-%m-%d-%H-%M')
    content = requests.get('https://movie.douban.com/subject/26363254/comments')
    mysoup = BeautifulSoup(content.text, 'lxml')
    want_watch = mysoup.find('ul', {'class': 'fleft CommentTabs'}).find('span').string
    has_watched = mysoup.find('ul', {'class': 'fleft CommentTabs'}).find('a').string
    print(want_watch)
    print(has_watched)

    append_info = "战狼二此时想看的人数为：" + str(want_watch) + '\n' + "已经看过的人数为：" + str(has_watched) +'\n'\
    + "当前系统抓取时间为" + str(now_time) + '\n'
    with open('data_append.csv', 'at') as s:
        s.write(append_info)

    while(page_num>=0):
        time.sleep(np.random.rand() * 5)
        url = 'https://movie.douban.com/subject/26363254/comments?start=' + str(page_num * 20) + '&limit=20&sort=new_score&status=P'
        r = session.get(url)
        data =r.text
        soup = BeautifulSoup(data, "lxml")
        all_td = soup.findAll('div', {'class': 'comment-item'})

        for line in all_td:
            id = line.attrs['data-cid']
            avatar_link = line.find('div', {'class': 'avatar'}).a.attrs['href']
            comment_info = line.find('span', {'class': 'comment-info'})
            name = comment_info.find('a').string
            try:
                star = comment_info.find('span', {'class': re.compile('allstar[0-9]+\srating')}).attrs['class']
            except:
                star = ['allstar30', 'rating']
            str_star = str(star[0]).replace('allstar', '')
            comment_time = comment_info.find('span', {'class': 'comment-time'})
            date_time = comment_time.attrs['title']
            votes = line.find('span', {'class': 'votes'}).string
            try:
                comment = line.p.get_text().replace(' ', '').replace('\n', '')
            except:
                comment = ''
            info = str(id) + ', ' + str(name) + ', ' + str_star + ', ' + str(votes) + ', ' + str(
                date_time) + ', ' + str(comment) + ', ' + str(avatar_link)
            last_info = info.replace('\n', '') + '\n'
            print(last_info)

            if last_info == None:
                break

            # with open('10.csv', 'at') as s:
            with open('data.csv', 'at') as s:
                s.write(last_info)
        page_num += 1
        print('正在下载第 %d 页' %page_num)


if __name__ == '__main__':
    # page_num参数为开始爬取的页数，爬取过程中出现问题时修改爬取页数即可
    get_page(page_num=7033)
