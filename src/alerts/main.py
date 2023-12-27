from fetcher import *
from client import *
from uagents import Bureau


if __name__ == "__main__":
    b = Bureau()
    b.add(fetcher)
    b.add(client)
    b.run()
