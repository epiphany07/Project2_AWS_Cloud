from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from collections import Counter

app = Flask(__name__, template_folder='templates')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "mydatabase.db")

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    address = request.form['address']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email, address))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect(url_for('profile', username=username))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

@app.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}": {}'.format(letter, count))
    return '<br>'.join(response)

if __name__ == '__main__':
  app.run(debug=True)