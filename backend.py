
# import os
# from dotenv import load_dotenv
# from groq import Groq

# # Load environment variables
# load_dotenv()

# # Initialize Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # Conversation memory
# messages = [
#     {"role": "system", "content": "You are a helpful AI assistant."}
# ]

# print("🤖 Groq Chatbot (type 'exit' to quit)\n")

# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("Goodbye 👋")
#         break

#     messages.append({"role": "user", "content": user_input})

#     try:
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=messages,
#             temperature=0.7,
#             max_tokens=1024,
#         )

#         reply = response.choices[0].message.content
#         print("Bot:", reply, "\n")

#         messages.append({"role": "assistant", "content": reply})

#     except Exception as e:
#         print("Error:", e)


import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def get_response(messages, temperature: float = 0.7, max_tokens: int = 1024, chunk_size: int = None, chunk_overlap: int = None):
    """Create a chat completion using the Groq client.

    Parameters are exposed so the UI can control temperature and max_tokens.
    `chunk_size` and `chunk_overlap` are accepted for future use (document chunking).
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content