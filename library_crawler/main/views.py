import datetime
import os
import threading

import urllib.parse as urlparse

from collections import OrderedDict
from urllib.parse import urlencode

from django.shortcuts import HttpResponse

import mechanicalsoup


class MyThread(threading.Thread):
    def __init__(self, threadid, name, counter, room_list, date):
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.name = name
        self.counter = counter
        self.room_list = room_list
        self.date = date

    def run(self):
        self.result_str = get_result(self.room_list, self.date)

    def join(self):
        threading.Thread.join(self)
        return self.result_str


def get_result(room_list, date):
    result_str = ""
    context = OrderedDict()

    page_url = 'http://library.hanyang.ac.kr/studyroom/main'

    browser = mechanicalsoup.Browser()

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

            try:
                if html.soup.find(class_='noticeW') is None:
                    raise AttributeError
            except AttributeError as e:
                print(e)
                return "비밀번호 틀림"

            # 예약 가능일이 아니거나 공휴일인 경우는 바로 리턴
            if html.soup.find(class_='noticeW').find('span', style="font: bold; color: red;"):
                return "예약 가능일이 아님"
            elif html.soup.find(class_='listtable').find('tbody').text.strip() == "":
                return "공휴일은 스터디룸이 없음"

        if 45 <= rid <= 48:
            link = "<a href=\"" + url + "\" target=\"_blank\">백남 스터디룸 " + str(rid - 44) + "</a>"
            # context['baeknam'] += rid - 44

        elif 49 <= rid <= 52:
            link = "<a href=\"" + url + "\" target=\"_blank\">법학 스터디룸 " + str(rid - 48) + "</a>"
            # context['law'] += str(rid - 48)
        else:
            link = "<a href=\"" + url + "\" target=\"_blank\">Creative Zone " + str(rid - 62) + "</a>"
            # context['creative'] += str(rid - 62)
        result_str += link + "<br>" + str(html.soup.find(class_='listtable')) + "<br><br>"

    return "<div class=\"inline\">" + result_str + "</div>"


def main(request, *args, **kwargs):
    print(datetime.datetime.now())

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

    thread1 = MyThread(1, "Thread-1", 1, room_list[0::4], date)
    thread2 = MyThread(2, "Thread-2", 2, room_list[1::4], date)
    thread3 = MyThread(3, "Thread-3", 3, room_list[2::4], date)
    thread4 = MyThread(4, "Thread-4", 4, room_list[3::4], date)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    result_str1 = thread1.join()
    result_str2 = thread2.join()
    result_str3 = thread3.join()
    result_str4 = thread4.join()

    print(datetime.datetime.now())

    css = "<html><head><style type=\"text/css\">.inline {float: left;display: inline-block;width: 25%;}</style></head><body>"

    if result_str1 == "예약 가능일이 아님" or result_str1 == "공휴일은 스터디룸이 없음" or result_str1 == "비밀번호 틀림":
        final_str = result_str1
    else:
        final_str = css + result_str1 + result_str2 + result_str3 + result_str4 + "</body></html>"

    # return

    return HttpResponse(final_str)
