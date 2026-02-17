"""
Quick test of knowledge database
"""
from db_manager import KnowledgeDB

print("\n" + "="*60)
print("TESTING FARMING KNOWLEDGE DATABASE")
print("="*60)

# Initialize database
print("\nInitializing database...")
db = KnowledgeDB()

# Test queries
test_queries = [
    "what to plant in monsoon",
    "my soil is not fertile",
    "how to save water",
    "insects eating my crops",
    "want to earn more money"
]

print("\n" + "="*60)
print("SEARCH RESULTS")
print("="*60)

for query in test_queries:
    print(f"\n>>> Query: {query}")
    results = db.search(query, top_k=1)
    if results:
        print(f"    Found: {results[0]['question']}")
        print(f"    Category: {results[0]['category']}")
        print(f"    Answer: {results[0]['answer'][:150]}...")
    else:
        print("    No results found")

print("\n" + "="*60)
print("AVAILABLE CATEGORIES")
print("="*60)
categories = db.get_all_categories()
for cat in categories:
    print(f"  - {cat}")

print("\n" + "="*60)
print("DATABASE TEST COMPLETE!")
print("="*60)
