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
        {"role": "system", "content": "You are a helpful assistant. Evaluate the user's input to determine if they want to end the conversation. If they do, call the 'end_conversation' function."},
        {"role": "user", "content": user_prompt}  # User's input
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=messages,  # Provide the conversation messages
        temperature=0.7,  # Set the randomness of the responses
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "end_conversation",
                    "description": "End the conversation with the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            }
        ],
        tool_choice="auto",  # Let the model decide whether to call the function
    )
    return response

# Function to end the conversation
def end_conversation():
    # print("Function 'end_conversation' called. Ending the chat.")
    # return "Conversation ended."
    return

def chat():
    print("Chatbot is ready! You can end the conversation by expressing your intent to do so.")
    while True:
        user_prompt = input("Enter a message: ")
        assistant_response = get_chat_conversation(user_prompt)
        input_cost = assistant_response.usage.prompt_tokens * MODELS[MODEL_4_TURBO]["input_cost"]
        output_cost = assistant_response.usage.completion_tokens * MODELS[MODEL_4_TURBO]["output_cost"]
        total_cost = input_cost + output_cost

        print(f"You: {user_prompt}")  # Display the user's input
        assistant_message = assistant_response.choices[0].message
        print(f"Assistant: {assistant_message.content}")  # Display the assistant's response
        print(f"Cost: ${total_cost:.8f}")

        # Check if the assistant wants to call the termination function
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "end_conversation":
                    print(f"Tool Call ID: {tool_call.id}")
                    # print(f"Function Name: {tool_call.function.name}")
                    # print(f"Function Arguments: {tool_call.function.arguments}")
                    end_conversation()
                    return  # End the chat

if __name__ == "__main__":
    chat()