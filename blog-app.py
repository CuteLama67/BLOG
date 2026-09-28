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


@app.route("/posts" , methods = ["GET", "POST"])
def show_posts():
    if request.method == "GET":
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

    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        title = data.get("title")
        content = data.get("content")
        author_id = data.get("author_id")

        if not title or not content or author_id is None:
            return jsonify({"error": "Fields title, content, author_id are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id, ))
        exist = cursor.fetchone()
        if exist:
            cursor.execute(
                "INSERT INTO posts (title, content, author_id, views) VALUES (?, ?, ?, ?)",
                (title, content, author_id, 0)
            )
        else: return {"error": "No such author"}, 400  

        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            "id": new_id,
            "title": title,
            "content": content,
            "author_id": author_id,
            "views": 0
        }), 201

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

