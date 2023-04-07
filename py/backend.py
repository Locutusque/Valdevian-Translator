from flask import Flask, render_template, request, abort, session, redirect, url_for, make_response
from flask_talisman import Talisman
from ValdevianTranslator import ValdevianTranslator
import os
import sqlite3
from queue import Queue
from datetime import datetime, timedelta
translation_queue = Queue()

# Create a connection to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
conn.commit()

# Close the database connection
conn.close()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
app = Flask(__name__, template_folder=f'{parent_dir}\\html', static_folder=f'{parent_dir}\\static')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Set a secret key for the session to enhance security
app.secret_key = os.urandom(16)

blacklisted_ips = ['152.89.196.54']

@app.before_request
def before_request():
    # Get the client IP address from the request headers
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Block requests from blacklisted IPs
    if client_ip in blacklisted_ips:
        return abort(403, "Your IP is not authorized to access this resource.")
    
    # Check if the user is logged in and redirect to login page if they are not
    if request.endpoint not in ['login', 'signup'] and 'username' not in session:
        return redirect(url_for('login'))

    # Block requests to non-existent directories
    path = request.path

    # Check if the request method is GET or POST
    if request.method in ['GET', 'POST']:
        # Check if the path starts with the parent directory

        # Allow requests to files in the static directory
        if path.startswith('/static/css/') or path.startswith('/translator') or path.startswith('/translate') or path.startswith('/') or path.startswith('/req') or path.startswith('/train') or path.startswith('/static/js/') or path.startswith('/login') or path.startswith('/signup') or path.startswith('/logout'):
            return None
        else:
            abort(403, "Your request is not authorized.")
    else:
        abort(403, "Your request is not authorized.")

@app.route('/static/css/login.css')
def serve_css():
    response = make_response(render_template('login.css'))
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.route('/')
def home():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/translator")
def translator():
    return render_template("translate.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # Check if the username is already taken
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if client_ip in blacklisted_ips:
            return render_template('signup.html', error='Your IP is blacklisted, you cannot sign up for this website')

        if result:
            # Username is already taken
            return render_template('signup.html', error='Username is already taken')

        else:
            # Insert the new user into the database
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            # Close the database connection
            conn.close()

            # Set the session variable and redirect to the home page
            session.permanent = True
            session['username'] = username
            return redirect(url_for('home'))

    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # Check if the username and password are correct
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        if client_ip in blacklisted_ips:
            return render_template('login.html', error='Your IP is blacklisted, you cannot log in to this website')

        if result:
            # Username and password are correct, set the session variable and redirect to the home page
            session.permanent = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Username or password is incorrect
            return render_template('login.html', error='Invalid username or password')

    else:
        return render_template('login.html')

@app.route('/translate', methods=['POST'])
def translate():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    input_text = request.form['input_text']
    model_input = request.form['model']
    
    # Add the translation request to the queue
    translation_queue.put((input_text, model_input))

    # Return a message indicating that the request has been queued
    print(client_ip + " Has been put in the queue")
    return process_translation_queue()

@app.route('/req', methods=['GET'])
def requirements():
    return render_template("requirements.html")

@app.route("/train", methods=["POST"])
def train():
    model = request.form["model"]
    print("Received model:", model)
    translate_text = ValdevianTranslator(model)
    translate_text.train()
    print("Training Complete!")
    return "Training Complete!"
@app.route("/logout")
def logout():
    # Clear the session data related to the user
    session.pop('username', None)
    # Redirect the user to the login page
    return redirect(url_for('login'))


def process_translation_queue():
    while True:
        # Get the next translation request from the queue
        input_text, model_input = translation_queue.get()

        # Translate the input text
        translate_text = ValdevianTranslator(model_input)
        translated_text = translate_text.generate_response(input_text)

        # Print the translated text
        print(translated_text)

        # Mark the request as complete
        translation_queue.task_done()
        return translated_text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")

