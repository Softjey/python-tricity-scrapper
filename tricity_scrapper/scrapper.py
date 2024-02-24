from bs4 import BeautifulSoup

def get_links_to_products(html):
  soup = BeautifulSoup(html, 'lxml')
  links_to_products = soup.find_all('a', attrs={'data-stats-ogl-id': True})
  hrefs = set()
  
  for link in links_to_products:
    hrefs.add(link.get('href'))
  
  return hrefs