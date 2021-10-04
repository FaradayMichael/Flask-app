from app import app, db
from app.models import Users, Orders, Book, Author


@app.shell_context_processor
def msc():
    return dict(db=db, Author=Author, Book=Book, Users=Users, Orders=Orders)
