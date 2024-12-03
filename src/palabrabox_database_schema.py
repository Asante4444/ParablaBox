import sqlite3
import logging
from typing import List, Tuple, Dict, Any

# Configure logging for better error tracking and debugging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class PalabraBoxDatabase:
    def __init__(self, database_path: str):
        """
        Initialize the database connection with a path.
        
        This approach allows for more flexible database management:
        - Centralized connection handling
        - Easier error tracking
        - Potential for connection pooling in future
        """
        self.database_path = database_path
        self.conn = None
        self.cursor = None

    def _connect(self):
        """
        Establish a database connection with error handling.
        
        Key Considerations:
        - Use context manager for automatic resource management
        - Implement connection timeout
        - Allow for potential custom SQLite configurations
        """
        try:
            self.conn = sqlite3.connect(
                self.database_path, 
                timeout=10,  # 10-second timeout for locks
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            logger.info(f"Successfully connected to database: {self.database_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def _close(self):
        """
        Safely close database connections and handle potential errors.
        """
        if self.conn:
            try:
                self.conn.close()
                logger.info("Database connection closed")
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection: {e}")

    def create_schema(self):
        """
        Create comprehensive database schema with robust error handling.
        
        Design Philosophy:
        - Use IF NOT EXISTS to prevent schema recreation errors
        - Implement cascading deletes for referential integrity
        - Add explicit constraints and checks
        """
        self._connect()
        try:
            # Words Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spanish_word TEXT NOT NULL,
                english_translation TEXT NOT NULL,
                part_of_speech TEXT CHECK(
                    part_of_speech IN (
                        'noun', 'verb', 'adjective', 'adverb', 
                        'preposition', 'conjunction', 'pronoun', 'interjection'
                    )
                ),
                difficulty_level INTEGER CHECK(difficulty_level BETWEEN 1 AND 5),
                date_added DATETIME DEFAULT (datetime('now', 'localtime')),
                UNIQUE(spanish_word, english_translation)
            )''')

            # Word Details Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_details (
                word_id INTEGER PRIMARY KEY,
                example_sentence TEXT,
                pronunciation TEXT,
                etymology TEXT,
                usage_notes TEXT,
                FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE
            )''')

            # Categories Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT
            )''')

            # Word Categories Junction Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_categories (
                word_id INTEGER,
                category_id INTEGER,
                PRIMARY KEY (word_id, category_id),
                FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE,
                FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
            )''')

            self.conn.commit()
            logger.info("Database schema created successfully")

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Schema creation failed: {e}")
            raise
        finally:
            self._close()

    def insert_words(self, words: List[Tuple]) -> List[int]:
        """
        Insert words with robust ID retrieval.
        
        Explicit steps:
        1. Begin transaction
        2. Insert words
        3. Retrieve IDs via explicit query
        4. Handle potential insertion failures
        
        Args:
            words: List of tuples (spanish_word, english_translation, part_of_speech, difficulty_level)
        
        Returns:
            List of inserted word IDs
        """
        self._connect()
        word_ids = []

        try:
            # Start transaction
            self.cursor.execute('BEGIN')

            # Insert words
            self.cursor.executemany('''
                INSERT INTO words (
                    spanish_word, english_translation, 
                    part_of_speech, difficulty_level
                ) VALUES (?, ?, ?, ?)
            ''', words)

            # Explicitly retrieve inserted IDs
            inserted_words = [word[0] for word in words]
            placeholders = ','.join(['?'] * len(inserted_words))
            
            self.cursor.execute(f'''
                SELECT id FROM words 
                WHERE spanish_word IN ({placeholders})
                ORDER BY id DESC
                LIMIT {len(inserted_words)}
            ''', inserted_words)

            word_ids = [row['id'] for row in self.cursor.fetchall()]
            word_ids.reverse()  # Restore original insertion order

            self.conn.commit()
            logger.info(f"Successfully inserted {len(word_ids)} words")
            
            return word_ids

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Word insertion failed: {e}")
            raise
        finally:
            self._close()
    """
    def reset_database(self):
        #Utility to reset the database for testing.
        self._connect()
        try:
            self.cursor.execute('DROP TABLE IF EXISTS words')
            self.cursor.execute('DROP TABLE IF EXISTS word_details')
            self.cursor.execute('DROP TABLE IF EXISTS categories')
            self.cursor.execute('DROP TABLE IF EXISTS word_categories')
            self.conn.commit()
            logger.info("Database reset successfully")
        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Database reset failed: {e}")
        finally:
            self._close()
    """

def main():
    """
    Demonstration of database initialization and word insertion
    """
    db_path = r'D:\Computer science\PalabraBox\db\palabrabox.db'
    palabrabox_db = PalabraBoxDatabase(db_path)

    try:
        """
        # Reset the database (for testing purposes)
        palabrabox_db.reset_database()
        """
        # Create schema
        palabrabox_db.create_schema()

        # Sample words for insertion
        sample_words = [
            ('perro', 'dog', 'noun', 1),
            ('correr', 'to run', 'verb', 2),
            ('rápido', 'fast', 'adjective', 3)
        ]

        # Insert words and get their IDs
        word_ids = palabrabox_db.insert_words(sample_words)
        print(f"Inserted word IDs: {word_ids}")

    except Exception as e:
        logger.error(f"An error occurred in main execution: {e}")

if __name__ == '__main__':
    main()
