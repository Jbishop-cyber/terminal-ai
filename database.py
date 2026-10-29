import sqlite3
import os
# import string

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE = os.path.join(BASE_DIR, "conversation.db")

DATA_DIR = os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "jay",
)

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE = os.path.join(DATA_DIR, "conversation.db")

STOP_WORDS = {
    "what", "is", "my", "the", "a", "an",
    "do", "does", "did", "i", "you",
    "me", "about", "are", "am", "to",
    "of", "in", "on", "for", "and"
}


def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS messages (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           role TEXT,
           content TEXT
       )
   """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)",
                   (role, content))

    conn.commit()
    conn.close()


def save_memory(content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM memories  WHERE content = ?",
        (content,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "Memory already exists."

    cursor.execute(
        "INSERT INTO memories (content) VALUES (?)",
        (content,)
    )

    conn.commit()
    conn.close()

    return "Memory saved successfully."


def update_memory(memory_id, new_content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE memories SET content = ? WHERE id = ?",
        (new_content, memory_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return "Memory not found."

    conn.close()
    return "Memory updated successfully."


def forget_memory(memory_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memories WHERE id = ?",
        (memory_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return "Memory not found."

    conn.close()
    return "Memory forgotten successfully."


def get_memories():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM memories")
    rows = cursor.fetchall()

    conn.close()

    return rows


def search_memories(query):
    keywords = [
        word.strip(".,!?;:").lower()
        for word in query.split()
        if word.strip(".,!?;:").lower() not in STOP_WORDS
    ]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    scores = {}

    for keyword in keywords:
        cursor.execute(
            "SELECT id, content FROM memories WHERE content LIKE ?",
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        for row in rows:
            memory_id, content = row

            if memory_id not in scores:
                scores[memory_id] = {
                    "content": content,
                    "score": 0
                }

            scores[memory_id]["score"] += 1

    conn.close()

    ranked_memories = sorted(
        scores.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    return [
        (memory_id, data["content"])
        for memory_id, data in ranked_memories[:5]
    ]


def load_messages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT role, content From messages")
    rows = cursor.fetchall()

    conn.close()

    conversation = []

    for role, content in rows:
        conversation.append({
            "role": role,
            "content": content
        })

    return conversation
