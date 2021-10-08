from app import db
from app.models import Users, Author, Book, Orders
from sqlalchemy import exc


def insert_test_users():
    u1 = Users(username="qwe1", adm=True)
    u1.set_password("qwe1")
    u2 = Users(username="qwe2", adm=False)
    u2.set_password("qwe2")
    try:
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()

def insert_test_books():
    b = Book(book_name="Tri", year=1555, author=Author("Dumas"))
    try:
        db.session.add(b)
        db.session.commit()
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()


def create_test_orders():
    u1, u2 = select_test_users()
    b = Book.query.filter(Book.book_name=="Tri").first()
    o1 = Orders(book=b, price=5, user=u1)
    o2 = Orders(book=b, price=5, user=u2)
    try:
        db.session.add(o1)
        db.session.add(o2)
        db.session.commit()
    except BaseException as e:
        print(e)
        db.session.rollback()


def select_test_users():
    return Users.query.filter(Users.username.in_(["qwe1", "qwe2"])).all()

if __name__ == "__main__":
    create_test_orders()
