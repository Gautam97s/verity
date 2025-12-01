import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "verity.db")

def inspect_db():
    if not os.path.exists(DB_PATH):
        print("Database file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Table Info: business ---")
    try:
        cursor.execute("PRAGMA table_info(business)")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
            # col structure: (cid, name, type, notnull, dflt_value, pk)
    except Exception as e:
        print(f"Error getting table info: {e}")

    print("\n--- Existing Business Records ---")
    try:
        cursor.execute("SELECT * FROM business")
        rows = cursor.fetchall()
        print(f"Total rows: {len(rows)}")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error querying business table: {e}")

    conn.close()

if __name__ == "__main__":
    inspect_db()
