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


def get_tutor_instance(username: str):
    with mysql.connector.connect(
            host="localhost",
            database="newdb",
            user="root",
            password=""
    ) as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM TUTOR WHERE username = '{username}'")

        user = cursor.fetchone()

    return user


def get_course(username: str):
    with mysql.connector.connect(
            host="localhost",
            database="newdb",
            user="root",
            password=""
    ) as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM learning WHERE studuser = '{username}'")
        results = cursor.fetchall()

    return results


def get_course2(username: str):
    with mysql.connector.connect(
            host="localhost",
            database="newdb",
            user="root",
            password=""
    ) as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM learning WHERE tutuser = '{username}'")
        results = cursor.fetchall()

    return results
