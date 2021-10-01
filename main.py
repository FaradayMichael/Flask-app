from app import db
from app.entities import Users

if __name__ == "__main__":
    u = Users(username="qwe1", adm=True)
    u.set_password("qwe1")
    db.session.add(u)
    db.session.commit()