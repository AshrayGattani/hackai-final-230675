from typing import List
from uagents import Context, Model, Protocol

class ElecArticle(Model):
    type: str
    brand: str
    color: str
    available : bool

class QueryElecRequest(Model):
    type: str
    brand: str
    color: str

class QueryElecResponse(Model):
    articles: List[int]

class GetTotalElecQueries(Model):
    pass

class TotalElecQueries(Model):
    total_queries: int

elec_query_proto = Protocol()

@elec_query_proto.on_message(model=QueryElecRequest, replies=QueryElecResponse)
async def handle_query_clothing_request(ctx: Context, sender: str, msg: QueryElecRequest):
    articles = {
        int(num): ElecArticle(**attributes)
        for num, attributes in ctx.storage._data.items()
        if isinstance(num, int)
    }
    available_articles = []
    for number, article in articles.items():
        if (
            article.type == msg.type
            and article.brand == msg.brand
            and article.color == msg.color
        ):
            available_articles.append(int(number))
    ctx.logger.info(f"Query: {msg}. Available articles: {available_articles}.")
    await ctx.send(sender, QueryElecResponse(articles=available_articles))
    total_clothing_queries = int(ctx.storage.get("total_clothing_queries") or 0)
    ctx.storage.set("total_clothing_queries", total_clothing_queries + 1)

@elec_query_proto.on_query(model=GetTotalElecQueries, replies=TotalElecQueries)
async def handle_get_total_clothing_queries(ctx: Context, sender: str, _msg: GetTotalElecQueries):
    total_clothing_queries = int(ctx.storage.get("total_clothing_queries") or 0)
    await ctx.send(sender, TotalElecQueries(total_queries=total_clothing_queries))
