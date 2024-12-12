import pandas as pd
import uuid
from huggingface_hub import InferenceClient
from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
from rag_query import rag_query  # Import your RAG query logic

# Hugging Face Client Setup
HF_TOKEN = "hhf_wLKmaqGneiqxqiVtdPMNhWywjnOThTzAEa"
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key

# Dummy user credentials
USERS = {
    'user1': 'password1',
    'user2': 'password2',
    'sujal': 'hero',
    'kmit': 'kmit123',
    'hansika': 'vardhini',
    'shruthika':'shamarthi',
    }

def generate_initial_message():
    """Generate an initial welcome message for the chatbot"""
    return (
        "Welcome to Mental Health Support. I'm here to listen and provide compassionate support. "
        "Feel free to share your thoughts or concerns, and I'll do my best to help you."
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            # Initialize chat with a welcome message
            session['chat_history'] = [
                {'role': 'bot', 'content': generate_initial_message()}
            ]
            session['not_satisfied'] = False  # Initialize satisfaction state
            return redirect(url_for('chatbot'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    session.setdefault('chat_history', [
        {'role': 'bot', 'content': generate_initial_message()}
    ])
    session.setdefault('not_satisfied', False)
    # Handle "Clear Chat History" button
    if request.method == 'POST' and 'clear_history' in request.form:
        session['chat_history'] = [
            {'role': 'bot', 'content': generate_initial_message()}
        ]  # Reset to the initial bot message
        session['not_satisfied'] = False  # Reset satisfaction flag
        session.modified = True
        return render_template('chatbot.html', chat_history=session.get('chat_history', []))

    # Handle "Not Satisfied" button
    if request.method == 'POST' and 'not_satisfied' in request.form:
        if len(session['chat_history']) >= 1:
            # Extract the last user message
            last_user_message = session['chat_history'][-1]['content']
            
            # Regenerate response
            new_response = rag_query(last_user_message)
            
            if new_response:
                # Replace the last bot message with the new response
                session['chat_history'][-1] = {'role': 'bot', 'content': new_response}
            else:
                # Add a fallback if no new response
                session['chat_history'][-1] = {
                    'role': 'bot', 
                    'content': "Sorry, I couldn't provide a response."
                }
            
            session.modified = True
        
        return render_template('chatbot.html', chat_history=session.get('chat_history', []))
    
    # Existing user query handling remains the same
    if request.method == 'POST' and 'user_message' in request.form:
        user_message = request.form['user_message']
        session['chat_history'].append({'role': 'user', 'content': user_message})
        
        try:
            bot_response = rag_query(user_message)
        except Exception as e:
            print(f"[ERROR] Error querying LLM: {e}")
            bot_response = "I'm here to support you. Could you rephrase your question?"
        
        if not bot_response or bot_response.strip() == "":
            bot_response = (
                "I'm here to listen. Could you tell me more about what you're experiencing?"
            )
        
        session['chat_history'].append({'role': 'bot', 'content': bot_response})
        session.modified = True
    
    return render_template('chatbot.html', chat_history=session.get('chat_history', []))













@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
