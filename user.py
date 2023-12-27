from protocols.query import QueryClothingRequest, QueryClothingResponse
from protocols.book import BookClothingRequest, BookClothingResponse
from protocols.elecquery import QueryElecRequest, QueryElecResponse
from protocols.elecbook import BookElecRequest, BookElecResponse
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

CLOTHING_STORE_ADDRESS = "agent1qt5j5dgcl4gnrxqnt3jgm3klh0n623mxv9vuvfxx3haugxgwk5anczd45kw"
ELEC_STORE_ADDRESS = "agent1qvmw8mkdg8j27rmf6reknsej2mymfmqr0ha6qs87qwtzlypvj45ku8fzfnj"
user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)


fund_agent_if_low(user.wallet.address())

category = input("Enter category : ")
if(category=="Clothes"):
    colorin = input("Enter color : ")
    sizein = input("Enter size : ")
    stylein = input("Enter style : ")

    clothing_query = QueryClothingRequest(
        color=colorin,
        size=sizein,
        style=stylein,
    )

    @user.on_interval(period=3.0, messages=QueryClothingRequest)
    async def interval(ctx: Context):
        completed = ctx.storage.get("completed")
        if not completed:
            await ctx.send(CLOTHING_STORE_ADDRESS, clothing_query)

    @user.on_message(QueryClothingResponse, replies={BookClothingRequest})
    async def handle_query_response(ctx: Context, sender: str, msg: QueryClothingResponse):
        if len(msg.articles) > 0:
            ctx.logger.info("There are available clothing articles. Proceeding to book.")
            article_number = msg.articles[0]

            request = BookClothingRequest(
                article_number=article_number,
                color=clothing_query.color,
                size=clothing_query.size,
                style=clothing_query.style,
            )

            await ctx.send(sender, request)
        else:
            ctx.logger.info("No available clothing articles found.")
            # ctx.storage.set("completed", True)

    @user.on_message(BookClothingResponse, replies=set())
    async def handle_book_response(ctx: Context, _sender: str, msg: BookClothingResponse):
        if msg.success:
            ctx.logger.info("Clothing article reservation was successful.")
        else:
            ctx.logger.info("Clothing article reservation was UNSUCCESSFUL.")
        # ctx.storage.set("completed", True)

if category=="Electronics":
    typein = input("Enter type : ")
    brandin = input("Enter brand : ")
    colorin = input("Enter color : ")

    elec_query = QueryElecRequest(
        type=typein,
        brand=brandin,
        color=colorin,
    )

    @user.on_interval(period=3.0, messages=QueryElecRequest)
    async def interval(ctx: Context):
        completed = ctx.storage.get("completed")
        if not completed:
            await ctx.send(ELEC_STORE_ADDRESS, elec_query)

    @user.on_message(QueryElecResponse, replies={BookElecRequest})
    async def handle_query_response(ctx: Context, sender: str, msg: QueryElecResponse):
        if len(msg.articles) > 0:
            ctx.logger.info("There are available electronics articles. Proceeding to book.")
            article_number = msg.articles[0]

            request = BookElecRequest(
                article_number=article_number,
                type=elec_query.type,
                brand=elec_query.brand,
                color=elec_query.color,
            )

            await ctx.send(sender, request)
        else:
            ctx.logger.info("No available electronics articles found.")
            # ctx.storage.set("completed", True)

    @user.on_message(BookElecResponse, replies=set())
    async def handle_book_response(ctx: Context, _sender: str, msg: BookElecResponse):
        if msg.success:
            ctx.logger.info("Article reservation was successful.")
        else:
            ctx.logger.info("Article reservation was UNSUCCESSFUL.")
        # ctx.storage.set("completed", True)


if __name__ == "__main__":
 
    user.run()

