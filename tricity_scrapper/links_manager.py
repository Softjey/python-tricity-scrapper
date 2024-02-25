import asyncio
import math
from network import create_session
from scrapper import scrap_items_links, scrap_items_count
from constants import ITEMS_PER_PAGE, FIRST_PAGE, LAST_PAGE
from url_manager import get_url

async def get_items_links():
  session = await create_session()
  pages_amount = await _get_pages_amount(session)
  first_page = FIRST_PAGE or 0
  last_page = LAST_PAGE if LAST_PAGE and LAST_PAGE < pages_amount else pages_amount
  links = await _get_items_links_in_range(session, first_page, last_page)

  await session.close()
  return links

async def _get_pages_amount(session):
  items_amount = scrap_items_count(await session.get_text(get_url(0)))

  return math.ceil(items_amount / ITEMS_PER_PAGE) 

async def _get_items_links_in_range(session, first_page, last_page):
  async def get_page_links(url):
    page = await session.get_text(url)
    return list(scrap_items_links(page))

  requests = [get_page_links(get_url(i)) for i in range(first_page, last_page)]
  pages_links = await asyncio.gather(*requests)
  links = []

  for page_links in pages_links:
    links.extend(page_links)
    
  return links
