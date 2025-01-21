"if __name__ == '__main__'"


import os  # For environment variable management
import openai  # OpenAI library for interacting with the API
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client with an API key and base URL
# The API key is fetched from an environment variable
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://litellm.aks-hs-prod.int.hyperskill.org",  # Custom base URL for the API
)

# Function to generate a chat conversation with the assistant
def get_chat_conversation(system_message, user_prompt):
    # Define the conversation messages: system message and user prompt
    messages = [
        {"role": "system", "content": system_message},  # System's instructions to the assistant
        {"role": "user", "content": user_prompt}  # User's input
    ]
    # Send the request to the OpenAI API and get the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=messages,  # Provide the conversation messages
        temperature=0.7  # Set the randomness of the responses
    )
    # Extract and return the assistant's response
    return response.choices[0].message.content

# Define the system's initial instructions for the assistant
system_message1 = "You are a helpful assistant for a simple CLI chat. Only respond with text messages. Get creative with the answers!"

# Define the user's input or question
user_prompt1 = "What are you?"

# Get the assistant's response based on the system message and user prompt
assistant_response = get_chat_conversation(system_message1, user_prompt1)

# Print the conversation to the console
print(f"You: {user_prompt1}")  # Display the user's input
print(f"Assistant: {assistant_response}")  # Display the assistant's response
