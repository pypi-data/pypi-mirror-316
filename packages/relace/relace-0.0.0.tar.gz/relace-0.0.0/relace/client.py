from fastapi import FastAPI
from pydantic import BaseModel


class HelloResponse(BaseModel):
    message: str


app = FastAPI(
    title="Relace",
    description="End-to-end fine tuning and inference for open source LLMs",
    version="0.0.0",
)


@app.get("/", response_model=HelloResponse)
async def read_root():
    """
    Return a friendly hello message.
    """
    return {"message": "Hello World"}
