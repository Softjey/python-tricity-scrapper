from bs4 import BeautifulSoup

def _get_soup(html):
  return BeautifulSoup(html, 'lxml')

def scrap_items_links(html):
  soup = _get_soup(html)
  links_to_items = soup.find_all('a', attrs={'data-stats-ogl-id': True})
  hrefs = set(map(lambda link: link.get('href'), links_to_items))
    
  return hrefs

def scrap_items_count(html):
  soup = _get_soup(html)
  count_text = soup.find('h1').find('span').text
  
  return int(count_text[2:-1])
  
def scrap_product(html):
  soup = _get_soup(html)

  return {
    'id': scrap_id(soup),
    'title': scrap_title(soup),
    'price': scrap_price(soup),
    'auction': scrap_is_auction(soup),
    'photos':  scrap_photos(soup),
    'properties': scrap_properties(soup),
    'description': scrap_description(soup),
    'location': scrap_location(soup),
  }
  
def scrap_id(soup):
  return soup.find(class_ = 'oglStats__col').find('span').text
  
def scrap_location(soup):
  return soup.find(class_ = 'oglField--address').find('div').contents[-1].text
  
def scrap_description(soup):
  return soup.find(class_ = 'ogl__description').contents[0].strip() 

def scrap_properties(soup):
  names = soup.find_all(class_ = 'oglField__name')[1:-1]
  values = soup.find_all(class_ = 'oglField__value')

  return {name.text.strip(): value.text.strip() for name, value in zip(names, values)}

def scrap_price(soup):
  return soup.find(class_ = 'oglDetailsMoney').contents[0].strip()

def scrap_is_auction(soup):
  return soup.find(class_ = 'oglDetailsMoneyNegotiation') is not None

def scrap_title(soup): 
  return soup.find('h1').text

def scrap_photos(soup):
  photos_nodes = soup.find_all('a', attrs={'data-fancybox': 'photo'})

  return list(map(lambda node: node.get('href'), photos_nodes))
  
  