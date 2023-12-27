from uagents import Agent,Context, Model, Protocol

class Product(Model):
    product_id: int
    price: float

class BuyProductRequest(Model):
    product_id: int

class BuyProductResponse(Model):
    success: bool
    remaining_money: float

user_money = 100.0  # Initial amount of money for the user

product_list = {
    1: Product(product_id=1, price=20.0),
    2: Product(product_id=2, price=30.0),
}

buy_agent = Agent(name="BUY")

@buy_agent.on_message(model=BuyProductRequest, replies=BuyProductResponse)
async def handle_buy_product_request(ctx: Context, sender: str, msg: BuyProductRequest):
    product = product_list.get(msg.product_id)
    
    if product:
        if user_money >= product.price:
            # Sufficient funds to buy the product
            user_money -= product.price
            ctx.logger.info(f"User bought product {msg.product_id} for ${product.price}. Remaining money: ${user_money}.")
            await ctx.send(sender, BuyProductResponse(success=True, remaining_money=user_money))
        else:
            # Insufficient funds
            ctx.logger.info(f"User does not have enough money to buy product {msg.product_id}.")
            await ctx.send(sender, BuyProductResponse(success=False, remaining_money=user_money))
    else:
        # Product not found
        ctx.logger.info(f"Product with ID {msg.product_id} not found.")
        await ctx.send(sender, BuyProductResponse(success=False, remaining_money=user_money))


if __name__ == "__main__":
 
    buy_agent.run()
