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

    retries = state.get("search_retries",0 )  #default to 0, if no retries yet

    if retries >=3:
        print("🚨 MAX RETRIES REACHED. Forcing progression to avoid infinite loop.")
        return {"eval_passed": True, "search_retries": retries + 1}
    
    print(model , f"is ⚖️ Evaluating scraped results (Attempt {retries + 1}/3)...")
    
    # passing context -dict comprehension
    context = f"User query : {state['query']}\nFound: { [r['title'] for r in state['search_results']]}"

    res = evaluator_llm.invoke(context)

    print(f" > Decision :{res.enough}")
    print(f" > Reason: {res.reason}")

    # retry - LOOP if agent disapproves

    return {
        "eval_passed": res.enough,
        "query": res.suggested_query if not res.enough else state["query"],
        "search_retries":retries+1  #counter
    }