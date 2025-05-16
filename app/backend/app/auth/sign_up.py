from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
import psycopg2
from config import db_config, transactionTypes

auth_bp = Blueprint('sign_up', __name__, url_prefix='/auth')

# route for sign up
@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        data = request.get_json(force=True)  # force parsing as JSON
    except Exception as e:
        return jsonify({'message': 'Invalid JSON'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({ 'message': 'Missing username and/or password' }), 400
    
    hashed_password = generate_password_hash(password)
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**db_config())
        cur = conn.cursor()
        # check if username exists
        cur.execute("SELECT * FROM Users WHERE username = %s;", (username,))
        results = cur.fetchall()
        
        if len(results) != 0:
            return jsonify({ 'message': 'Already used username' }), 409
        else:
            # Insert new user
            cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s);", (username, hashed_password))
            conn.commit()
            return jsonify({ 'message': 'Successfully signed up a new account' }), 201
    
    except Exception as e:
        print("DB Error:", e)
        return jsonify({'message': 'Database error'}), 500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()