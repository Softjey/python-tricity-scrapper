import sys

def update_last_message(new_message):
  sys.stdout.write(f'\r{new_message}')
  sys.stdout.flush()
  
def print_message(message):
  sys.stdout.write(message)
  sys.stdout.flush()
  