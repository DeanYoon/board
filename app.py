from flask import Flask, render_template,redirect,url_for,request,jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/signup/')
def signup():
       return render_template("signup.html")
@app.route('/boards/')
def boards():
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boards')
    boards = cursor.fetchall()
    conn.close()
    return render_template("boards.html", boards=boards)


@app.route('/boards/<board_id>/')
def posts(board_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM posts WHERE board_id = {board_id}')
    posts = cursor.fetchall()

    return render_template("posts.html", posts=posts)


@app.route('/boards/<board_id>/posts/<post_id>/')
def detail_post(board_id,post_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM posts WHERE id = {post_id}')
    post = cursor.fetchone()
    conn.close()

    return render_template("post_detail.html", post=post)












@app.route('/api/login',methods = ['POST'])
def login_api():
   username = request.form['username']
   password = request.form['password']

   conn = sqlite3.connect('notice_board.db')
   cursor = conn.cursor()

   cursor.execute('SELECT * FROM users WHERE username=?', (username,))
   user = cursor.fetchone()
   conn.close()
   print(user)
   
   if user is None:
       return 'No user found', 400
   
   elif user is not None and user[2] == password:
      return  redirect(url_for("boards"))
   else:
      return 'Wrong Password', 400

@app.route('/api/signup',methods = ['POST'])
def signup_api():
   username = request.form['username']
   password = request.form['password']
   password_conf = request.form['password_conf']
   if password != password_conf:
       return 'Wrong Password',400

   conn = sqlite3.connect('notice_board.db')
   cursor = conn.cursor()

   cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
   conn.commit()

   cursor.execute('SELECT * FROM users')
   user = cursor.fetchone()   
   conn.close()
  
   if user:
      return  redirect(url_for("boards"))

   else:
       return 'Problem',400

if __name__ == '__main__':
    app.run( debug=True)


