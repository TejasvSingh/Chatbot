from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import openai

openai.api_key='sk-vFey-R3pjo-cjOpALdmoP0pa7QhVDaVydpntGUQ2X9T3BlbkFJAeHyrr4PaFCXJoMm8qTuKzlr4M5QmaUDWgqJfZo2EA'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change this if using MongoDB Atlas
db = client['campus_guidance_chatbot']
users_collection = db['users']

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/campus_guidance_chatbot"  # Ensure the database name is correct
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check user credentials
        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'error': 'Invalid email or password.'}), 401

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        if mongo.db.users.find_one({"email": email}):
            return jsonify({'error': 'Email already exists.'}), 409

        # Hash the password for security
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            "email": email,
            "password": hashed_password
        })

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Route to display flash messages
@app.route('/flash_messages')
def flash_messages():
    return render_template('flash_messages.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# New /chat route for handling chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()

    # First, check if the input matches rule-based responses
    response = rule_based_response(user_input)

    if response is None:
        # If no rule-based match, fall back to AI-based response
        response = ai_response(user_input)

    return jsonify({'response': response})

def rule_based_response(user_input):
    # Define a set of common questions and answers
    faq_responses = {
        "campus hours": "Campus hours are from 8 AM to 10 PM, Monday to Friday.",
        "reset password": "Your islander email password can be reset by clicking on Forgot password link and following the steps while trying to sign into your edu account",
        "library hours": "Usually Mon-Thu 7 am - 1:30 am. Check library hours at the frontdesk or website since it may vary on weekends.",
        "wifi issue": "For any WiFi-related issues, please contact the IT department.",
        "michael and karen o'connor building to bay hall": "Begin by heading southeast for a distance of 52 feet. Then, make a left turn and proceed for 351 feet. Next, take a slight right and continue for 102 feet. Finally, turn left, and your destination will be located on the left after traveling an additional 43 feet.",
        "michael and karen o'connor to bay hall": "Begin by heading southeast for a distance of 52 feet. Then, make a left turn and proceed for 351 feet. Next, take a slight right and continue for 102 feet. Finally, turn left, and your destination will be located on the left after traveling an additional 43 feet.",
        "ocnr to bay hall": "Begin by heading southeast for a distance of 52 feet. Then, make a left turn and proceed for 351 feet. Next, take a slight right and continue for 102 feet. Finally, turn left, and your destination will be located on the left after traveling an additional 43 feet.",
        "ocnr building to bay hall": "Begin by heading southeast for a distance of 52 feet. Then, make a left turn and proceed for 351 feet. Next, take a slight right and continue for 102 feet. Finally, turn left, and your destination will be located on the left after traveling an additional 43 feet.",
        "dining hall to engineering": "Begin by heading northwest on Curfew Drive/Curlew Drive for 433 feet. Then, make a right turn and proceed for 164 feet. Next, turn left and continue for 335 feet. Afterward, turn right and travel 249 feet before making another left turn. Continue for 171 feet, then make a final right turn. Your destination will be located on the left after an additional 141 feet.",
        "human assistant": "Since you think I cannot help you please get in touch with the human assistant here : <a href='https://support.tamucc.edu/' target='_blank'>Support TAMUCC</a>."
    }

    # Check if any of the pre-defined questions match the user's input
    for question, response in faq_responses.items():
        if question in user_input.lower():
            return response
    return None

def ai_response(user_input):
    try:
        # Send the input to OpenAI for a response
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:guidance-system:ASWWwtyb", # fine-tuned model - ft:gpt-4o-mini-2024-07-18:personal:guidance-system:ASWWwtyb # normal model - gpt-3.5-turbo-instruct
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in guiding students around the Texas A&M University-Corpus Christi campus."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
            #prompt=user_input,
            #max_tokens=150,
            #n=1,
            #stop=None,
            #temperature=0.7
        )
        # Extract the response from the API result
        # return response.choices[0].text.strip() # for normal model
        return response['choices'][0]['message']['content'].strip() # For fine-tuned model
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")  # Log the error message
        return "Sorry, there was an issue connecting to the AI service. Please try again later."
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")  # Catch and log any other unexpected errors
        return "Sorry, I am unable to process your request right now."


# The above rules are basic, we can make them more precise. But we want to create a hybrid chatbot.
# Consider using OpenAI, integrate it using the KEY and train the model to answer personalized questions.


if __name__ == '__main__':
    app.run(debug=True)
