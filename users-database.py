import sqlite3

def init_db():
    conn = sqlite3.connect("users-info.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    bio TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    views INTEGER NOT NULL DEFAULT 0)""")

    conn.commit()
    conn.close()
    print("Database is ready")

def seed_db():
    conn = sqlite3.connect("users-info.db")
    cursor = conn.cursor()

    starter_authors = [('Алекс Тревел', 'Путешествую с рюкзаком. Фотограф, снимаю красивые пейзажи.'),
                        ('Лена Код', 'Пишу про Python, IT и будни разработчика 👩‍💻'),
                        ('Макс Фитнес', 'Твой онлайн-тренер. ЗОЖ, тренировки и правильное питание.')]

    starter_posts = [('Топ 5 скрытых пляжей на Бали', 'Сегодня расскажу про места, куда не добираются обычные туристы. Сохраняйте в закладки!', 1, 1450),
                    ('Как я выучила Python за полгода', 'Много практики, пет-проекты и бессонные ночи. Делюсь своим планом обучения и полезными ссылками.', 2, 3200),
                    ('Рецепт идеального завтрака', 'Овсяноблин с творожным сыром и лососем. Готовится 10 минут, заряжает энергией на полдня!', 3, 850),
                    ('Мой новый рабочий сетап', 'Наконец-то купила механическую клавиатуру и второй монитор. Теперь баги фиксятся в два раза быстрее :)', 2, 0),
                    ('Что обязательно взять в горы?', 'Собрал для вас чеклист самого необходимого: от аптечки до правильных треккинговых носков.', 1, 0)]

    cursor.executemany("INSERT INTO authors (name, bio) VALUES (?, ?)", starter_authors)
    cursor.executemany("INSERT INTO posts (title, content, author_id, views) VALUES (?, ?, ?, ?)", starter_posts)

    conn.commit()
    conn.close()
    print(f"Data has been added to the database")

if __name__ == "__main__":
    init_db()
    seed_db()

