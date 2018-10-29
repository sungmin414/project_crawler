import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail,
                 title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        """
        self.webtoon_id, self.no 요소를 사용하여
        실제 에피소드 페이지 URL을 리턴
        :return:
        """
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        # webtoon 속성 채우기 위해 webtoon_crawler() 실행
        # webtoon_crawler 함수 결과 dict()
        info = self.webtoon_crawler()
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']
        self.episode_list = list()

    def get_html(self):
        # HTML파일을 저장하거나 불러올 경로
        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        # HTTP요청을 보낼 주소
        url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
        # HTTP요청시 전달할 GET Parameters
        params = {
            'titleId': self.webtoon_id,
        }
        # -> 'http://com....nhn?titleId=703845

        # HTML파일이 로컬에 저장되어 있는지 검사
        if os.path.exists(file_path):
            # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
            html = open(file_path, 'rt').read()
        else:
            # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
            response = requests.get(url_episode_list, params)
            print(response.url)
            # 요청 응답객체의 text속성값을 html변수에 할당
            html = response.text
            # 받은 텍스트 데이터를 HTML파일로 저장
            open(file_path, 'wt').write(html)

        # 공통함수는 html을 리턴하도록 한다
        return html

    def webtoon_crawler(self):
        """
        self.webtoon_id를 사용해서
        웹툰 title, author,description를 딕셔너리 형태로 return
        :return:title, author, description 딕셔너리로
        """
        html = self.get_html()

        # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
        soup = BeautifulSoup(html, 'lxml')

        # 파일 저장하지 않고 진행하고 싶은 경우
        # 위에 코드를 다 주석으로 변경
        # 파일 저장안해도 되는 경우
        # url = 'http://comic.naver.com/webtoon/list.nhn'
        # params = {
        #     "titleId": webtoon_id
        # }
        # response = requests.get(url, params)
        # print(response.url)
        # soup = BeautifulSoup(response.text, 'lxml')

        # div.detail > h2 (제목, 작가)의
        #  0번째 자식: 제목 텍스트
        #  1번째 자식: 작가정보 span Tag
        #   Tag로부터 문자열을 가져올때는 get_text()
        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        # div.detail > p (설명)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        # webtoon title, author, description
        # 딕셔너리 형태로 return
        info = dict()
        info['title'] = title
        info['author'] = author
        info['description'] = description
        return info

    def episode_crawler(self):
        """
        webtoon_id를 매개변수로 각 에피소드의
        webtoon_id,no,title,url_thumbnail,rating 정보를 Episode 인스턴스로 생성 후
        list에 추가하여 return
        :return: Episode 인스턴스가 저장되어있는 List
        """

        # episode_crawler는 webtoon_crawler로 생성된 html 이용
        html = self.get_html()

        # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
        soup = BeautifulSoup(html, 'lxml')

        # 파일 저장안해도 되는 경우
        # 파일 저장하지 않고 실행하고 싶다면 위의 코드를 주석처리후 사용할것!
        # url = 'http://comic.naver.com/webtoon/list.nhn'
        # params = {
        #     "titleId": webtoon_id
        # }
        # response = requests.get(url, params)
        # print(response.url)
        # soup = BeautifulSoup(response.text, 'lxml')

        # 에피소드 목록을 담고 있는 table
        table = soup.select_one('table.viewList')

        # table내의 모든 tr요소 목록
        tr_list = table.select('tr')

        # list를 리턴하기 위해 선언
        # for문을 다 실행하면 episode_lists 에는 Episode 인스턴스가 들어가있음
        episode_lists = list()

        # 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
        for index, tr in enumerate(tr_list[1:]):
            # 에피소드에 해당하는 tr은 클래스가 없으므로,
            # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
            if tr.get('class'):
                continue

            # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            # 현재 tr의 첫 번째 td요소의 자식   a태그의 'href'속성값
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            # print(query_dict)
            no = query_dict['no'][0]

            # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            # 현재 tr의 네 번째 td요소의 내용
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            # 매 에피소드 정보를 Episode 인보스턴스로 생성
            # new_episode = Episode 인스턴스
            new_episode = Episode(
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )

            # episode_lists Episode 인스턴스들 추가
            episode_lists.append(new_episode)

        return episode_lists

    def update(self):
        """
        update 함수를 실행하면 해당 webtoon_id에 따른 에피소드 정보를 list에
        Episode 인스턴스들로 저장하고 self.episode_list 에 할당
       :return:
        """
        result = self.episode_crawler()
        self.episode_list = result


if __name__ == '__main__':
    webtoon1 = Webtoon(703846)
    print(webtoon1.title)
    webtoon1.update()
    for episode in webtoon1.episode_list:
        print(episode.url)