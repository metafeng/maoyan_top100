from bs4 import BeautifulSoup
import re
import requests
import pprint


class MaoYan(object):
    def __init__(self):
        pass

    def get_html(self, url):
        """
        获取html页面
        :param url: 请求链接
        :return: html页面
        """
        html = requests.get(url)
        return html

    def get_movies_pages(self):
        """
        获取Top100榜
        :return:
        """
        htmls = {}
        for i in range(0, 100, 10):
            url = f'https://maoyan.com/board/4?offset={i}'
            html = self.get_html(url)
            htmls[i] = html
        return htmls

    def get_movies_list(self, html):
        """
        获取每页电影列表
        """
        soup = BeautifulSoup(html.content, 'lxml')
        boards = soup.findAll('dd')
        return boards

    def regular_time(self, time):
        """
        部分电影日期带有国家, 例如：'1994-09-10(加拿大)'
        正则提取日期
        9, 42 上映日期只有年，没有具体到日
        """

        pattern = '^(([1-9]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))'
        try:
            matches = re.match(pattern, time, flags=0).group()
        except Exception as e:
            pattern = '^(([1-9]\d{3})-(0[1-9]|1[0-2]))'
            try:
                matches = re.match(pattern, time, flags=0).group() + '-01'
            except Exception as e:
                pattern = '^(([1-9]\d{3}))'
                matches = re.match(pattern, time, flags=0).group() + '-01-01'
        return matches

    def download(self, src, img_name):
        """
        下载图片
        """
        dir = './top_100_posters/' + str(img_name) + '.jpg'
        try:
            pic = requests.get(src, timeout=10)
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
            return '开始下载:' + str(img_name), src
        except requests.exceptions.ConnectionError as e:
            return e, 'ConnectionError:' + str(img_name) + 'download failed.'
        except OSError as e:
            return e, 'OSError:' + str(img_name) + 'download failed.'

    def get_movies_info(self, boards, movie_info, offset):
        """
        获取电影的名字，演员，分数，上映时间，海报url
        movie_info: 电影信息存储容器
        """
        for i in range(len(boards)):
            title = boards[i].find('p', class_='name').find('a').get('title')
            stars = boards[i].find('p', class_='star').contents[0].strip()[3:]
            score_1 = boards[i].find('i', class_='integer').contents[0]
            score_2 = boards[i].find('i', class_='fraction').contents[0]
            score = float(score_1 + score_2)
            release_time = boards[i].find('p',
                                          class_='releasetime').contents[0].strip()[5:]
            release_time = self.regular_time(release_time)
            img_url = boards[i].find(
                'img', class_='board-img').get('data-src').split('@')[0]
            ranking = offset + i + 1
            movie_info[ranking] = {
                'ranking': ranking,
                'title': title,
                'stars': stars,
                'score': score,
                'release_time': release_time,
                'img_url': img_url
            }
            download(img_url, str(ranking) + '_' + title)
        return movie_info


def crawling_movies():
    maoyan = MaoYan()
    htmls = maoyan.get_movies_pages()
    movie_info = {}
    for offset in htmls:
        boards = maoyan.get_movies_list(htmls[offset])
        movie_info = maoyan.get_movies_info(boards, movie_info, offset)
    return movie_info


if __name__ == '__main__':
    res = crawling_movies()
    pprint.pprint(res)
