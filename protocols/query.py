from typing import List
from uagents import Context, Model, Protocol

class ClothingArticle(Model):
    color: str
    size: str
    style: str

class QueryClothingRequest(Model):
    color: str
    size: str
    style: str

class QueryClothingResponse(Model):
    articles: List[int]

class GetTotalClothingQueries(Model):
    pass

class TotalClothingQueries(Model):
    total_queries: int

cloth_query_proto = Protocol()

@cloth_query_proto.on_message(model=QueryClothingRequest, replies=QueryClothingResponse)
async def handle_query_clothing_request(ctx: Context, sender: str, msg: QueryClothingRequest):
    articles = {
        int(num): ClothingArticle(**attributes)
        for num, attributes in ctx.storage._data.items()
        if isinstance(num, int)
    }
    available_articles = []
    for number, article in articles.items():
        if (
            article.color == msg.color
            and article.size == msg.size
            and article.style == msg.style
        ):
            available_articles.append(int(number))
    ctx.logger.info(f"Query: {msg}. Available articles: {available_articles}.")
    await ctx.send(sender, QueryClothingResponse(articles=available_articles))
    total_clothing_queries = int(ctx.storage.get("total_clothing_queries") or 0)
    ctx.storage.set("total_clothing_queries", total_clothing_queries + 1)

@cloth_query_proto.on_query(model=GetTotalClothingQueries, replies=TotalClothingQueries)
async def handle_get_total_clothing_queries(ctx: Context, sender: str, _msg: GetTotalClothingQueries):
    total_clothing_queries = int(ctx.storage.get("total_clothing_queries") or 0)
    await ctx.send(sender, TotalClothingQueries(total_queries=total_clothing_queries))
