from db import connect_db
from auth import login, register
from applications import add_application
from analytics import apps_per_company
from companies import list_companies
from utils import hr

def main():
    conn = connect_db()

    user = None
    while not user:
        user = login(conn)

    while True:
        hr()
        print("1. Add Application")
        print("2. View Companies")
        print("3. Analytics")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_application(conn, user)
        elif choice == "2":
            list_companies(conn)
        elif choice == "3":
            apps_per_company(conn)
        elif choice == "0":
            break

    conn.close()

if __name__ == "__main__":
    main()
