import sqlite3
import logging
from knowledge_base import FARMING_KNOWLEDGE

logger = logging.getLogger(__name__)


class KnowledgeDB:
    def __init__(self, db_path="farming_knowledge.db"):
        """Initialize SQLite database with FTS5."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._populate_database()

    def _create_tables(self):
        """Create FTS5 table for full-text search."""
        self.cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts
            USING fts5(category, question, answer, keywords)
        ''')
        self.conn.commit()

    def _populate_database(self):
        """Add farming knowledge to database if not already populated."""
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_fts")
        count = self.cursor.fetchone()[0]

        if count > 0:
            logger.info(f"Loaded existing knowledge base with {count} entries")
            return

        try:
            for item in FARMING_KNOWLEDGE:
                keywords = self._extract_keywords(
                    item['question'] + ' ' + item['answer']
                )
                self.cursor.execute(
                    "INSERT INTO knowledge_fts (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
                    (item['category'], item['question'], item['answer'], keywords)
                )
            self.conn.commit()
            logger.info(f"Added {len(FARMING_KNOWLEDGE)} knowledge entries to database")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to populate knowledge database: {e}")
            raise

    def _extract_keywords(self, text):
        """Extract important keywords from text."""
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are',
            'was', 'were', 'how', 'what', 'when', 'where', 'why'
        }
        words = text.lower().split()
        keywords = [w.strip('.,!') for w in words
                    if w.strip('.,!') not in common_words and len(w) > 3]
        return ' '.join(keywords[:20])

    def search(self, query, top_k=2):
        """Search for relevant knowledge using FTS5."""
        try:
            # Sanitize: only strip characters that break FTS5 syntax
            # Keep '?' as it is harmless in OR-joined terms
            sanitized = query.translate(
                str.maketrans('', '', '"\'^*()[]{}~:')
            )
            # Build OR query from individual words
            words = [w.strip() for w in sanitized.lower().split() if w.strip()]
            if not words:
                return []
            query_clean = ' OR '.join(words)

            self.cursor.execute(
                """SELECT category, question, answer, rank
                   FROM knowledge_fts
                   WHERE knowledge_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query_clean, top_k)
            )

            results = self.cursor.fetchall()
            return [
                {
                    'category': row[0],
                    'question': row[1],
                    'answer': row[2],
                    'relevance': abs(row[3])
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Knowledge search error: {e}")
            return []

    def add_knowledge(self, category, question, answer):
        """Add a new knowledge entry."""
        try:
            keywords = self._extract_keywords(question + ' ' + answer)
            self.cursor.execute(
                "INSERT INTO knowledge_fts (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
                (category, question, answer, keywords)
            )
            self.conn.commit()
            logger.info(f"Added new knowledge entry: {question}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to add knowledge entry: {e}")
            raise

    def get_all_categories(self):
        """Get sorted list of all categories from the database."""
        try:
            self.cursor.execute("SELECT DISTINCT category FROM knowledge_fts ORDER BY category")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to fetch categories: {e}")
            return []

    def close(self):
        """Close database connection."""
        try:
            self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")
