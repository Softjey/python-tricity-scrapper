from links_manager import get_items_links

async def main():
  print('Scrapping items links...')
  links = await get_items_links()
  print(f'Was scrapped {len(links)} items!')
