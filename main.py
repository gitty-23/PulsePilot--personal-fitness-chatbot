# Import necessary libraries
import os
from openai import OpenAI
import gradio
from youtube_search import YoutubeSearch
from gradio import components

# Set OpenAI API key
api_key = "insert API key here"
client = OpenAI(api_key=api_key)

# Define start and restart sequences for conversation history
start_sequence = "\nTrainer:"
restart_sequence = "\nClient: "

# Define initial prompt for the conversation
prompt = "The following is a conversation with a gym trainer. The trainer is knowledgeable, helpful, and dedicated to helping you reach your fitness goals.\n\nClient: Hi, I need some guidance on my workout routine.\nTrainer: "

# Function to generate response using OpenAI API
def openai_create(message):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Function to handle conversation history
def chatgpt_clone(input, history, client_info):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    inp += "\nClient Info: " + client_info
    output = openai_create(inp)
    history.append((input, output))
    return history, history


# Function to handle the chat interface
def chat_interface(message, client_info):
    if message.strip() == "":
        # Return empty outputs if both queries are empty
        return ""

    chatbot_output = ""

    if message.strip() != "":
        # Generate chatbot response using OpenAI
        response = openai_create(message)
        chatbot_output = response.split("Trainer:")[-1].strip()

    return chatbot_output

# Define example prompts, client info examples, and video query examples
example_prompts = [
    "What are some good exercises for weight loss?",
    "How many calories should I consume in a day?",
    "Can you recommend a workout routine for beginners?"
]
client_info_examples = [
    "I am 5 feet 9 inches, 20 years old, and weigh 95 kg",
    "I have a shoulder injury",
    "I am a male and a beginner"
]

# Create the Gradio interface
iface = gradio.Interface(
    fn=chat_interface,
    inputs=[
        components.Textbox(label="Talk With Fit", lines=5, placeholder="Enter your message"),
        components.Textbox(label="Client Info", placeholder="Enter your height, age, weight, etc For better Personalized results"),
        
    ],
    outputs=[
        components.Textbox(label="Chatbot Response", lines=5),
    
    ],
    title="PulsePIlot - Your Personal Gym Trainer",
    theme="default",
    examples=[
        [example_prompt, client_info_example]
        for example_prompt, client_info_example in zip(
            example_prompts, client_info_examples
        )
    ]
)

# Launch the interface
iface.launch(inline=False, share=True)
