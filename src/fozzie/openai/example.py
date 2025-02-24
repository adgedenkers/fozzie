from fozzie.openai import set_openai_api_key, send_message

# Set your OpenAI API key (You can also set this as an environment variable)
set_openai_api_key("your-api-key-here")

# Define the conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the address of the Empire State Building?"}
]

# Send the message
response = send_message(messages)

# Print the response
print("ChatGPT Response:", response)
