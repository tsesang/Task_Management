from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['DATABASE'] = 'User_Data.db'
app.config['SECRET_KEY'] = 'secretkey'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<custom_route>') # dynamic route
def custom_fun(custom_route):
    return f'This page is for {custom_route}'

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signUp.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        
        db = get_db()
        cursor = db.cursor()
        
        # Execute the SELECT statement with a WHERE clause
        cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
        
        # Fetch the result (email)
        result = cursor.fetchone()

        # Check if the result is not None
        if result:
            email = result[0]
            return render_template('signup.html', msg="Email already exists")

        # Hash the password before storing it
        else:
            if password == cpassword:
                hashed_password = generate_password_hash(password)

                # Insert the user data into the database
                cursor.execute('INSERT INTO users (email, name, password, confirmpassword) VALUES (?, ?, ?, ?)', (email, name, hashed_password, cpassword))
                db.commit()

                return render_template('signup.html', msg="Signup successful")
            else:
                return render_template('signup.html', msg='Sign up unsuccessful! Passwords do not match.')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        
        # Execute the SELECT statement with a WHERE clause to check if the email exists
        cursor.execute('SELECT email, password FROM users WHERE email = ?', (email,))
        
        # Fetch the result (email and hashed password)
        result = cursor.fetchone()

        # Check if the result is not None (email exists)
        if result:
            stored_email, stored_hashed_password = result
            if check_password_hash(stored_hashed_password, password):
                # Password matches; login successful
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect('/')
            else:
                # Incorrect password
                flash('Incorrect password. Please try again.', 'error')
        else:
            # Email not found
            flash('Email not found. Please sign up.', 'error')

        return render_template('login.html')


@app.route('/')
def form_page():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
