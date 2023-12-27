from uagents import Context, Model, Protocol

# Define a model for clothing availability query
class CheckClothingAvailabilityRequest(Model):
    clothing_item: str
    size: str

class CheckClothingAvailabilityResponse(Model):
    available: bool

# Assume there's a storage dictionary with clothing availability information
clothing_inventory = {
    "tshirt": {"S": True, "M": False, "L": True},
    "pants": {"S": False, "M": True, "L": True},
    # Add more clothing items and their availability by size here
}

clothing_proto = Protocol()

@clothing_proto.on_query(model=CheckClothingAvailabilityRequest, replies=CheckClothingAvailabilityResponse)
async def handle_clothing_availability_query(ctx: Context, sender: str, msg: CheckClothingAvailabilityRequest):
    clothing_item = msg.clothing_item.lower()
    size = msg.size.upper()

    if clothing_item in clothing_inventory and size in clothing_inventory[clothing_item]:
        available = clothing_inventory[clothing_item][size]
        response = CheckClothingAvailabilityResponse(available=available)
        ctx.logger.info(f"Query: {msg}. Available: {available}.")
        await ctx.send(sender, response)
    else:
        ctx.logger.error(f"Clothing item '{clothing_item}' or size '{size}' not found.")
        # Respond with unavailable if item or size not found
        await ctx.send(sender, CheckClothingAvailabilityResponse(available=False))
