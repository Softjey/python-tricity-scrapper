from constants import PATH, BROKEN_LINKS_PATH
from links_manager import get_items_links
from products_manager import get_items_by_links
from file_manager import write_products_in_file
from console_manager import print_message

async def main():
  links = await get_items_links()
  print_message('\n')
  items, broken_links = await get_items_by_links(links)
  
  print('\nSaving items to file...')
  write_products_in_file(items, PATH)
  print(f'File was successfully saved on! You can find it in {PATH}')
  if (len(broken_links) > 0):
    print(f'Some of the was\'nt scrapped items were saved on {BROKEN_LINKS_PATH}')
    write_products_in_file(broken_links, BROKEN_LINKS_PATH)