# import asyncio
# import time
# import random
# import siridb.connector
#
# async def example(siri):
#     # Start connecting to SiriDB.
#     # .connect() returns a list of all connections referring to the supplied
#     # hostlist. The list can contain exceptions in case a connection could not
#     # be made.
#     await siri.connect()
#
#     try:
#         # insert
#         ts = int(time.time())
#         value = random.random()
#         await siri.insert({'some_measurement': [[ts, value]]})
#
#         # query
#         resp = await siri.query('select * from "some_measurement"')
#         print(resp)
#
#     finally:
#         # Close all SiriDB connections.
#         siri.close()
#
#
# siri = siridb.connector.SiriDBClient(
#     username='sjrbc-writer',
#     password='sjrbc-writer',
#     dbname='sjrbc',
#     hostlist=[('159.89.48.126', 9000)],  # Multiple connections are supported
#     keepalive=True)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(example(siri))