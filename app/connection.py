import psycopg2


class Connection(object):

    def __init__(self):
        self.con = psycopg2.connect(user="postgres",
                                    password="root",
                                    host="localhost",
                                    port="5432",
                                    database="flaskapp")

    def find_user(self, username, password):
        cur = self.con.cursor()
        cur.execute(f"select * from public.users " +
                    f"where username='{username}' and pass='{password}'")
        return cur.fetchall()
