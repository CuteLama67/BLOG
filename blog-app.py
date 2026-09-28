import sqlite3
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("users-info.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/authors")
def show_authors():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM authors")
    rows = cursor.fetchall()
    conn.close()

    authors = []
    for row in rows:
        authors.append({
            "id": row["id"],
            "name": row["name"],
            "bio": row["bio"]
        })

    return jsonify(authors)


@app.route("/posts")
def show_posts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()

    posts = []
    for row in rows:
        posts.append({
            "id": row["id"],
            "title": row["title"],
            "content": row["content"],
            "author_id": row["author_id"],
            "views": row["views"]
        })

    return jsonify(posts)

@app.route("/posts/<int:id>")
def post_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (id, ))
    row = cursor.fetchone()

    post = {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "author_id": row["author_id"],
        "views": row["views"]
    }
    return jsonify(post)


if __name__ == "__main__":
    app.run(debug=True)

