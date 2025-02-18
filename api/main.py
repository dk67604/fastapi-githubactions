from fastapi import FastAPI
from mangum import Mangum # Wrapper for AWS Lambda to run FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

handler = Mangum(app)