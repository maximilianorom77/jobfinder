import sqlite3


class JobsDB:
    
    def __init__(self):
        self.conn = sqlite3.connect("posts.sqlite3")
        self.cursor = self.conn.cursor()
        self.visited = set()
        self.setup()
        self.get_posts_visited()

    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS posts(url, title, body)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS posts_words(url, words)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS posts_visited(url)")
        self.conn.commit()

    def get_posts_visited(self):
        self.cursor.execute("SELECT url FROM posts_visited")
        self.visited = set(self.cursor.fetchall())

    def post_visited(self, post_url):
        self.cursor.execute(f"INSERT INTO posts_visited(url) VALUES (?)", (post_url,))
        self.visited.add(post_url)

    def is_visited(self, post_url):
        return post_url in self.visited

    def save_post(self, url, post_title, post_body, words):
        self.cursor.execute("INSERT INTO posts(url, title, body) VALUES (?, ?, ?)", (url, post_title, post_body))
        self.cursor.execute("INSERT INTO posts_words(url, words) VALUES (?, ?)", (url, words))
        self.post_visited(url)

    def get_posts_words(self):
        self.cursor.execute("SELECT words FROM posts_words")
        return self.cursor.fetchall()
