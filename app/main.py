from fastapi import FastAPI
from app.api.routes import books
from app.api.routes import author

app = FastAPI(title="Library Management System")

app.include_router(books.router, prefix="/api/routes/books", tags=["Books"])
app.include_router(author.router, prefix="/api/routes/authors", tags=["Authors"])

@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}