import asyncio
import json

import xlsxwriter

import aiohttp

from understat import Understat

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)
        players = await understat.get_match_shots(16455)

        f = open("json/match/match16455.json", "w")
        f.write(json.dumps(players))

        f.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())