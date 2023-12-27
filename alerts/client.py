from uagents import Agent,Context,Protocol
from essentials import *
from utils import alert
from fetcher import *
# from messages import Notification


# User Input
orgprice = input("Enter The original Price of Product: ")
newprice = input("Enter new Price for given product: ")

# base_currency = input("Enter The Base Currency: ") # Format e.g. USD
# target_currencies = input("Enter The Currencies To Be Converted: ") # Format e.g. INR EUR
# max_threshold = input("Enter Maximum Limit For The Given Currencies: ") # Format e.g. 45 50 70
# min_threshold = input("Enter Minimum Limit For The Given Currencies: ") # Format e.g. 1 9 11



client = Agent(name="Client Agent")

@client.on_interval(period=45.0, messages= FetchRequest)
async def fetch_rates(ctx: Context):

    await ctx.send(fetcher.address, FetchRequest(org_price=orgprice,new_price=newprice)
)

@client.on_message(FetchResponse)
async def print_rates(ctx: Context,_sender: str, msg: FetchResponse):

    '''

        This is Responsible for displaying and printing the result obtained using the values from Client Agent and 
        the results fetched from the Fetcher Agent.

    '''
    if msg.success:
        print("ALERT ALERT !!!!")
            
    else:
        pass


# # Create a protocol for notifications
# notify_protocol = Protocol("Notify")


# # Function to handle incoming notifications requests
# @notify_protocol.on_message(model=Notification)
# async def send_notification(ctx: Context, sender: str, msg: Notification):
#     # context = generate_context(msg)
#     success, data = await send_email(msg.name, msg.email, ctx)
#     if success:
#         ctx.logger.info("Email sent successfully")
#     else:
#         ctx.logger.error(f"Error sending email: {data}")

# client.include(notify_protocol)