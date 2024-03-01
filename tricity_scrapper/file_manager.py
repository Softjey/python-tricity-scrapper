import os
import simplejson

def write_products_in_file(products, path):
  with open(os.path.abspath(path), "w", encoding='utf-8') as json_file:
    simplejson.dump(products, json_file, ensure_ascii=False)