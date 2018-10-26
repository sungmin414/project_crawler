import os

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        info = self.webtoon_crawler()
        self.title = info['title']
        self.author = info['author']
        self.desc = info['desc']

    def webtoon_crawler(self):
        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        url = 'https://comic.naver.com/webtoon/list.nhn'
        parmas = {
            'titleId': self.webtoon_id,
        }

        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            response = requests.get(url, parmas)
            html = response.text
            open(file_path, 'wt').write(html)

        soup = BeautifulSoup(html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        desc = soup.select_one('div.detail > p').get_text(strip=True)
        webtoon_dict ={
            'title': title,
            'author': author,
            'desc': desc,
        }
        # info = dict()
        # info['title'] = title
        # info['author'] = author
        # info['desc'] = desc
        return webtoon_dict


if __name__ == '__main__':
    a = Webtoon(641253)
    print(a.title)
    print(a.author)
    print(a.desc)





