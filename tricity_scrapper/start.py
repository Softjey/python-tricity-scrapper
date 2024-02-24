from network import create_session
from scrapper import get_links_to_products

async def start():
  session = await create_session()
  html = await session.get_text('https://ogloszenia.trojmiasto.pl/motoryzacja-sprzedam/?strona=0')
  links = get_links_to_products(html)

  print(links)

  await session.close()