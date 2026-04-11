# agent/database.py
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    """
    Handles directory creation and returns a  LangGraph checkpointer.
    """
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(current_dir, "data")
    db_path = os.path.join(db_dir, "shopping_researcher.db")

    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    
    # check_same_thread= False allows multiple agent workers to write safely
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    return SqliteSaver(conn)