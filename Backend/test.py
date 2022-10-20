import requests
from bs4 import BeautifulSoup

login_url = '로그인페이지주소/login.aspx'
crawl_url = '크롤링할주소\Status.aspx'

login_info = {
'Txt_1': '아이디',
'Txt_2': '비밀번호'
}

with requests.Session() as ss:
    req = ss.post(login_url, data=login_info, verify=False)
    if(req.status_code == 200):
        soup = BeautifulSoup(req.content, 'html.parser')
       _FORM = soup.select('p')