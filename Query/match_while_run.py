import asyncio
import json

import xlsxwriter

import aiohttp

from understat import Understat

page = 16000

async def main():
    global page
    while page != 16011:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            understat = Understat(session)
            players = await understat.get_match_shots(page)
            f = open(f"json/match/match{page}.json", "w")
            f.write(json.dumps(players))
            f.close()
            page = page + 1

loop = asyncio.get_event_loop()
loop.run_until_complete(main())