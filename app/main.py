from fastapi import FastAPI
from app.api.routes import books

app = FastAPI(title="Library Management System")

app.include_router(books.router, prefix="/api/routes/books", tags=["Books"])

@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}