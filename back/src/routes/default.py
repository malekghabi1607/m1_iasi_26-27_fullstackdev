from fastapi import FastAPI

app = FastAPI()

class DefaultRoute:

	@app.get("/")
	def read_root():
		return {"Hello World"}

