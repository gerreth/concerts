from datetime import datetime
import os
import requests

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
		file = open(os.path.join(path, filename),"w") 
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
			if not soup.select(self.selectors['pager']):
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
		return BeautifulSoup(open(filename), "html.parser")

	def _get_page_from_web(self, page):
		url = self.url + '&page=' + str(page)
		r = requests.get(url)
		return BeautifulSoup(r.text, "html.parser")

	def process(self):
		pages = self._before()

		for page in pages:
			for row in page.select(self.selectors['items']):
				date = row.select(self.selectors['date'])[0].text.replace('\\n', '').strip()
				date = datetime.strptime(date, '%d.%m.%y - %H:%M Uhr')

				band = row.find(self.selectors['band']).text.encode('UTF-8').decode('UTF-8').replace('\\n', '').strip()

				location = row.select(self.selectors['location'])[0].text.replace('\\n', '').strip()

				print(location)
				print(date)
				print(band)

def run():
	clubs = ['molotow','markthalle']
	club = 'markthalle'
	source = 'eventim'
	url = 'http://www.eventim.de/tickets.html?doc=search&fun=search&action=grouped&fuzzy=yes&inline=false&suchbegriff='+club+'&ort=Hamburg&group=event'

	selectors = {
		'pager': '#pager li.nextPage',
		'items': '#serp li.group-item.event-item',
		'band': 'h3',
		'location': '.item-city',
		'date': '.item-date'
	}

	selectors = {
		'pager': '#pager li.nextPage',
		'items': '#replaced .Konzert',
		'band': 'div_title',
		'location': '.item-city',
		'date': '.item-date'
	}

	c = Concerts(club=club, source=source, url=url, selectors=selectors)
	c.process()

if __name__ == '__main__':
	run()