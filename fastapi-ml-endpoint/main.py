from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/sentiment")
def get_sentiment(text: str):
    """Mock sentiment analysis by returning a random score between -1 and 1."""
    return {"sentiment": random.uniform(-1, 1)}
