from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from state import ShoppingState

load_dotenv()
model="gpt-4o"
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class EvalResult(BaseModel):
    enough: bool = Field(description="True if results cover at least 3 distinct products with prices.")
    reason: str = Field(description="Why the current results are or aren't sufficient.")
    suggested_query: str = Field(description="If enough=False, provide a better search query to find more data.")

# evaluator - with pydantic
evaluator_llm = llm.with_structured_output(EvalResult)

def eval_node(state:ShoppingState):
    if state.get("search_retries", 0) >=3:
        return { "eval_passed":True}
    
    print(model, " is evaluating the loot (scraped data )...")
    
    # passing context
    context = f"User query : {state['query']}\nFound: { [r['title'] for r in state['search_results']]}"

    res = evaluator_llm.invoke(context)

    print(f" >sufficieny:{res.enough}")
    print(f"  > Reason: {res.reason}")

    # retry - LOOP if agent disapproves

    return {
        "eval_passed": res.enough,
        "query": res.suggested_query if not res.enough else state["query"]
    }