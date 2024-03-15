from flask import Flask, render_template, request, redirect, url_for, g
import Main
import sqlite3

app = Flask(__name__)
app.config["DATABASE"] = 'example.db'

# Define your routes

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    # Establish a database connection before each request
    g.db = Main.get_db_connection()


@app.teardown_request
def teardown_request(exception=None):
    # Close the database connection after each request
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Retrieve username and password from the form
            username = request.form['username']
            password = request.form['password']

            # Call the relevant function from Main.py
            Main.createUser(username, password)

            # Commit the transaction
            g.db.commit()

            # Redirect to another page or return a response
            return redirect(url_for('success'))  # Redirect to the success page
        except Exception as e:
            return f"An error occurred: {str(e)}"


@app.route('/success')
def success():
    return "User created successfully!"  # Display a success message


if __name__ == '__main__':
    app.run(debug=True)
