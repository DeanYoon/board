from flask import Flask, render_template, redirect, url_for, request, session
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
    return render_template("add_post.html", board_id=board_id)


@app.route('/boards/<board_id>/')
def posts(board_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT posts.*,users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.board_id = {board_id}')
    posts = cursor.fetchall()
  # Retrieve the name of the board
    cursor.execute(f'SELECT name FROM boards WHERE id = {board_id}')
    board_name = cursor.fetchone()[0]
    return render_template("posts.html", posts=posts, title=board_name)


@app.route('/boards/<board_id>/posts/<post_id>/')
def detail_post(board_id, post_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    # Update view count
    cursor.execute(f'UPDATE posts SET views = views + 1 WHERE id = {post_id}')
    conn.commit()
    cursor.execute(
        f'SELECT posts.*,users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = {post_id}')
    post = cursor.fetchone()
    cursor.execute(
        f'SELECT comments.user_id, comments.content, comments.likes, comments.created_at, users.username,comments.id FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = {post_id}')
    comments = cursor.fetchall()

    conn.close()

    post_data = {
        'title': post[1],
        'content': post[2],
        'posted_date': post[3],
        'views': post[4],
        'user_id': post[5],
        'board_id': post[6],
        'owner_name': post[7]
    }
    comments_list = []
    for comment in comments:
        comment_dict = {
            'user_id': comment[0],
            'content': comment[1],
            'likes': comment[2],
            'created_at': comment[3],
            'username': comment[4],
            'id': comment[5]
        }
        comments_list.append(comment_dict)
    # 현재 로그인한 상태라면
    try:
        current_user = session['user_id']
    except:
        current_user = ''

    return render_template("post_detail.html", post_data=post_data, comments=comments_list, post_id=post_id, board_id=board_id, current_user=current_user)


@app.route('/boards/<board_id>/posts/<post_id>/edit')
def edit_post(board_id, post_id):

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM posts WHERE id=?', (post_id,))
    post = cursor.fetchone()
    post_data = {
        'title': post[1],
        'content': post[2],
    }

    conn.close()
    return render_template("edit_post.html", board_id=board_id, post_id=post_id, post_data=post_data)

# API


@app.route('/api/login', methods=['POST'])
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
        return redirect(url_for("boards"))
    else:
        return 'Wrong Password', 400


@app.route('/api/signup', methods=['POST'])
def signup_api():
    username = request.form['username']
    password = request.form['password']
    password_conf = request.form['password_conf']
    if password != password_conf:
        return 'Wrong Password', 400

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        return redirect(url_for("boards"))

    else:
        return 'Problem', 400


@app.route('/api/boards', methods=['POST'])
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
    return redirect(url_for("boards"))


@app.route('/api/boards/<board_id>/posts', methods=['POST'])
def add_post_api(board_id):
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    time_now = datetime.datetime.now()
    time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
    user_id = session['user_id']

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    new_post = (post_title, post_content, time_str, 0, user_id, board_id)
    cursor.execute(
        'INSERT INTO posts (title, content, created_at, views, user_id, board_id) VALUES (?, ?, ?, ?, ?, ?)', new_post)

    conn.commit()
    conn.close()
    return redirect(url_for("posts", board_id=board_id))


@app.route('/api/boards/<board_id>/posts/<post_id>', methods=['POST'])
def edit_post_api(board_id, post_id):
    post_title = request.form['post_title']
    post_content = request.form['post_content']

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE posts SET title = ?, content = ? WHERE id = ?',
        (post_title, post_content, post_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("detail_post", board_id=board_id, post_id=post_id))


@app.route('/api/boards/<board_id>/posts/<post_id>', methods=['DELETE'])
def del_post_api(board_id, post_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    # delete the post with the given post_id

    cursor.execute(
        'DELETE FROM posts WHERE id = ?', (post_id,)
    )
    # delete comments with the same post_id
    cursor.execute(
        'DELETE FROM comments WHERE post_id = ?', (post_id,)
    )
    conn.commit()
    conn.close()
    return '200'


@app.route('/api/boards/<board_id>/posts/<post_id>/comments', methods=['POST'])
def add_comment_api(board_id, post_id):
    comment = request.form['comment']
    try:
        user_id = session['user_id']
    except:
        redirect(url_for('login'))
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    new_comment = (post_id, user_id, comment, time_now, 0)
    cursor.execute(
        'INSERT INTO comments (post_id, user_id, content, created_at,likes) VALUES (?,?,?,?,?)', new_comment
    )

    conn.commit()
    conn.close()
    return redirect(url_for("detail_post", board_id=board_id, post_id=post_id))


@app.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment_api(comment_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()

    return '200'


@app.route('/api/comments/<comment_id>', methods=['PUT'])
def edit_comment_api(comment_id):
    comment_text = request.form.get('comment_text')
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE comments SET content = ?  WHERE id = ?',
        (comment_text, comment_id)
    )
    conn.commit()
    conn.close()

    return '200'


if __name__ == '__main__':
    app.run(debug=True)
