import sqlite3

def get_db_connection(db_path):
    """Create and return a connection to the SQLite database."""
    try:
        connection = sqlite3.connect(db_path)
        print("Database connection successful.")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def verify_database(connection):
    """Verify that the database connection is valid by listing tables."""
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        if tables:
            print("Tables in database:", tables)
        else:
            print("No tables found in the database.")
    except sqlite3.Error as e:
        print(f"Error verifying database: {e}")
