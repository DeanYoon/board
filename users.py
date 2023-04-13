from flask import Flask, render_template,redirect,url_for,request,jsonify
import sqlite3


def login_api():
   username = request.form['username']
   password = request.form['password']

   conn = sqlite3.connect('board.db')
   cursor = conn.cursor()

   cursor.execute('SELECT * FROM users WHERE username=?', (username,))
   user = cursor.fetchone()
   conn.close()
   print(user)
   
   if user is not None and user[2] == password:
      return 'Logged in'
   else:
      return 'Invalid', 400
