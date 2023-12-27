from typing import List
from uagents import Context, Model, Protocol

class FurniArticle(Model):
    type: str
    color: str
    available : bool

class QueryFurniRequest(Model):
    type: str
    color: str

class QueryFurniResponse(Model):
    articles: List[int]

class GetTotalFurniQueries(Model):
    pass

class TotalFurniQueries(Model):
    total_queries: int

Furni_query_proto = Protocol()

@Furni_query_proto.on_message(model=QueryFurniRequest, replies=QueryFurniResponse)
async def handle_query_Furniture_request(ctx: Context, sender: str, msg: QueryFurniRequest):
    articles = {
        int(num): FurniArticle(**attributes)
        for num, attributes in ctx.storage._data.items()
        if isinstance(num, int)
    }
    available_articles = []
    for number, article in articles.items():
        if (
            article.type == msg.type
            and article.color == msg.color
        ):
            available_articles.append(int(number))
    ctx.logger.info(f"Query: {msg}. Available articles: {available_articles}.")
    await ctx.send(sender, QueryFurniResponse(articles=available_articles))
    total_Furniture_queries = int(ctx.storage.get("total_Furniture_queries") or 0)
    ctx.storage.set("total_Furniture_queries", total_Furniture_queries + 1)

@Furni_query_proto.on_query(model=GetTotalFurniQueries, replies=TotalFurniQueries)
async def handle_get_total_clothing_queries(ctx: Context, sender: str, _msg: GetTotalFurniQueries):
    total_Furniture_queries = int(ctx.storage.get("total_Furniture_queries") or 0)
    await ctx.send(sender, TotalFurniQueries(total_queries=total_Furniture_queries))
