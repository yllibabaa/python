from fastapi import FastAPI


app = FastAPI()

@app.get("/")

def root():
    return {"message": "Hello, World!"}

@app.get("/greet")

def read_root(name: str):
    return{"message": "f'Hello,{name}!'"}