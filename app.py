from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/home/")
def home(skip: int = 0, limit: int = 10):
    return skip, limit