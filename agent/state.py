from typing import Annotated 
import operator
from typing_extensions import TypedDict

class ShoppingState(TypedDict):
    query: str
    search_results: list[dict]
    eval_passed: bool   # check - did the llm approve results ?
    search_retries: int  # if not retry , - count retries max 
    urls_to_scrape: list[str]
#     scraped_data: Annoted[list[dict]]
#     final_report: str

class WorkerState(TypedDict):
    url: str
#     scraped_data: Annoted[list[dict], operator.add]

