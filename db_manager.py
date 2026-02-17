import sqlite3
import os
from knowledge_base import FARMING_KNOWLEDGE

class KnowledgeDB:
    def __init__(self, db_path="farming_knowledge.db"):
        """Initialize SQLite database with FTS"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._populate_database()
    
    def _create_tables(self):
        """Create FTS5 table for full-text search"""
        self.cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
            USING fts5(category, question, answer, keywords)
        ''')
        self.conn.commit()
    
    def _populate_database(self):
        """Add farming knowledge to database"""
        # Check if already populated
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_fts")
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            print(f"Loaded existing knowledge base with {count} entries")
            return
        
        for item in FARMING_KNOWLEDGE:
            # Extract keywords for better search
            keywords = self._extract_keywords(item['question'] + ' ' + item['answer'])
            self.cursor.execute(
                "INSERT INTO knowledge_fts (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
                (item['category'], item['question'], item['answer'], keywords)
            )
        
        self.conn.commit()
        print(f"Added {len(FARMING_KNOWLEDGE)} knowledge entries to database")
    
    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        # Simple keyword extraction - remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'how', 'what', 'when', 'where', 'why'}
        words = text.lower().split()
        keywords = [w for w in words if w not in common_words and len(w) > 3]
        return ' '.join(keywords[:20])  # Top 20 keywords
    
    def search(self, query, top_k=2):
        """Search for relevant knowledge using FTS"""
        try:
            # Clean query for FTS5
            query_clean = ' OR '.join(query.lower().split())
            
            # FTS5 search with ranking
            self.cursor.execute(
                """SELECT category, question, answer, rank 
                   FROM knowledge_fts 
                   WHERE knowledge_fts MATCH ? 
                   ORDER BY rank 
                   LIMIT ?""",
                (query_clean, top_k)
            )
            
            results = self.cursor.fetchall()
            knowledge_items = []
            
            for row in results:
                knowledge_items.append({
                    'category': row[0],
                    'question': row[1],
                    'answer': row[2],
                    'relevance': abs(row[3])  # FTS rank (lower is better, convert to positive)
                })
            
            return knowledge_items
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def add_knowledge(self, category, question, answer):
        """Add new knowledge entry"""
        keywords = self._extract_keywords(question + ' ' + answer)
        self.cursor.execute(
            "INSERT INTO knowledge_fts (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
            (category, question, answer, keywords)
        )
        self.conn.commit()
        print(f"Added new knowledge: {question}")
    
    def get_all_categories(self):
        """Get list of all categories"""
        categories = set()
        for item in FARMING_KNOWLEDGE:
            categories.add(item['category'])
        return sorted(list(categories))
    
    def close(self):
        """Close database connection"""
        self.conn.close()
