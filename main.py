from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from flask_session import Session
from api.auth import auth_bp
from api.post import post_api_bp
from api.comment import comment_bp_api
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.register_blueprint(auth_bp)
app.register_blueprint(post_api_bp)
app.register_blueprint(comment_bp_api)


if __name__ == '__main__':
    app.run(debug=True)
