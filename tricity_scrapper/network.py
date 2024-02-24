import aiohttp

async def create_session():
  session = aiohttp.ClientSession()

  async def get_text(url):
    async with session.get(url) as response:
      return await response.text()

  session.get_text = get_text

  return session