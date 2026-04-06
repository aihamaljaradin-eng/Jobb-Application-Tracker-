import mysql.connector
from utils import hr, pause


def list_companies(conn):
    cursor = conn.cursor()
    hr()
    print("  ALL COMPANIES")
    hr()

    cursor.execute(
        "SELECT company_id, company_name, industry, website FROM Company ORDER BY company_name"
    )
    rows = cursor.fetchall()

    if rows:
        print(f"\n  {'ID':<5} {'Name':<25} {'Industry':<20} Website")
        hr()
        for row in rows:
            print(f"  {row[0]:<5} {row[1]:<25} {(row[2] or '—'):<20} {row[3] or '—'}")
    else:
        print("  No companies found.")

    cursor.close()
    pause()


def add_company(conn):
    cursor = conn.cursor()
    hr()
    print("  ADD COMPANY")
    hr()

    name = input("  Company name:            ").strip()
    industry = input("  Industry [Enter to skip]: ").strip() or None
    website = input("  Website  [Enter to skip]: ").strip() or None

    try:
        cursor.execute(
            "INSERT INTO Company (company_name, industry, website) VALUES (%s, %s, %s)",
            (name, industry, website)
        )
        conn.commit()
        print(f"  ✓ Company added (ID: {cursor.lastrowid}).")

    except mysql.connector.Error as e:
        print(f"  ✗ Error: {e}")

    finally:
        cursor.close()

    pause()
