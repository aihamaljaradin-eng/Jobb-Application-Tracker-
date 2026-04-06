import mysql.connector
from utils import hr, prompt_int, prompt_date, pause

DEFAULT_STATUS_ID = 1


def add_application(conn, user):
    cursor = conn.cursor(dictionary=True)
    hr()
    print("  ADD NEW APPLICATION")
    hr()

    cursor.execute("SELECT company_id, company_name, industry FROM Company ORDER BY company_name")
    companies = cursor.fetchall()

    print("\n  Companies:")
    for c in companies:
        print(f"    [{c['company_id']}] {c['company_name']} — {c['industry'] or '—'}")

    company_id = prompt_int("Enter company ID")

    cursor.execute("SELECT company_id FROM Company WHERE company_id = %s", (company_id,))
    if not cursor.fetchone():
        print("  ✗ Invalid company ID.")
        cursor.close()
        pause()
        return

    cursor.execute("SELECT status_id, status_name FROM Status ORDER BY status_id")
    statuses = cursor.fetchall()

    print(f"\n  Status (default: [{DEFAULT_STATUS_ID}] Pending):")
    for s in statuses:
        print(f"    [{s['status_id']}] {s['status_name']}")

    status_input = input("  Enter status ID [Enter for Pending]: ").strip()
    status_id = int(status_input) if status_input else DEFAULT_STATUS_ID

    contact_person = input("  Contact person   [Enter to skip]: ").strip() or None
    contact_email = input("  Contact email    [Enter to skip]: ").strip() or None
    application_date = prompt_date("Application date")
    interview_date = prompt_date("Interview date", required=False)
    deadline = prompt_date("Deadline", required=False)
    notes = input("  Notes            [Enter to skip]: ").strip() or None

    try:
        cursor.execute(
            """
            INSERT INTO JobApplication
                (contact_person, contact_email, interview_date,
                 application_date, notes, deadline,
                 user_id, status_id, company_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                contact_person, contact_email, interview_date,
                application_date, notes, deadline,
                user["user_id"], status_id, company_id
            )
        )
        conn.commit()
        print(f"\n  ✓ Application added (ID: {cursor.lastrowid}).")

    except mysql.connector.Error as e:
        print(f"  ✗ Error inserting application: {e}")

    finally:
        cursor.close()

    pause()


def view_applications(conn, user):
    cursor = conn.cursor(dictionary=True)
    hr()
    print("  MY APPLICATIONS")
    hr()

    try:
        cursor.callproc("GetUserApplications", [user["user_id"]])
        rows = []

        for result in cursor.stored_results():
            rows = result.fetchall()

        if not rows:
            print("  No applications found.")
        else:
            print(f"\n  {'ID':<5} {'Company':<20} {'Status':<12} {'Applied':<13} {'Interview':<13} {'Deadline'}")
            hr()
            for r in rows:
                print(
                    f"  {r['application_id']:<5} "
                    f"{r['company_name']:<20} "
                    f"{(r['status_name'] or '—'):<12} "
                    f"{str(r['application_date']):<13} "
                    f"{(str(r['interview_date']) if r['interview_date'] else '—'):<13} "
                    f"{str(r['deadline']) if r['deadline'] else '—'}"
                )

    except mysql.connector.Error as e:
        print(f"  ✗ Error calling procedure: {e}")

    finally:
        cursor.close()

    pause()


def update_status(conn, user):
    cursor = conn.cursor(dictionary=True)
    hr()
    print("  UPDATE APPLICATION STATUS")
    hr()

    cursor.execute(
        """
        SELECT ja.application_id, c.company_name, s.status_name
        FROM JobApplication ja
        JOIN Company c ON ja.company_id = c.company_id
        LEFT JOIN Status s ON ja.status_id = s.status_id
        WHERE ja.user_id = %s
        ORDER BY ja.application_date DESC
        """,
        (user["user_id"],)
    )
    apps = cursor.fetchall()

    if not apps:
        print("  No applications to update.")
        cursor.close()
        pause()
        return

    for a in apps:
        print(f"  [{a['application_id']}] {a['company_name']} — {a['status_name'] or '—'}")

    app_id = prompt_int("Enter application ID to update")

    cursor.execute(
        "SELECT application_id FROM JobApplication WHERE application_id=%s AND user_id=%s",
        (app_id, user["user_id"])
    )
    if not cursor.fetchone():
        print("  ✗ Application not found or does not belong to you.")
        cursor.close()
        pause()
        return

    cursor.execute("SELECT status_id, status_name FROM Status ORDER BY status_id")
    statuses = cursor.fetchall()

    print("\n  Available statuses:")
    for s in statuses:
        print(f"    [{s['status_id']}] {s['status_name']}")

    new_status = prompt_int("New status ID")

    try:
        cursor.execute(
            "UPDATE JobApplication SET status_id=%s WHERE application_id=%s",
            (new_status, app_id)
        )
        conn.commit()
        print("  ✓ Status updated successfully.")

    except mysql.connector.Error as e:
        print(f"  ✗ Error updating status: {e}")

    finally:
        cursor.close()

    pause()


def delete_application(conn, user):
    cursor = conn.cursor(dictionary=True)
    hr()
    print("  DELETE APPLICATION")
    hr()

    cursor.execute(
        """
        SELECT ja.application_id, c.company_name, ja.application_date
        FROM JobApplication ja
        JOIN Company c ON ja.company_id = c.company_id
        WHERE ja.user_id = %s
        ORDER BY ja.application_date DESC
        """,
        (user["user_id"],)
    )
    apps = cursor.fetchall()

    if not apps:
        print("  No applications found.")
        cursor.close()
        pause()
        return

    for a in apps:
        print(f"  [{a['application_id']}] {a['company_name']} — Applied: {a['application_date']}")

    app_id = prompt_int("Enter application ID to delete")
    confirm = input(f"  Confirm delete application {app_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("  Cancelled.")
        cursor.close()
        pause()
        return

    try:
        cursor.execute(
            "DELETE FROM JobApplication WHERE application_id=%s AND user_id=%s",
            (app_id, user["user_id"])
        )
        conn.commit()

        if cursor.rowcount:
            print(f"  ✓ Application {app_id} deleted.")
        else:
            print("  ✗ Application not found or does not belong to you.")

    except mysql.connector.Error as e:
        print(f"  ✗ Error: {e}")

    finally:
        cursor.close()

    pause()
