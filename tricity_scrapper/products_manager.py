import asyncio
from constants import SCRAP_LIMIT_AT_ONE_TIME, SLEEP_TIME_BETWEEN_REQUESTS
from network import create_session
from scrapper import scrap_product
from console_manager import update_last_message

async def get_items_by_links(links):
  session = await create_session()
  semaphore = asyncio.Semaphore(SCRAP_LIMIT_AT_ONE_TIME)
  links_amount = len(links)
  scrapped_amount = 0
  broken_links = []
  
  async def get_product(url):
    nonlocal scrapped_amount, links_amount, broken_links
    async with semaphore:
      try:
        page = await session.get_text(url)
        scrapped_amount += 1
        percentage = scrapped_amount / links_amount * 100
        update_last_message(f'Scrapping items... {percentage:.2f}%({scrapped_amount})')
        return scrap_product(page)
      except Exception as e:
        broken_links.append(url)
        return None
      finally:
        await asyncio.sleep(SLEEP_TIME_BETWEEN_REQUESTS)
  
  requests = [get_product(link) for link in links]
  items = await asyncio.gather(*requests)
  
  await session.close()
  return items, broken_links