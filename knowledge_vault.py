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
    print("\nFilter Options:")
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
        params=(f"%{tag}%",)
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
    for note in results:
        print('-'*40)
        print(f"ID: {note[0]}")
        print(f"Title: {note[1]}")
        print(f"Note: {note[2]}")
        print(f"Category: {note[3]}")
        print(f"Tags: {note[4]}")
        print(f"Created at: {note[5]}")
        print('-'*40)

def update_note():
    id=input("Enter the ID of the note to update: ").strip()
    conn=sqlite3.connect("vault.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = cursor.fetchone()
    if not note:
        print("Note not found.")
        conn.close()
        return
    print("\nLeave a field empty if you don't want to change it.\n")
    new_title = input(f"New Title [{note[1]}]: ").strip() or note[1]
    new_content = input(f"New Content [{note[2]}]: ").strip() or note[2]
    new_category = input(f"New Category [{note[3]}]: ").strip() or note[3]
    new_tags = input(f"New Tags [{note[4]}]: ").strip() or note[4]

    cursor.execute("""
        UPDATE notes 
        SET title = ?, content = ?, category = ?, tags = ?
        WHERE id = ?
    """, (new_title, new_content, new_category, new_tags, id))
    conn.commit()
    conn.close()
    print("Note Updated Successfully!")

def delete_note():
    delete_id=input("Enter Id of the Note to delete: ")
    conn=sqlite3.connect("vault.db")
    cursor=conn.cursor()
    cursor.execute("Select * from notes where id=?",(delete_id,))
    note = cursor.fetchone()
    if not note:
        print("Note not found.")
        conn.close()
        return
    confirm=input(f"Are you sure you want to delete note '{note[1]}'? (y/n): ").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM notes WHERE id = ?", (delete_id,))
        conn.commit()
        print("Note deleted successfully!")
    else:
        print("Deletion cancelled.")

    conn.close()

def main():
    while True:
        print("\n📚 PERSONAL KNOWLEDGE VAULT")
        print("1. Add a new note")
        print("2. View all notes")
        print("3. Search notes by keyword")
        print("4. Filter notes by category or tag")
        print("5. Update a note")
        print("6. Delete a note")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            add_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            search_note()
        elif choice == '4':
            filter_notes()
        elif choice == '5':
            update_note()
        elif choice == '6':
            delete_note()
        elif choice == '7':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

