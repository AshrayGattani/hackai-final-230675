from uagents import Context, Model, Protocol
from query import ClothingArticle  # Importing ClothingArticle class from query.py

class BookClothingRequest(Model):
    article_number: int
    user_id: str  # Example: user identification
    # Add other necessary fields for the booking request

class BookClothingResponse(Model):
    success: bool

cloth_book_proto = Protocol()

@cloth_book_proto.on_message(model=BookClothingRequest, replies=BookClothingResponse)
async def handle_book_clothing_request(ctx: Context, sender: str, msg: BookClothingRequest):
    articles = {
        int(num): ClothingArticle(**attributes)
        for num, attributes in ctx.storage._data.items()
        if isinstance(num, int)
    }
    article = articles.get(msg.article_number)
    
    # Perform reservation logic based on the available articles
    if article and article.available:  # Assuming there's an 'available' attribute in ClothingArticle
        article.reserve_for_user(msg.user_id)  # Example method to reserve the article for a user
        ctx.storage.set(msg.article_number, article.dict())
        success = True
    else:
        success = False
    
    # Send the response
    await ctx.send(sender, BookClothingResponse(success=success))
