from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "secret",
    "database": "user_data"
}


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    code = data.get('code')

    if not email or not password or not code:
        return jsonify({"error": "All fields are required"}), 400

    try:

        hashed_password = generate_password_hash(password)

 
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

 
        query = "INSERT INTO user_inputs (email, password, code) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, hashed_password, code))
        conn.commit()

        return jsonify({"message": "Data saved successfully!"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)