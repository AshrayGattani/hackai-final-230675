from uagents import Context, Model, Protocol
from protocols.elecquery import ElecArticle  # Importing ClothingArticle class from query.py

class BookElecRequest(Model):
    article_number : int
    type: str
    brand: str
    color: str
     # Example: user identification
    # Add other necessary fields for the booking request

class BookElecResponse(Model):
    success: bool

elec_book_proto = Protocol()

@elec_book_proto.on_message(model=BookElecRequest, replies=BookElecResponse)
async def handle_book_elec_request(ctx: Context, sender: str, msg: BookElecRequest):
    articles = {
        int(num): ElecArticle(**attributes)
        for num, attributes in ctx.storage._data.items()
        if isinstance(num, int)
    }
    article = articles.get(msg.article_number)
    
    # Perform reservation logic based on the available articles
    if article and article.available:  # Assuming there's an 'available' attribute in ClothingArticle
      # Example method to reserve the article for a user
        ctx.storage.set(msg.article_number, article.dict())
        success = True
    else:
        success = False
    
    # Send the response
    await ctx.send(sender, BookElecResponse(success=success))
