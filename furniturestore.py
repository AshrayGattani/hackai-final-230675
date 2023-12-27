from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.furnibook import Furni_book_proto
from protocols.furniquery import Furni_query_proto
from protocols.furniquery import FurniArticle  # Assuming ClothingArticle model is defined

Furni_store = Agent(
    name="Furni_store",
    port=8002,  # Choose a suitable port for the elec store
    seed="Furni_store secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(Furni_store.wallet.address())

Furni_store.include(Furni_query_proto)
Furni_store.include(Furni_book_proto)

# Clothing articles available in the store
FURNI_ARTICLES = {
    1: FurniArticle(type="Chair",color="Black",available=True),
    2: FurniArticle(type="Table",color="Silver",available=True),
    3: FurniArticle(type="Cupboard",color="Brown",available=True),
    4: FurniArticle(type="Stool",color="Red",available=True)
    # Add more clothing articles as needed
}



# Set the clothing articles information in the store's protocols
for (number, article) in FURNI_ARTICLES.items():
    Furni_store._storage.set(number, article.dict())

if __name__ == "__main__":
    print(Furni_store.address)
    Furni_store.run()
