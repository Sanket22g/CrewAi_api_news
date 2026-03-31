from fastapi import FastAPI
from myagent_news_api.crew import MyagentNewsApi 
from datetime import datetime, timedelta, timezone

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MyagentNewsApi! Use the /run-crew endpoint to execute the crew."}

@app.post("/run-crew")
async def run_crew():
    """
    Endpoint to run the crew.

    """
    inputs = {
        "topic": "LLM, Agentic AI, AI Updates, AI Tools, Machine Learning",
        "current_year": str(datetime.now().year),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "two_days_ago": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    }
    try:
        result=MyagentNewsApi().crew().kickoff(inputs=inputs)
        
        return { "result": result.pydantic.model_dump() 
        }
    except Exception as e:
        return {"error": f"An error occurred while running the crew: {e}"}
    

