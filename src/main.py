from uagents import Bureau, Agent


from agents.furniturestore import Furni_store as furnitureagent
from agents.clothingstore import clothing_store as clothesagent
from agents.elecstore import elec_store as elecagent
from agents.sentiment_agent import agent as sentimentagent
from agents.sentiment_user import user as sentimentuser
from agents.context_agent import agent as contextagent
from agents.context_user import user as contextuser
from agents.imagegen_agent import agent as imagegenagent
from agents.imagegen_user import user as imagegenuser
from agents.gemini_agent import agent as geminiagent
from agents.gemini_user import user as geminiuser
from agents.user import user
# print("Debug")



if __name__ == "__main__":
    # opt = input("enter : ")
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    # print(f"Adding agent to Bureau: {agent.address}")
    
    bureau.add(furnitureagent)
    bureau.add(clothesagent)
    bureau.add(elecagent)
    bureau.add(contextagent)
    bureau.add(imagegenagent)
    bureau.add(geminiagent)
    bureau.add(sentimentuser)
    bureau.add(sentimentagent)
    bureau.add(contextuser)
    bureau.add(imagegenuser)
    bureau.add(geminiuser)
    bureau.add(user)

    bureau.run()
    
    # print(f"Adding user agent to Bureau: {user.address}")
        
    
    
