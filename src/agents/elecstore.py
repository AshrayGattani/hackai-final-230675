from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.elecbook import elec_book_proto
from protocols.elecquery import elec_query_proto
from protocols.elecquery import ElecArticle  # Assuming ClothingArticle model is defined

elec_store = Agent(
    name="elec_store",
    port=8000,  # Choose a suitable port for the elec store
    seed="elec_store secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(elec_store.wallet.address())

elec_store.include(elec_query_proto)
elec_store.include(elec_book_proto)

# Clothing articles available in the store
ELEC_ARTICLES = {
    1: ElecArticle(type="Headphones",brand="Sony",color="Black",available=True),
    2: ElecArticle(type="Fridge",brand="LG",color="Silver",available=True),
    3: ElecArticle(type="TV",brand="Mi",color="Blue",available=True),
    4: ElecArticle(type="Phone",brand="Apple",color="Red",available=True)
    # Add more clothing articles as needed
}



# Set the clothing articles information in the store's protocols
for (number, article) in ELEC_ARTICLES.items():
    elec_store._storage.set(number, article.dict())

if __name__ == "__main__":
    # print(elec_store.address)
    elec_store.run()
