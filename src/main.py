from db import connect_db
from utils import hr
from auth import auth_menu
from applications import (
    add_application,
    view_applications,
    update_status,
    delete_application,
)
from analytics import (
    days_waiting_menu,
    apps_per_company,
    get_status_by_id,
)
from companies import (
    list_companies,
    add_company,
)


def main_menu(conn, user):
    while True:
        hr("═")
        print(f"  JOB TRACKER  ·  {user['first_name']} {user['last_name']}")
        hr("═")
        print("  ── Applications ──────────────────────────────────")
        print("  [1] View my applications           (Query 4 – Procedure)")
        print("  [2] Add new application            (Query 1 – INSERT)")
        print("  [3] Update application status")
        print("  [4] Delete application")
        print()
        print("  ── Analytics ─────────────────────────────────────")
        print("  [5] Days waiting per interview     (Query 2 – DATEDIFF)")
        print("  [6] Applications per company       (Query 3 – COUNT/GROUP BY)")
        print("  [7] Check status by application ID (Query 5 – Function)")
        print()
        print("  ── Companies ─────────────────────────────────────")
        print("  [8] List all companies")
        print("  [9] Add company")
        print()
        print("  [0] Logout")
        hr()

        choice = input("  Choose: ").strip()

        if choice == "1":
            view_applications(conn, user)
        elif choice == "2":
            add_application(conn, user)
        elif choice == "3":
            update_status(conn, user)
        elif choice == "4":
            delete_application(conn, user)
        elif choice == "5":
            days_waiting_menu(conn, user)
        elif choice == "6":
            apps_per_company(conn)
        elif choice == "7":
            get_status_by_id(conn, user)
        elif choice == "8":
            list_companies(conn)
        elif choice == "9":
            add_company(conn)
        elif choice == "0":
            print(f"\n  Logged out. Goodbye, {user['first_name']}!\n")
            break
        else:
            print("  ✗ Invalid choice.\n")


def main():
    print("\n  Connecting to database...")
    conn = connect_db()
    print("  ✓ Connected.\n")

    try:
        while True:
            user = auth_menu(conn)
            main_menu(conn, user)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
