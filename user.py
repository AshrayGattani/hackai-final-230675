from protocols.query import QueryClothingRequest, QueryClothingResponse
from protocols.book import BookClothingRequest, BookClothingResponse
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

CLOTHING_STORE_ADDRESS = "agent1qt5j5dgcl4gnrxqnt3jgm3klh0n623mxv9vuvfxx3haugxgwk5anczd45kw"

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(user.wallet.address())

clothing_query = QueryClothingRequest(
    color="blue",
    size="M",
    style="casual",
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
        ctx.storage.set("completed", True)

@user.on_message(BookClothingResponse, replies=set())
async def handle_book_response(ctx: Context, _sender: str, msg: BookClothingResponse):
    if msg.success:
        ctx.logger.info("Clothing article reservation was successful.")
    else:
        ctx.logger.info("Clothing article reservation was UNSUCCESSFUL.")
    ctx.storage.set("completed", True)

if __name__ == "__main__":
    user.run()

