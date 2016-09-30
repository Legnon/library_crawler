from django.shortcuts import render, HttpResponse
import datetime
import os
import mechanicalsoup
import urllib.parse as urlparse
from urllib.parse import urlencode


def main(request):
    context = {}
    context_str = ""

    browser = mechanicalsoup.Browser()

    room_list = []
    for i in range(45, 53):
        room_list += [i]
    for i in range(63, 73):
        room_list += [i]
    today = datetime.datetime.today().strftime('%Y%m%d')

    # main url
    page_url = 'http://library.hanyang.ac.kr/studyroom/main'

    for rid in room_list:
        params = {
            'rId': rid,  # studyroom number
            'searchDate': today,  # date
        }

        # url에 parameter 붙이기
        url_parts = list(urlparse.urlparse(page_url))
        url = urlparse.urlunparse(url_parts) + '?' + urlencode(params)

        # request github login page. the result is a requests.Response object http://docs.python-requests.org/en/latest/user/quickstart/#response-content
        print(url)
        html = browser.get(url)
        html.raise_for_status()  # similar to assert login_page.ok but with full status code in case of failure.

        # login_page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
        # we grab the login form
        login_form = html.soup.select_one('form#login')
        if login_form:
            print('--- login needed ---')
            # specify username and password
            login_form.find("input", {"name": "id"})["value"] = os.environ.get('HYU_ID')
            login_form.find("input", {"name": "password"})["value"] = os.environ.get('HYU_PW')

            # submit form
            html = browser.submit(login_form, html.url)

        context_str += str(rid) + "<br>" + str(html.soup.find(class_='listtable'))
        # context.update({str(rid): str(html.soup.find(class_='listtable'))})

    # print(context)
    return HttpResponse(context_str)
    # return render(request, 'main/main.html', context)
