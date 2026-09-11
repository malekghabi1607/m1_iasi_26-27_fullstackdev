from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello_world() -> str:
    """Return a greeting from the API."""
    return "Hello World"
