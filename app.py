# Import required libraries
from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Set the model ID
model_id = "text-davinci-003"

# Function to generate a response from the model
def generate_response(conversation_history, user_input):
    # Authenticate with OpenAI using the environment variable
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    prompt = "You are an English teacher and Conversation Partner. "
    prompt += conversation_history + user_input

    # Create a completion using the provided prompt
    completions = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Extract the text from the first choice in the completions
    message = completions.choices[0].text
    return message.strip()

conversation_history = ""

# Define the route for the home page
@app.route("/")
def home():
    # Render the home page template
    return render_template("index.html")

# Define the route for submitting a message
@app.route("/submit", methods=["POST"])
def submit_message():
    global conversation_history
    # Get the message from the request JSON
    user_input = request.json["message"]
    conversation_history += f"User: {user_input}\n"
    # Generate a response using the modified prompt
    bot_response = generate_response(conversation_history, user_input)
    conversation_history += f"AI: {bot_response}\n"
    # Return the bot response as JSON
    return jsonify(response=bot_response)

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
