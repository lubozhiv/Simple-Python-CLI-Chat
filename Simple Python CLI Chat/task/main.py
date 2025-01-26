


import os  # For environment variable management
import openai  # OpenAI library for interacting with the API
from dotenv import load_dotenv  # To load environment variables from a .env file
load_dotenv()

MODEL_35_TURBO = "gpt-3.5-turbo"
MODEL_4_TURBO = "gpt-4-turbo-preview"

MODELS = {
    MODEL_35_TURBO: {"input_cost": 0.0005 / 1000, "output_cost": 0.0015 / 1000},
    MODEL_4_TURBO: {"input_cost": 0.01 / 1000, "output_cost": 0.03 / 1000},
}

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://litellm.aks-hs-prod.int.hyperskill.org",  # Custom base URL for the API
)

# Function to generate a chat conversation with the assistant
def get_chat_conversation(user_prompt):
    messages = [

        {"role": "user", "content": user_prompt}  # User's input
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=messages,  # Provide the conversation messages
        temperature=0.7  # Set the randomness of the responses
    )
    return response



def chat():
    print("Chatbot is ready! Type 'exit' to end the conversation.")
    while True:
        user_prompt = input("Enter a message:")
        if user_prompt.lower() == "exit":
            print("Goodbye! Ending the chat.")
            break

        assistant_response = get_chat_conversation(user_prompt)
        input_cost = assistant_response.usage.prompt_tokens * MODELS[MODEL_4_TURBO]["input_cost"]

        output_cost = assistant_response.usage.prompt_tokens * MODELS[MODEL_4_TURBO]["output_cost"]

        total_cost = input_cost + output_cost

        print(f"You: {user_prompt}")  # Display the user's input
        print(f"Assistant: {assistant_response.choices[0].message.content}")  # Display the assistant's response
        print(f"Cost: ${total_cost:.8f}")

# if __name__ == "__main__":
chat()