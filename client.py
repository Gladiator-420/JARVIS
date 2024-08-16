import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("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"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "You are a virtual assistent named jarvis ehich works like alexa and google",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)