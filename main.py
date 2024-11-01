from flask import Flask, render_template
import util

app = Flask(__name__)

# Database connection details
username = 'raywu1990'
password = 'test'
host = '127.0.0.1'
port = '5432'
database = 'dvdrental'

@app.route('/')
def home():
    return "Welcome to the Flask App! Use /api/update_basket_a or /api/unique"

@app.route('/api/update_basket_a')
def update_basket_a():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    try:
        cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
        connection.commit()
        util.disconnect_from_db(connection, cursor)
        return "Success!"
    except Exception as error:
        util.disconnect_from_db(connection, cursor)
        return f"Error: {error}"

@app.route('/api/unique')
def unique_fruits():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    try:
        # Fetch unique fruits from basket_a
        unique_a = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_a FROM basket_a;")
        unique_b = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_b FROM basket_b;")
        
        if unique_a == -1 or unique_b == -1:
            return "Error fetching unique fruits"
        
        # Prepare the data to display in the HTML table
        util.disconnect_from_db(connection, cursor)
        return render_template('index.html', unique_a=[row[0] for row in unique_a], unique_b=[row[0] for row in unique_b])
    except Exception as error:
        util.disconnect_from_db(connection, cursor)
        return f"Error: {error}"

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
