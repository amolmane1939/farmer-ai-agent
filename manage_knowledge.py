"""
Utility script to manage farming knowledge database
"""
from db_manager import KnowledgeDB

def test_search():
    """Test knowledge search"""
    db = KnowledgeDB()
    
    test_queries = [
        "what to plant in monsoon",
        "my soil is not fertile",
        "how to save water",
        "insects eating my crops",
        "want to earn more money"
    ]
    
    print("\n" + "="*60)
    print("TESTING KNOWLEDGE SEARCH")
    print("="*60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = db.search(query, top_k=1)
        if results:
            print(f"Found: {results[0]['question']}")
            print(f"Relevance: {results[0]['relevance']:.2f}")
            print(f"Answer preview: {results[0]['answer'][:100]}...")
        else:
            print("No results found")

def add_new_knowledge():
    """Add new knowledge to database"""
    db = KnowledgeDB()
    
    print("\n" + "="*60)
    print("ADD NEW KNOWLEDGE")
    print("="*60)
    
    category = input("\nCategory (crops/soil/pest/water/profit/fertilizer/storage/weather/technology): ")
    question = input("Question: ")
    answer = input("Answer: ")
    
    db.add_knowledge(category, question, answer)
    print("\nKnowledge added successfully!")

def show_categories():
    """Show all categories"""
    db = KnowledgeDB()
    categories = db.get_all_categories()
    
    print("\n" + "="*60)
    print("AVAILABLE CATEGORIES")
    print("="*60)
    for cat in categories:
        print(f"- {cat}")

if __name__ == "__main__":
    print("\nFARMING KNOWLEDGE DATABASE MANAGER")
    
    while True:
        print("\n" + "="*60)
        print("1. Test search")
        print("2. Add new knowledge")
        print("3. Show categories")
        print("4. Exit")
        print("="*60)
        
        choice = input("\nChoose option (1-4): ")
        
        if choice == "1":
            test_search()
        elif choice == "2":
            add_new_knowledge()
        elif choice == "3":
            show_categories()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
