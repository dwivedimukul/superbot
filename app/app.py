from flask import Flask, request, jsonify, session # type: ignore
import pyodbc  # type: ignore # For Azure SQL connection
from dotenv import load_dotenv
import os
from flask_cors import CORS
import json

load_dotenv()

SERVER_1 = os.getenv('DB_SERVER')
DATABASE_1 = os.getenv('DB_NAME')
UID_1 = os.getenv('DB_USER')
PWD_1 = os.getenv('DB_PASSWORD')
print(SERVER_1, DATABASE_1, UID_1, PWD_1)

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+SERVER_1+';DATABASE='+DATABASE_1+';UID='+UID_1+';PWD='+PWD_1+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()

@app.route('/user-role', methods=['GET'])
def user_role():
    try:
        data = request.get_json()
        if not data or 'username' not in data:
            return jsonify({"error": "Invalid JSON data"}), 400

        username = data['username']
        cursor.execute("SELECT [user_role] FROM [dbo].[employees] WHERE employee_name=?", (username,))
        row = cursor.fetchone()
        if row:
            result_dict = {column[0]: value for column, value in zip(cursor.description, row)}
        else:
            result_dict = {}

        # Serialize to JSON
        json_result = json.dumps(result_dict)
        print(json_result)
        return json_result
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    # engine = create_engine(connection_string)
    data=request.get_json()
    print(data)
    username = data['username']
    password = data['password']
    print(type(username))
    # with engine.connect() as connection:
    #     result = connection.execute("SELECT * FROM [dbo].[SuperBot] where username=? and password=?", (username, password))
    #     user = result.fetchone()
    cursor.execute("SELECT [employee_name] FROM [dbo].[login] where employee_email=? and password=?", (username, password))
    user = cursor.fetchone()
    # conn.close()

    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
