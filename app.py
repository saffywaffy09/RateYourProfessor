from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index ():
    connection = get_db_connection()
    info = connection.execute("SELECT * FROM allInfo").fetchall()
    connection.close()
    return render_template("index.html", allInfo=info)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    return conn

if __name__ == '__main__':
    app.run(debug=True)