from db.connection import get_connection


class Task:
    def __init__(self, id, title, done):
        self.id = id
        self.title = title
        self.done = done

    @classmethod
    def get_all(cls, filter_status="all"):
        conn = get_connection()
        cur = conn.cursor()

        if filter_status == "completed":
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE done = TRUE AND is_deleted = FALSE ORDER BY id DESC"
            )
        elif filter_status == "pending":
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE done = FALSE AND is_deleted = FALSE ORDER BY id DESC"
            )
        else:
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE is_deleted = FALSE ORDER BY id DESC"
            )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [cls(*row) for row in rows]

    @classmethod
    def create(cls, title):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        cur.close()
        conn.close()

    def mark_complete(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET done = TRUE WHERE id = %s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()

    def soft_delete(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET is_deleted = TRUE WHERE id = %s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()
