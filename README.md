### Crawler 

+ python requests, beautifulsoup 문서보기

        http://docs.python-requests.org/en/master/
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        
+ 패키지 설치

        requests, beautifulsoup4 lxml 
        
        
+ GET 요청 결과, requests를 사용해 요청한 결과를 status_code 속성으로 출력하면 상태코드를 보여줌


+ url query parameters to dict python
> parse_ps : parse_qs()에는 쿼리스트링 문자열을 지정해 주어야 합니다.  리턴타입은 딕셔너리 타입입니다.

> parse_psl : 만약 쿼리스트링 변환 결과를 파라미터와-값 쌍으로 이루어진 튜플 리스트로 얻고 싶은 경우 parse_qsl()을 사용합니다.
               하나의 파라미터에 값이 여러개인 경우에도 여러개의 튜플이 됩니다.

        
    url을 query를 dict형식으로 만들기
    
    ex)
    
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    query = parse.urlsplit(url_detail).query
    query_dict = parse.parse_qs(query)
    no = query_dict['no'][0]
    print(no)