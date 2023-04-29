import mysql.connector

def get_student_instance(username: str):
    with mysql.connector.connect(
        host="localhost",
        database="newdb",
        user="root",
        password=""
    ) as conn:

        cursor = conn.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM STUDENT WHERE username = '{username}'")

        user = cursor.fetchone()

    return user