from urllib import parse

from bs4 import BeautifulSoup
import requests
import os


# HTML 파일을 저장하거나 불러올 경로
file_path = 'data/epsode_list.html'
# HTTP 요청을 보낼 주소
url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'


# HTTP 요청시 전달할 GET Parameters
params = {
    'titleId' : 626907,
}
# HTML 파일이 로컬에 저장되어 있는지 검사
if os.path.exists(file_path):
    # 저장되어 있다면, 해당 파일을 읽어서 html 변수에 할당
    html = open(file_path, 'rt').read()
else:
    # 저장되어 있지 않다면, requests 를 사용해 HTTP GET 요청
    response = requests.get(url_episode_list, params)
    # 요청 응답객체의 text 속성값을 html 변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTML 파일로 저장
    open(file_path, 'wt').write(html)

# BeautifulSoup 클래스형 객체 생성 및 soup 변수에 할당
soup = BeautifulSoup(html, 'lxml')

h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
# desc = soup.select_one('div.detail').h2.next_sibling
desc = soup.select_one('div.detail > p').get_text(strip=True)
# print(desc)
# print(type(desc))

# 에피소드 목록을 담고 있는 table
table = soup.select_one('table.viewList')
# table 내의 모든 tr 요소 목록
tr_list = table.select('tr')

# 첫 번째 tr 은 thead 의 tr 이므로 제외, tr_list 의 [1:]부터 순회
for index, tr in enumerate(tr_list[1:]):
    # 에피소드에 해당하는 tr 은 클래스가 없으므로,
    # 현재 순회중인 tr 요소가 클래스 속성값을 가진다면 continue
    if tr.get('class'):
        continue
    # 현재 tr 의 첫 번째 td 요소의 하위 img 태그의 'src' 속성값
    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    # 현재 tr 의 첫 번째 td 요소의 자식 a 태그의 'href'속성값
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    # url_parse = parse.urlsplit(url_detail)
    # url_parse_qs = dict(parse.parse_qsl(parse.urlsplit(url_detail).query))
    # url_numbers = url_parse_qs.get('no')
    query = parse.urlsplit(url_detail).query
    query_dict = parse.parse_qs(query)
    no = query_dict['no'][0]

    # 현재 tr 의 두 번째 td 요소의 자식 a 요소의 내용
    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    # 현재 tr 의 세 번째 td 요소의 하위 strong 태그 내용
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    # 현재 tr 의 네 번째 td 요소의 내용
    created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

    # print(url_thumbnail)
    # print(url_detail)
    # print(url_parse_qs)
    print(no)
    # print(title)
    # print(rating)
    # print(created_date)
