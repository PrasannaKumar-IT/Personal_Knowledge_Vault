import sqlite3
conn = sqlite3.connect("vault.db")
cursor=conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

def add_note():
    title=input("Enter a Title: ").strip()
    content=input("Enter a note: ").strip()
    category=input("Enter a category: ").strip()
    tags=input("Enter the Tags: ").strip()
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute('''Insert into notes (title,content,category,tags) values (?,?,?,?)''',(title,content,category,tags))
    conn.commit()
    conn.close()
    print("✅ Note added successfully!")

def view_notes():
    conn=sqlite3.connect('vault.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
    notes=cursor.fetchall()
    conn.close()
    if not notes:
        print("📭 No notes found.")
        return
    for note in notes:
        print('-'*40)
        print(f"ID: {note[0]}")
        print(f"Title: {note[1]}")
        print(f"Note: {note[2]}")
        print(f"Category: {note[3]}")
        print(f"Tags: {note[4]}")
        print(f"Created at: {note[5]}")
        print('-'*40)

def search_note():
    keyword=input("Enter a Keyword to Search: ").strip()
    conn=sqlite3.connect("vault.db")
    cursor=conn.cursor()
    cursor.execute('''SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC''', (f'%{keyword}%', f'%{keyword}%'))
    results=cursor.fetchall()
    conn.close()
    if not results:
        print("NO Match Found")
        return
    print(f"\nFound {len(results)} matching note(s):\n")
    for note in results:
        print('-'*40)
        print(f"ID: {note[0]}")
        print(f"Title: {note[1]}")
        print(f"Note: {note[2]}")
        print(f"Category: {note[3]}")
        print(f"Tags: {note[4]}")
        print(f"Created at: {note[5]}")
        print('-'*40)
def filter_notes():
    print("\Filter Options:")
    print("1. Filter by Category")
    print("2. Filter by Tag")
    choice = input("Choose an option (1/2): ").strip()
    if choice=='1':
        category=input("Enter a category: ").strip()
        query="select * from notes where category=? order by created_at DESC"
        params=(category,)
    elif choice=='2':
        tag=input("Enter a tag for filter: ")
        query="select * from notes where tags like ? order by created_at DESC"
        params=(f"%{tag}%")
    else:
        print("Invalid Option!")
        return
    conn=sqlite3.connect('vault.db')
    cursor=conn.cursor()
    cursor.execute(query,params)
    results=cursor.fetchall()
    conn.close()
    if not results:
        print("NO Match Found")
        return
    print(f"\nFound {len(results)} matching note(s):\n")
    for note in results:
        print('-'*40)
        print(f"ID: {note[0]}")
        print(f"Title: {note[1]}")
        print(f"Note: {note[2]}")
        print(f"Category: {note[3]}")
        print(f"Tags: {note[4]}")
        print(f"Created at: {note[5]}")
        print('-'*40)
filter_notes()