from uagents import Context, Model, Protocol
from protocols.furniquery import FurniArticle  # Importing ClothingArticle class from query.py

class BookFurniRequest(Model):
    article_number : int
    type: str
    color: str
     # Example: user identification
    # Add other necessary fields for the booking request

class BookFurniResponse(Model):
    success: bool

Furni_book_proto = Protocol()

@Furni_book_proto.on_message(model=BookFurniRequest, replies=BookFurniResponse)
async def handle_book_elec_request(ctx: Context, sender: str, msg: BookFurniRequest):
    articles = {
        int(num): FurniArticle(**attributes)
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
    await ctx.send(sender, BookFurniResponse(success=success))
