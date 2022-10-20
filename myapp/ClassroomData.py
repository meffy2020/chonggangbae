import asyncio
from inspect import getclasstree
from biblebot import IntranetAPI
import re, requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


# 강의정보를 얻어오는 클래스
class Get_Classroom_Data :
    # 인트라넷에 로그인해 강의실정보 창 URL을 파싱하는 메서드
    async def getclass(id, password):

        # Login
        resp = await IntranetAPI.Login.fetch(id, password)
        result = IntranetAPI.Login.parse(resp)
        cookie = result.data["cookies"]

        # Get 강의실URL
        resp = await IntranetAPI.Course_plan.fetch(cookies=cookie)
        resp = str(resp)

        # <----강의계획서 페이지 파싱 및 Junk값 제거---->
        resp = resp[resp.find('비고') :]
        resp = resp.replace("<","\n<")
        resp = resp.replace('''<a href="javascript:goGD640(\\''', "")
        resp = resp.replace(" ","")
        resp = resp.replace("'","")
        resp = resp.replace("\\","")

        # <----줄바꿈문자 기준으로 문자열을 나눠 parsinglist에 리스트 형태로 저장---->
        parsinglist = list(resp.split("\n"))

        # <----리스트 형태로 저장된 값들중 GD640과 일치하는 값만 추출해 matching리스트에 저장---->
        matching = [s for s in parsinglist if "GD640" in s]

        # <----matching리스트에 저장된 값에는 URL 외에도 Junk값이 끝에 붙어있으므로 정리----> 
        # Junk Example>> );">월16:20~17:35'
        for i in range (len(matching)):
            k = int(matching[i].find(')'))
            matching[i] = matching[i][:k]
        return(matching)

    # 강의실정보창 Url 리스트를 분석해 과목명, 강의실, 교시를 추출해서 리스트에 저장하는 메서드
    def UrlListAnalysis(UrlList):
        UrlList = list(UrlList)
        k = int(len(UrlList))
        MyUrl = "http://kbuis.bible.ac.kr/GradeMng/"
        course_data = []
        for i in range(k): # Url리스트 길이만큼(과목개수만큼) 반복
            url = MyUrl + str(UrlList[i])
            x = list(url.split("&"))
            match_coursename = [s for s in x if "과목명=" in s]
            match_coursecode = [s for s in x if "haksuNo="in s]

            # 과목명과 과목코드는 URL로부터 파싱해서 저장함
            # Get 과목명
            coursename = match_coursename[0].replace('과목명=','') #과목명 추출됨

            # Get 과목코드
            coursecode = match_coursecode[0].replace('haksuNo=','')#과목코드 추출됨

            # 강의실정보와 강의시간은 URL에 접속해 크롤링해서 저장함
            webpage = requests.get(url)
            soup = BeautifulSoup(webpage.content, "html.parser", from_encoding='cp949')
            soup = soup(attrs={'class':'mbody'})
            soup = str(soup).replace("<","\n<")
            soup = soup.replace(">",">\n")
            soup = list(soup.split("\n"))

            # Get 강의시간
            day = ['월 ','화 ','수 ','목 ','금 ']
            coursetime = [s for s in soup if any(xs in s for xs in day)] #강의시간 추출됨

            # Get 강의실정보
            complex = ['밀알관','복음관','갈멜관','일립관','모리아관','기본간호실습실','보육실습실','천마홀','컴소실습실','수업행동분석실','로고스홀','교양정보','브니엘홀','종합실습실', '수업'] 
            courseroom = [s for s in soup if any(xs in s for xs in complex)] #강의실 추출됨

            # 폐강된 강의 걸러내기 
            # courseroom
            if len(courseroom) == 0:
                courseroom = '폐강된 강의입니다.'
            else:
                courseroom = courseroom[0]

            course_data.insert(i,list([coursename, coursecode, courseroom, coursetime]))
        # 모든 과목명 / 과목코드 / 강의실 / 강의시간 담긴 리스트 리턴
        return (course_data)

            # (디버깅용) 강의정보 출력해보기 test
            # print("-------------------------------------------------------------------")
            # print(coursename)
            # print(coursecode)
            # print(courseroom)
            # print(coursetime)