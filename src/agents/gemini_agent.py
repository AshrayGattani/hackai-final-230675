# Import all necessary modules and resources from various libraries
from uagents import Agent, Context, Protocol
from messages.basic import Data, Request, Error
from uagents.setup import fund_agent_if_low
import os
import requests
import json

# Get the HUGGING_FACE_ACCESS_TOKEN from environment variable or default to a placeholder string if not found.
# HUGGING_FACE_ACCESS_TOKEN = os.getenv(
#     "HUGGING_FACE_ACCESS_TOKEN", "HUGGING FACE secret phrase :)")

# HUGGING_FACE_ACCESS_TOKEN = "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"

# Define configurations used for HTTP requests to Hugging Face
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyAM-r5O4jcnGuecd42RV3keS9BHTaY-aA4"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')
# Create an agent with predefined properties
agent = Agent(
    name="gemini_agent",
    seed="HUGGING_FACE_ACCESS_TOKEN",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Ensure the agent has enough funds
fund_agent_if_low(agent.wallet.address())

# Define an asynchronous function to get the auto-completion from the GPT-2 model


async def get_completion(ctx: Context, sender: str, completion_text: str):
    # Prepare the data for HTTP request
    # data = {
    #     "inputs": completion_text
    # }

    # Make the HTTP request and handle possible errors
    try:
        # response = requests.post(
        #     SENTIMENT_URL, headers=HEADERS, json=data)
        response = model.generate_content(f"{completion_text}")
        # if response.status_code != 200:
        #     await ctx.send(sender, Error(error=f"Error: {response.json().get('error')}"))
        #     return
        message = response.text
    except Exception as ex:
        await ctx.send(sender, Error(error=f"Sorry, I wasn't able to answer your request this time. Feel free to try again. Error detail: {ex}"))
        return

    # Send the response back to the sender
    await ctx.send(sender, Data(generated_text=message))
    return message

# Create an instance of Protocol with a label "Request"
gemini_agent = Protocol("Request")


@gemini_agent.on_message(model=Request, replies={Data, Error})
async def handle_request(ctx: Context, sender: str, request: Request):
    # Log the request details
    ctx.logger.info(
        f"Got request from  {sender} to answer: {request.text}")

    # Get the response from GPT-2 model
    await get_completion(ctx, sender, request.text)


# Include the protocol with the agent
agent.include(gemini_agent)

# Define the main entry point of the application
if __name__ == "__main__":
    gemini_agent.run()
    