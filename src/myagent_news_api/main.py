#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv

load_dotenv()

from datetime import datetime, timedelta

from myagent_news_api.crew import MyagentNewsApi    

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'LLM, Agentic AI, AI Updates, AI Tools, Machine Learning',
        'current_year': str(datetime.now().year),
        'date': datetime.now().strftime("%Y-%m-%d"),
        'two_days_ago': (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    }

    try:
        MyagentNewsApi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
if __name__ == "__main__":
    run()