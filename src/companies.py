from utils import hr, pause

def list_companies(conn):
    cursor = conn.cursor()
    hr()
    print("COMPANIES")
    hr()

    cursor.execute("SELECT * FROM Company")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    pause()
