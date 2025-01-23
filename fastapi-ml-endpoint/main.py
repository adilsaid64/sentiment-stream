from fastapi import FastAPI
from typing import Dict
import random

app = FastAPI()

@app.get("/sentiment")
def get_sentiment(text: str) -> Dict[str, float]:
    """Returns a mock sentiment score between -1 and 1 for a given text."""
    return {"sentiment": random.uniform(-1, 1)}
