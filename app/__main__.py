from datetime import datetime
import os
import requests

#from MySQLdbHelper import MySQLdbHelper

from bs4 import BeautifulSoup

class Concerts():
	def __init__(self, club, source, url, selectors):
		self.club = club
		self._pages = []
		self.selectors = selectors
		self.source = source
		self.today = datetime.today()
		self.url = url

	def save_html(self, path, html, filename):
		file = open(os.path.join(path, filename),'w')
		file.write(str(html.prettify().encode('utf-8')))
		file.close()

	def _before(self):
		path = self.source
		if not os.path.exists(path):
			os.makedirs(path)

		path = os.path.join(path, self.club)
		if not os.path.exists(path):
			os.makedirs(path)

		pages = self._get_pages(path)

		return pages

	def _get_pages(self, path, page=1, soup=None):
		proceed = True
		if soup:
			if self.selectors['pager']:
				if not soup.select(self.selectors['pager']):
					proceed = False
			else:
				proceed = False

		if proceed:
			soup = self._get_page(path, page)
			self._get_pages(path, page+1, soup)

		return self._pages

	def _get_page(self, path, page):
		filename = self.today.strftime('%d%b%Y') + str(page) + '.html'
		if os.path.isfile(os.path.join(path, filename)):
			# Get html from file
			soup = self._get_page_from_file(os.path.join(path, filename))
		else:
			# Get html from web
			soup = self._get_page_from_web(page)
			self.save_html(path, soup, filename)

		self._pages.append(soup)

		return soup

	def _get_page_from_file(self, filename):
		return BeautifulSoup(open(filename), 'html.parser')

	def _get_page_from_web(self, page):
		url = self.url# + '&page=' + str(page)
		r = requests.get(url)
		return BeautifulSoup(r.text, 'html.parser')

	# EVENTIM
	# def process(self):
	# 	pages = self._before()

	# 	for page in pages:
	# 		for row in page.select(self.selectors['items']):
	# 			date = row.select(self.selectors['date'])[0].text.replace('\\n', '').strip()
	# 			date = datetime.strptime(date, self.selectors['date_format'])
	# 			band = row.find(self.selectors['band']).text.encode('UTF-8').decode('UTF-8').replace('\\n', '').strip()
	# 			venue = row.select(self.selectors['venue'])[0].text.replace('\\n', '').strip()

	# 			helper = MySQLdbHelper()
	# 			helper._query()
	# 			try:
	# 				helper.save({
	# 					'date': date,
	# 					'band': band,
	# 					'venue': venue
	# 				})
	# 			except:
	# 				pass

	# MOLOTOW
	def process(self):
		pages = self._before()

		for page in pages:
			for some in page.select('#replaced'):
				print(some)

			for row in page.select(self.selectors['items']):
				date = row.select(self.selectors['date'])[0].text.replace('\\n', '').strip()
				date = datetime.strptime(date, self.selectors['date_format'])
				
				for col in row.select(self.selectors['band']):
					band = col.text.replace('\\n', '').strip()

				if self.selectors['venue']:
					venue = row.select(self.selectors['venue'])[0].text.replace('\\n', '').strip()
				else:
					venue = self.club

				print(venue)
				print(date)
				print(band)

				# helper = MySQLdbHelper()
				# helper._query()
				# try:
				# 	helper.save({
				# 		'date': date,
				# 		'band': band,
				# 		'venue': venue
				# 	})
				# except:
				# 	pass

def run():
	# clubs = ['docks','molotow','markthalle']
	# source = 'eventim'

	# selectors = {
	# 	'pager': '#pager li.nextPage',
	# 	'items': '#serp li.group-item.event-item',
	# 	'band': 'h3',
	# 	'venue': '.item-city',
	# 	'date': '.item-date',
	#	'date_format': '%d.%m.%y - %H:%M Uhr'
	# }

	# for club in clubs:
	# 	url = 'http://www.eventim.de/tickets.html?doc=search&fun=search&action=grouped&fuzzy=yes&inline=false&suchbegriff='+club+'&ort=Hamburg&group=event'

	# 	c = Concerts(club=club, source=source, url=url, selectors=selectors)
	# 	c.process()

	selectors = {
		'pager': None,
		'items': '#replaced',
		'band': '.PartyKonzert .div_title',
		'venue': None,
		'date': '.div_date',
		'date_format': '%a, %d.%m.%Y'
	}

	url = 'http://molotowclub.com/programm/programm.php'
	c = Concerts(club='molotow', source='molotow', url=url, selectors=selectors)
	c.process()	

if __name__ == '__main__':
	import locale
	locale.setlocale(locale.LC_TIME, "de_DE")
	run()
