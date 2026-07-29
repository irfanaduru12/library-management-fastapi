from fastapi import FastAPI
from app.api.routes import books, author, root, auth, user

app = FastAPI(title="Library Management System")

app.include_router(books.router)
app.include_router(author.router)
app.include_router(root.router)
app.include_router(auth.router)
app.include_router(user.router)