import requests

response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)

# HTTP GET 요청으로 받아온 Content 를 text 데이터로 리턴
print(response.text)

# response.text 에 해당하는 데이터를
# weekday.html 이라는 파일에 기록
# 다 기록했으면 close() 호출

f = open('weekday.html', 'wt')
f.write(response.text)
f.close()

with open('weekday.html', 'wt') as f:
    f.write(response.text)
