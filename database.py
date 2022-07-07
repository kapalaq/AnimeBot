import psycopg2
from psycopg2 import Error


class Database:

    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                      password="2444666668888888",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres_db")
        self.cursor = self.connection.cursor()
        self.name = "anime_search"

    def __getitem__(self, value):
        try:
            get_query = f"SELECT * from {self.name}"
            self.cursor.execute(get_query)
            urls = self.cursor.fetchall()
            for i in urls:
                if int(i[0]) == value:
                    return i[1]

        except (Exception, Error) as error:
            print("Something goes wrong4:", error)

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()

        except (Exception, Error) as error:
            print("Something goes wrong5:", error)

    def insert(self, value):
        try:
            number, url = value
            get_query = f"SELECT * from {self.name}"
            self.cursor.execute(get_query)
            urls = self.cursor.fetchall()
            if list(filter(lambda x: x[0] == number, urls)):
                insert_query = f"""Update {self.name} set url = '{url}' where id = {number}"""
            else:
                insert_query = f"""INSERT INTO {self.name} (ID, URL) VALUES ({number}, '{url}')"""
            self.cursor.execute(insert_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Something goes wrong2:", error)

    def delete(self, n):
        try:
            delete_query = f"""Delete from {self.name} where id = {n}"""
            self.cursor.execute(delete_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Something goes wrong3:", error)
