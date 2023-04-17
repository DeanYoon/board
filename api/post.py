from flask import Blueprint, request, redirect, url_for, session, render_template
import sqlite3
import datetime

post_api_bp = Blueprint('post_api', __name__)


@post_api_bp.route('/boards/')
def boards():
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boards')
    boards = cursor.fetchall()
    conn.close()
    return render_template("boards.html", boards=boards)


@post_api_bp.route('/add_board/')
def add_board():
    try:
        session['user_id']
    except:
        return redirect(url_for('login'))
    return render_template("add_board.html")


@post_api_bp.route('/search/')
def search():
    return render_template('search.html')


@post_api_bp.route('/boards/<board_id>/add_post/')
def add_post(board_id):
    try:
        session['user_id']
    except:
        return redirect(url_for('login'))
    return render_template("add_post.html", board_id=board_id)


@post_api_bp.route('/boards/<board_id>/')
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


@post_api_bp.route('/boards/<board_id>/posts/<post_id>/')
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


@post_api_bp.route('/boards/<board_id>/posts/<post_id>/edit')
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


@post_api_bp.route('/api/boards/<board_id>/posts', methods=['POST'])
def add_post_api(board_id):
    try:
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
        return '200'
    except:
        return 'wrong', 400


@post_api_bp.route('/api/boards/<board_id>/posts/<post_id>', methods=['POST'])
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


@post_api_bp.route('/api/boards/<board_id>/posts/<post_id>', methods=['DELETE'])
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


@post_api_bp.route('/api/search', methods=['GET'])
def get_posts_search():
    search_query = request.args.get('query')
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.title LIKE '%{search_query}%'")
    results = cursor.fetchall()
    conn.close()

    return results, '200'


# board api
@post_api_bp.route('/api/boards', methods=['POST'])
def add_board_api():
    board_name = request.form['board_name']
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM boards WHERE name=?', (board_name,))
    board = cursor.fetchone()
    if (board):
        return 'Board Already Exist', 404

    cursor.execute('INSERT INTO boards (name) VALUES ( ?)', (board_name,))
    conn.commit()
    conn.close()
    return '200'
