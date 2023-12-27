from uagents import Agent,Context
from utils import alert
from essentials import *


fetcher = Agent(name="Fetcher Agent")

@fetcher.on_message(FetchRequest,replies={FetchResponse})
async def fetch_rates(ctx: Context,sender: str,msg: FetchRequest):
    '''

    Defining the working and operation of the Fetcher Agent.

    '''
    try:
        rates = alert(msg.new_price,msg.org_price)
        await ctx.send(sender, FetchResponse(success=True))
    except:
        ctx.send(sender,FetchResponse(success=False))
    
