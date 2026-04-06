from utils import hr, pause

def apps_per_company(conn):
    cursor = conn.cursor()
    hr()
    print("APPLICATIONS PER COMPANY")
    hr()

    cursor.execute("""
        SELECT Company.company_name,
               COUNT(JobApplication.application_id)
        FROM JobApplication
        JOIN Company ON JobApplication.company_id = Company.company_id
        GROUP BY Company.company_name
    """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    pause()
