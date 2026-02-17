# Knowledge Database Guide

## What We Built

**SQLite with FTS5** - Fast full-text search database built into Python (no installation needed!)

Example:
- User asks: "what to grow in rainy season"
- Database finds: "Which crops to grow in Kharif season"
- Works with keywords and synonyms!

## How It Works

1. **Knowledge Base** (`knowledge_base.py`) - 15+ farming Q&A entries
2. **Database Manager** (`db_manager.py`) - SQLite FTS5 search engine
3. **Agent** (`app.py`) - Searches database first, then uses AI to format answer

## Installation

```bash
pip install -r requirements.txt
```

No extra packages needed - SQLite is built into Python!

## Test the Database

```bash
python manage_knowledge.py
```

Options:
1. Test search - Try sample queries
2. Add new knowledge - Add your own farming tips
3. Show categories - See all topics

## Add More Knowledge

### Method 1: Edit knowledge_base.py

Add to `FARMING_KNOWLEDGE` list:

```python
{
    "category": "crops",
    "question": "How to grow tomatoes",
    "answer": """Tomato Growing:
1. Sow in nursery - 4-5 weeks
2. Transplant - 6 inch spacing
3. Water regularly - Morning time
4. Support with stakes
5. Harvest - 60-80 days"""
}
```

### Method 2: Use manage_knowledge.py script

Run script and choose option 2.

## Categories

- crops - Crop selection, seasons
- soil - Fertility, pH, testing
- pest - Pest control, diseases
- water - Irrigation, drought
- profit - Income, schemes
- fertilizer - NPK, organic
- storage - Grain storage
- weather - Forecasting
- technology - Modern tools

## How Agent Uses Database

1. User asks question
2. Database searches for similar questions (semantic search)
3. If relevance > 30%, adds knowledge to context
4. AI formats the answer naturally
5. User gets accurate offline knowledge + AI formatting

## Benefits

✅ Works offline (after first setup)
✅ Fast responses
✅ Accurate farming knowledge
✅ Easy to add more data
✅ Semantic search (understands meaning)

## PythonAnywhere Deployment

1. Upload all files including `knowledge_base.py` and `db_manager.py`
2. Install: `pip install chromadb==0.4.22`
3. Database auto-creates on first run
4. `chroma_db/` folder stores data

## Future Improvements

- Add images/videos
- Multi-language knowledge
- User feedback to improve answers
- Export/import knowledge
- Admin panel to manage database
