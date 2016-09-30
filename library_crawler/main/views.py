from django.shortcuts import HttpResponse
import datetime
import os
import mechanicalsoup
import urllib.parse as urlparse
from urllib.parse import urlencode


def main(request, *args, **kwargs):
    # context = {}
    context_str = ""

    browser = mechanicalsoup.Browser()

    room_list = []
    if 'room' in kwargs.keys():
        if kwargs['room'] == "1":
            for i in range(45, 49):
                room_list += [i]
        elif kwargs['room'] == "2":
            for i in range(49, 53):
                room_list += [i]
        elif kwargs['room'] == "3":
            for i in range(63, 73):
                room_list += [i]
        else:
            return HttpResponse('1,2,3 중 하나만 입력')
    else:
        for i in range(45, 53):
            room_list += [i]
        for i in range(63, 73):
            room_list += [i]

    if 'date' in kwargs.keys():
        if len(kwargs['date']) == 4:
            date = datetime.datetime.today().strftime('%Y') + kwargs['date']
        elif len(kwargs['date']) == 8:
            date = kwargs['date']
        else:
            return HttpResponse('yyyymmdd 혹은 mmdd 식으로 입력')
    else:
        date = datetime.datetime.today().strftime('%Y%m%d')

    # main url
    page_url = 'http://library.hanyang.ac.kr/studyroom/main'

    for rid in room_list:
        params = {
            'rId': rid,  # studyroom number
            'searchDate': date,  # date
        }

        # url에 parameter 붙이기
        url_parts = list(urlparse.urlparse(page_url))
        url = urlparse.urlunparse(url_parts) + '?' + urlencode(params)

        # request library login page.
        print(url)
        html = browser.get(url)
        html.raise_for_status()  # similar to assert login_page.ok but with full status code in case of failure.

        # login_page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
        # we grab the login form
        login_form = html.soup.select_one('form#login')
        if login_form:
            print('--- login required ---')
            # specify username and password
            login_form.find("input", {"name": "id"})["value"] = os.environ.get('HYU_ID')
            login_form.find("input", {"name": "password"})["value"] = os.environ.get('HYU_PW')

            # submit form
            html = browser.submit(login_form, html.url)

            # 예약 가능일이 아니거나 공휴일인 경우는 바로 리턴
            if html.soup.find(class_='noticeW').find('span', style="font: bold; color: red;"):
                return HttpResponse("예약 가능일이 아님")
            elif html.soup.find(class_='listtable').find('tbody').text.strip() == "":
                return HttpResponse("공휴일은 스터디룸이 없음")

        context_str += str(rid) + "<br>" + str(html.soup.find(class_='listtable'))
        # context.update({str(rid): str(html.soup.find(class_='listtable'))})

    return HttpResponse(context_str)
    # return render(request, 'main/main.html', context)
