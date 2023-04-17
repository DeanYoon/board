from flask import Blueprint, request, redirect, url_for, session
import sqlite3
import datetime

comment_bp_api = Blueprint('comment_api', __name__)


@comment_bp_api.route('/api/boards/<board_id>/posts/<post_id>/comments', methods=['POST'])
def add_comment_api(board_id, post_id):
    comment = request.form['comment']
    try:
        user_id = session['user_id']
    except:

        return redirect(url_for('login'))
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


@comment_bp_api.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment_api(comment_id):
    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()

    return '200'


@comment_bp_api.route('/api/comments/<comment_id>', methods=['PUT'])
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

# 좋아요,좋아요 취소 api


@comment_bp_api.route('/api/comments/<comment_id>/like', methods=['POST'])
def like_comment_api(comment_id):
    try:
        session['user_id']
    except:
        return redirect(url_for('login'))
    current_user_id = session['user_id']

    conn = sqlite3.connect('notice_board.db')
    cursor = conn.cursor()
    # get  current liked
    cursor.execute(
        f'SELECT liked_by_users from comments WHERE id={comment_id}'
    )

    try:
        comment_liked_users = [int(x) for x in cursor.fetchone()[0].split(',')]
    except:
        comment_liked_users = []
    if current_user_id not in comment_liked_users:
        comment_liked_users.append(current_user_id)
    else:
        comment_liked_users.remove(current_user_id)

    comment_num = len(comment_liked_users)
    comment_liked_users = ','.join(str(x) for x in comment_liked_users)

    cursor.execute(
        f"UPDATE comments SET liked_by_users = '{comment_liked_users}', likes={comment_num} WHERE id = {comment_id}",
    )
    conn.commit()
    conn.close()

    return '200'
