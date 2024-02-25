from bs4 import BeautifulSoup

def _get_soup(html):
  return BeautifulSoup(html, 'lxml')

def scrap_items_links(html):
  soup = _get_soup(html)
  links_to_items = soup.find_all('a', attrs={'data-stats-ogl-id': True})
  hrefs = set()
  
  for link in links_to_items:
    hrefs.add(link.get('href'))
  
  return hrefs

def scrap_items_count(html):
  soup = _get_soup(html)
  count_text = soup.find('h1').find('span').text
  
  return int(count_text[2:-1])
  
  