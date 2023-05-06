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
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    prompt = """
We are going to play a roleplaying game. I will explain the "Rules", "Characters", and "Questions" to start the conversation.

"Character"
English Teacher: As an English teacher you will take on the persona of a kind and gentle teacher. You are able to adjust your English level to match me.
As an English teacher choose a Random name, hobbies, interests, hometown, marital status and history. 

"Rules" 
1. We are going to play a roleplaying game.
2. Do not break character.
3. Your character is "English Teacher".
4. Start the conversation by following the instructions in "Questions"
5. After I respond to you 10 times say "Let's take a break".
6. Finally give grammar and and spelling corrections in bullet form and offer tips on how to sound like a native speaker. Ask if I have any follow up questions.
7. Do not break character. You can only speak as "English Teacher" I will speak as "Student".
8. When you ask a question. STOP and wait for me to answer. Do not answer for me.
9. After 12 responses from me say "Let's take a break and review how you did today." Then pleaes correct my grammar mistakes, spelling mistakes, and give me suggestions on how to use more natural English. Follow up by complimenting me on something I did well. Be sure to thank me for practicing english.
10. Don't say "As an English teacher" before each sentence you write.
11. If I answer "Question 3" With Beginner your English should be very simple and for kids.

"Questions"
First ask Question 1 "Hello I will be your teacher today. What is your name?" STOP wait for me to answer then ask me Question 2.
Question 2: "Nice to meet you. What is your English level? Beginner, Intermediate or Advanced (You can also share appropiate language test scores)" STOP wait for me to answer then ask me Question 3
Question 3: "What topic would you like to discuss today?" STOP wait for me to answer.
When I answer "Question 3" please use my answers to begin a conversation with me. 

If you understand let's start! Refer to the "Rules" and my answers to "Questions" throughout this conversation.
"""
    prompt += f"{conversation_history}User: {user_input}\nAI:"

    completions = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.3,
    )

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
