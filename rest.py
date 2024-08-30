from pyopensky.rest import REST
from pyopensky.trino import Trino
from datetime import datetime, timedelta


rest = REST()
trino = Trino()

start = (datetime.now() - timedelta(days=2)).timestamp()
flights = trino.flightlist(start)
print(flights)

