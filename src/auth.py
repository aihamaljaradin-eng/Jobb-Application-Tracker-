src/auth.py
import getpass
import mysql.connector
from utils import hr


def login(conn):
    cursor = conn.cursor(dictionary=True)
    hr()
    print("  LOGIN")
    hr()

    email = input("  Email:    ").strip()
    password = getpass.getpass("  Password: ")

    cursor.execute(
        "SELECT user_id, first_name, last_name FROM p_User WHERE gmail=%s AND p_password=%s",
        (email, password)
    )
    row = cursor.fetchone()
    cursor.close()

    if row:
        print(f"\n  ✓ Welcome back, {row['first_name']} {row['last_name']}!")
        return row

    print("  ✗ Invalid email or password.")
    return None


def register(conn):
    cursor = conn.cursor()
    hr()
    print("  REGISTER")
    hr()

    first = input("  First name: ").strip()
    last = input("  Last name:  ").strip()
    email = input("  Email:      ").strip()
    password = getpass.getpass("  Password:   ")

    try:
        cursor.execute(
            """
            INSERT INTO p_User (first_name, last_name, gmail, p_password)
            VALUES (%s, %s, %s, %s)
            """,
            (first, last, email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        print(f"\n  ✓ Account created! Your user ID is {user_id}.")
        return {"user_id": user_id, "first_name": first, "last_name": last}

    except mysql.connector.Error as e:
        print(f"  ✗ Registration failed: {e}")
        return None

    finally:
        cursor.close()


def auth_menu(conn):
    while True:
        hr("═")
        print("  JOB APPLICATION TRACKER")
        hr("═")
        print("  [1] Login")
        print("  [2] Register")
        print("  [0] Exit")
        hr()

        choice = input("  Choose: ").strip()

        if choice == "1":
            user = login(conn)
            if user:
                return user

        elif choice == "2":
            user = register(conn)
            if user:
                return user

        elif choice == "0":
            print("\n  Goodbye!\n")
            raise SystemExit(0)

        else:
            print("  ✗ Invalid choice.\n")
