from app import db
from app.models import Users, Author, Book, Orders

if __name__ == "__main__":
    # u = Users(username="qwe1", adm=True)
    # u.set_password("qwe1")
    # a = Author(author_name="Dumas")
    # b = Book(book_name="Tri", year=1856, author=a)
    u = Users.query.filter_by(username="qwe1").first()
    b = Book.query.filter_by(book_name="Tri mushketera").first()
    if u and b:
        o = Orders(book=b, price=5, user=u)
        db.session.add(o)
        db.session.commit()

