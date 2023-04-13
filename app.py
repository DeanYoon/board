from flask import Flask, render_template,redirect,url_for,request,session
import sqlite3
from flask_session import Session
import datetime



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def login():
    session.clear()
  
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


@app.route('/add_board/')
def add_board():
    try:
        session['user_id']
    except:
        return redirect(url_for('login'))
    return render_template("add_board.html")
@app.route('/boards/<board_id>/add_post/')
def add_post(board_id):
    try:
        session['user_id']
    except:
        return redirect(url_for('login'))
    return render_template("add_post.html",board_id=board_id)




@app.route('/boards/<board_id>/')
def posts(board_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT posts.*,users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.board_id = {board_id}')
    posts = cursor.fetchall()
    print(posts)
  # Retrieve the name of the board
    cursor.execute(f'SELECT name FROM boards WHERE id = {board_id}')
    board_name = cursor.fetchone()[0]
    return render_template("posts.html", posts=posts, title=board_name)


@app.route('/boards/<board_id>/posts/<post_id>/')
def detail_post(board_id,post_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT posts.*,users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = {post_id}')
    post = cursor.fetchone()
    print(post)
    title = post[1]
    content = post[2]
    views = post[4]
    owner_name = post[7]
    conn.close()

    return render_template("post_detail.html",title=title,content=content,views=views,owner_name=owner_name)












@app.route('/api/login',methods = ['POST'])
def login_api():
   username = request.form['username']
   password = request.form['password']

   conn = sqlite3.connect('notice_board.db')
   cursor = conn.cursor()

   cursor.execute('SELECT * FROM users WHERE username=?', (username,))
   user = cursor.fetchone()
   conn.close()
   session['user_id'] = user[0]

   
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


@app.route('/api/boards',methods = ['POST'])
def add_board_api():
    board_name = request.form['board_name']
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO boards (name) VALUES ( ?)', (board_name,))
    conn.commit()

    cursor.execute('SELECT * FROM boards')
    added_board = cursor.fetchone()   
    print(added_board)
    conn.close()    
    return  redirect(url_for("boards"))


@app.route('/api/boards/<board_id>/posts',methods = ['POST'])
def add_post_api(board_id):
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    time_now = datetime.datetime.now()
    time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
    user_id = session['user_id']

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    
    new_post = (post_title, post_content, time_str, 0, user_id, board_id)
    cursor.execute('INSERT INTO posts (title, content, created_at, views, user_id, board_id) VALUES (?, ?, ?, ?, ?, ?)', new_post)

    conn.commit()

    conn.close()    
    return  redirect(url_for("posts",board_id=board_id))


if __name__ == '__main__':
    app.run( debug=True)


