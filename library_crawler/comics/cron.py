from django.core.mail import send_mail
from .models import Onepiece, Denma

# from django_cron import CronJobBase, Schedule
import mechanicalsoup


def onepiece():
	page_url = 'http://zangsisi.net/?page_id=3974'
	browser = mechanicalsoup.Browser()

	html = browser.get(page_url)
	html.raise_for_status()  # similar to assert login_page.ok but with full status code in case of failure.

	post = html.soup.select_one('div#post').select('p')[0].select('a')[0]

	latest = Onepiece.objects.latest('id')

	if post.text != latest.name:
		context = '''
ONEPIECE\n
{} updated!\n
{}
		'''.format(post.text, post['href'])

		send_mail(
			'Onepiece updated',
			context,
			'Django-crontab',
			['rotanev7@gmail.com'],
			fail_silently=False
		)
		latest.delete()
		Onepiece.objects.create(name=post.text)


def denma():
	page_url = 'http://comic.naver.com/webtoon/list.nhn?titleId=119874'
	browser = mechanicalsoup.Browser()

	html = browser.get(page_url)
	html.raise_for_status()  # similar to assert login_page.ok but with full status code in case of failure.

	post = html.soup.findAll('tr', {'class': None})[1].select('td')[1].select('a')[0]

	latest = Denma.objects.latest('id')

	if post.text != latest.name:
		context = '''
DENMA\n
{} updated!\n
http://comic.naver.com{}
		'''.format(post.text, post['href'])

		send_mail(
			'Denma updated',
			context,
			'Django-crontab',
			['rotanev7@gmail.com'],
			fail_silently=False
		)

		latest.delete()
		Denma.objects.create(name=post.text)


# class WebtoonCrawl(CronJobBase):
# 	RUN_EVERY_MINS = 1  # every 2 hours
# 	# RUN_AT_TIMES = ['11:30', '14:00', '23:15']

# 	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
# 	code = 'asnibmemipwln41dsiEcnbaic'    # a unique code

# 	def do(self):
# 		denma()
# 		onepiece()
