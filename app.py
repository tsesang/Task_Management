from flask import Flask, render_template, request, redirect, url_for, g,session,flash
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

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
        
        if email=='admin@gmail.com':
            if password == 'admin':
                return redirect('/admin')

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
                session['email'] = email;
                return redirect('/user')
            else:
                # Incorrect password
                return render_template('login.html',msg='Incorrect password Please try again error')
        else:
            # Email not found
            return render_template('login.html',msg='Email not found. Please sign up error')

        return render_template('login.html')

@app.route('/')
def form_page():
    return render_template('index.html')

# ... (other imports and setup)

@app.route('/user',methods=['POST','GET'])
def userpage():
    return render_template('userpage.html')

@app.route('/admin', methods=['POST', 'GET'])
def adminpage():
    if request.method == 'GET':
        return render_template('adminpage.html')
    elif not session.get('logged_in'):
        # Redirect to the login page if the user is not logged in
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('login'))
    else:
        email = request.form['email']
        task = request.form['task']
        status = "assigned"

        db = get_db()  # Call get_db within the route handler
        cursor = db.cursor()
                
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS TaskList (
                taskid INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                task TEXT,
                task_completed BOOLEAN
            )
        '''

                # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)
        db.commit()

        # Insert the email and task into the "tasks" table
        cursor.execute('INSERT INTO TaskList (email, task,task_completed) VALUES (?,?, ?)', (email, task,status))
        db.commit()
        
        return redirect('/get_all_data');
    
@app.route('/get_all_data')
def get_all_data():
    db = get_db()
    cursor = db.cursor()

    # Execute the SELECT statement to retrieve all data from the 'usertask' table
    cursor.execute('SELECT * FROM TaskList')

    # Fetch all the results
    data = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    db.close()

    # Return the data to be displayed in the template
    return render_template('adminpage.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

    
if __name__ == '__main__':
    app.run(debug=True)







