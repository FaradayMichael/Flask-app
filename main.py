from app import db
from app.models import Users, Author, Book

if __name__ == "__main__":
    # u = Users(username="qwe1", adm=True)
    # u.set_password("qwe1")
    a = Author(author_name="Dumas")
    b = Book(book_name="Tri", year=1856, author=a)

    db.session.add(a)
    db.session.add(b)
    db.session.commit()
