from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.book import cloth_book_proto
from protocols.query import cloth_query_proto
from protocols.query import ClothingArticle  # Assuming ClothingArticle model is defined

clothing_store = Agent(
    name="clothing_store",
    port=8002,  # Choose a suitable port for the clothing store
    seed="clothing_store secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(clothing_store.wallet.address())

clothing_store.include(cloth_query_proto)
clothing_store.include(cloth_book_proto)

# Clothing articles available in the store
CLOTHING_ARTICLES = {
    1: ClothingArticle(color="blue", size="M", style="casual"),
    2: ClothingArticle(color="red", size="S", style="formal"),
    3: ClothingArticle(color="green", size="L", style="sportswear"),
    # Add more clothing articles as needed
}

# Set the clothing articles information in the store's protocols
for (number, article) in CLOTHING_ARTICLES.items():
    clothing_store._storage.set(number, article.dict())

if __name__ == "__main__":
    clothing_store.run()
