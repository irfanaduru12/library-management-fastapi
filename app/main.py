from fastapi import FastAPI
from app.api.routes import books
from app.api.routes import author
from app.api.routes import root
from app.api.routes import auth

app = FastAPI(title="Library Management System")

app.include_router(books.router)
app.include_router(author.router)
app.include_router(root.router)
app.include_router(auth.router)