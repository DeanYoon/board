from flask import Blueprint, request, session, redirect, url_for, render_template
import sqlite3

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def login():
    session.clear()

    return render_template("login.html")


@auth_bp.route('/signup/')
def signup():
    return render_template("signup.html")


@auth_bp.route('/api/login', methods=['POST'])
def login_api():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return 'No user found', 400

    elif user is not None and user[2] == password:
        session['user_id'] = user[0]
        return username, 200
    else:
        return 'Wrong Password', 400


@auth_bp.route('/api/signup', methods=['POST'])
def signup_api():
    username = request.form['username']
    password = request.form['password']
    password_conf = request.form['password_conf']
    if password != password_conf:
        return 'Wrong Password', 400

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if (user):
        return 'User Already Exists', 400

    cursor.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        return username, 200

    else:
        return 'Problem', 400
