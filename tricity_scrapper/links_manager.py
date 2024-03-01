import asyncio
import math
from network import create_session
from scrapper import scrap_items_links, scrap_items_count
from constants import ITEMS_PER_PAGE, FIRST_PAGE, LAST_PAGE, SCRAP_LIMIT_AT_ONE_TIME, SLEEP_TIME_BETWEEN_REQUESTS
from url_manager import get_url
from console_manager import update_last_message
from constants import ITEMS_PER_PAGE

async def get_items_links():
  session = await create_session()
  pages_amount = await get_pages_amount(session)
  first_page = FIRST_PAGE or 0
  last_page = LAST_PAGE if LAST_PAGE and LAST_PAGE < pages_amount else pages_amount
  links = await get_items_links_in_range(session, first_page, last_page)

  await session.close()
  return links

async def get_pages_amount(session):
  items_amount = scrap_items_count(await session.get_text(get_url(0)))

  return math.ceil(items_amount / ITEMS_PER_PAGE) 

async def get_items_links_in_range(session, first_page, last_page):
  links_amount = (last_page - first_page) * ITEMS_PER_PAGE
  semaphore = asyncio.Semaphore(SCRAP_LIMIT_AT_ONE_TIME)
  scrapped_links = 0

  async def get_page_links(url):
    nonlocal links_amount, scrapped_links
    async with semaphore:
      try:
        page = await session.get_text(url)
        scrapped_links+=ITEMS_PER_PAGE
        percentage = scrapped_links / links_amount * 100
        update_last_message(f'Scrapping items links... {percentage:.2f}%({scrapped_links})')
        return list(scrap_items_links(page))
      except Exception as e:
        print('During scraping links, an error occurred: ', e)
      finally:
        await asyncio.sleep(SLEEP_TIME_BETWEEN_REQUESTS)

  requests = [get_page_links(get_url(i)) for i in range(first_page, last_page)]
  pages_links = await asyncio.gather(*requests)
  links = []

  for page_links in pages_links:
    links.extend(page_links)
    
  return links
