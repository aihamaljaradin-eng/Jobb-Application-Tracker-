import mysql.connector
from utils import hr, prompt_int, pause


def get_days_waiting_for_each_job(cursor, user_id):
    try:
        cursor.execute(
            """
            SELECT p_User.first_name, p_User.last_name,
                   JobApplication.application_id,
                   DATEDIFF(JobApplication.interview_date, JobApplication.application_date)
                   AS days_waiting_for_interview
            FROM JobApplication
            JOIN p_User ON JobApplication.user_id = p_User.user_id
            WHERE JobApplication.interview_date IS NOT NULL
              AND JobApplication.user_id = %s
            ORDER BY JobApplication.application_date DESC
            """,
            (user_id,)
        )

        results = cursor.fetchall()

        if results:
            print(f"\n  {'App ID':<8} {'Days Waiting':<15} Name")
            hr()
            for row in results:
                print(f"  {row[2]:<8} {row[3]:<15} {row[0]} {row[1]}")
        else:
            print("  No applications with interview dates found.")

    except mysql.connector.Error as e:
        print(f"  ✗ Error executing query: {e}")


def days_waiting_menu(conn, user):
    cursor = conn.cursor()
    hr()
    print("  DAYS WAITING PER INTERVIEW")
    hr()

    get_days_waiting_for_each_job(cursor, user["user_id"])

    cursor.close()
    pause()


def apps_per_company(conn):
    cursor = conn.cursor()
    hr()
    print("  APPLICATIONS PER COMPANY (all users)")
    hr()

    try:
        cursor.execute(
            """
            SELECT Company.company_name,
                   COUNT(JobApplication.application_id) AS application_count
            FROM JobApplication
            JOIN Company ON JobApplication.company_id = Company.company_id
            GROUP BY Company.company_name
            ORDER BY application_count DESC
            """
        )
        rows = cursor.fetchall()

        if rows:
            print(f"\n  {'Company':<30} Applications")
            hr()
            for row in rows:
                print(f"  {row[0]:<30} {row[1]}")
        else:
            print("  No data found.")

    except mysql.connector.Error as e:
        print(f"  ✗ Error: {e}")

    finally:
        cursor.close()

    pause()


def get_status_by_id(conn, user):
    cursor = conn.cursor()
    hr()
    print("  CHECK STATUS BY APPLICATION ID")
    hr()

    cursor.execute(
        "SELECT application_id FROM JobApplication WHERE user_id = %s ORDER BY application_id",
        (user["user_id"],)
    )
    apps = cursor.fetchall()

    if apps:
        ids = ", ".join(str(a[0]) for a in apps)
        print(f"  Your application IDs: {ids}")

    app_id = prompt_int("Enter application ID")

    try:
        cursor.execute("SELECT GetApplicationStatus(%s)", (app_id,))
        row = cursor.fetchone()

        if row and row[0]:
            print(f"\n  Status: {row[0]}")
        else:
            print("  No status found for that application ID.")

    except mysql.connector.Error as e:
        print(f"  ✗ Error calling function: {e}")

    finally:
        cursor.close()

    pause()
