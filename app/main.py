from fastapi import FastAPI
from app.api.routes import books
from app.api.routes import author
from app.api.routes import root

app = FastAPI(title="Library Management System")

app.include_router(books.router, prefix="/api/routes/books", tags=["Books"])
app.include_router(author.router, prefix="/api/routes/authors", tags=["Authors"])
app.include_router(root.router)
