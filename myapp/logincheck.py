# ReadMe
# << biblebot api installation >>
# $ pip install 'biblebot[http]'


import asyncio
from biblebot import IntranetAPI

async def main(a, b):
    response = await IntranetAPI.Login.fetch(str(a), str(b))
    result = IntranetAPI.Login.parse(response)

    val = "ErrorData" in str(result) #로그인 여부 확인
    if val : 
        print("로그인 실패")
    else :
        print("로그인 성공")

a = 'cherryshine'
b = 'jee77546906'
asyncio.run(main(str(a), str(b)))