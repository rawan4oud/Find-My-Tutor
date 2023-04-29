from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.utils import secure_filename
from controller import *
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define database connection parameters
conn = mysql.connector.connect(
    host="localhost",
    database="newdb",
    user="root",
    password=""
)

app.config['UPLOAD_FOLDER'] = 'static/UPLOAD_FOLDER'


# Define a function to insert a new student record into the database
def insert_student(fname, lname, email, password, age, gender, contact, image, languages, newinterest):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    languages_str = ', '.join(languages)
    cur.execute(
        "INSERT INTO USER (username, password, picture, fullname, age, gender, languages, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages_str, contact)
    )
    cur.execute(
        "INSERT INTO STUDENT (username, password, picture, fullname, age, gender, languages, interests, contact, useruser, userpass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages_str, newinterest, contact, email, password)
    )
    conn.commit()
    cur.close()


def insert_tutor(fname, lname, email, password, age, gender, contact, image, languages, newinterest):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    languages_str = ', '.join(languages)
    cur.execute(
        "INSERT INTO USER (username, password, picture, fullname, age, gender, languages, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages_str, contact)
    )
    cur.execute(
        "INSERT INTO TUTOR (username, password, picture, fullname, age, gender, subjects, contact, useruser, userpass, bio, education, yearsofexperience, location, availability, pricerange, deliverymethod, avgrating, cv, docs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            email, password, image, fullname, age, gender, newinterest, contact, email, password, "", "", 0, "", "", "",
            "",
            0.0, "", "")
    )
    conn.commit()
    cur.close()

def update_student(username, fname, lname, password, age, gender, contact, image, languages, newinterest):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    languages_str = ', '.join(languages) 
    cur.execute(
        "UPDATE USER SET password = %s, picture = %s, fullname = %s, age = %s, gender = %s, languages = %s, contact = %s WHERE username = %s",
        (password, image, fullname, age, gender, languages_str, contact, username)
    )
    cur.execute(
        "UPDATE STUDENT SET password = %s, picture = %s, fullname = %s, age = %s, gender = %s, languages = %s, interests = %s, contact = %s WHERE useruser = %s AND userpass = %s",
        (password, image, fullname, age, gender, languages_str, newinterest, contact, username, password)
    )
    conn.commit()
    cur.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/studentprofile.html')
def profile():
    username = session['username']

    student = get_student_instance(username)

    if student:
        return render_template('studentprofile.html', student=student)
    else:
        return "Error: student not found"

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    conn = mysql.connector.connect(
        host="localhost",
        database="newdb",
        user="root",
        password=""
    )
    error = None
    fullname = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE username=%s AND password=%s", (email, password))
        user = c.fetchone()
        if user is None:
            error = 'Invalid username or password'
        else:
            fullname_query = "SELECT fullname FROM USER WHERE username=%s AND password=%s"
            c.execute(fullname_query, (email, password))
            fullname = c.fetchone()[0]
            tutor_query = "SELECT * FROM TUTOR WHERE username=%s AND password=%s"
            c.execute(tutor_query, (email, password))
            tutor = c.fetchone()
            if tutor is not None:
                session['username'] = email
                session['user_type'] = 'tutor'
                return redirect(url_for('loggedintutor'))
            else:
                session['username'] = email
                session['user_type'] = 'student'
                return render_template('loggedin.html', student=get_student_instance(email))
        conn.commit()
        conn.close()
    return render_template('login.html', error=error)


@app.route('/loggedin.html')
def loggedin():
    if 'username' in session and session['user_type'] == 'student':
        username = session['username']

        return render_template('loggedin.html', username=username, student=get_student_instance(username))
    else:
        return render_template('login.html')


@app.route('/loggedintutor.html')
def loggedintutor():
    if 'username' in session and session['user_type'] == 'tutor':
        username = session['username']
        return render_template('loggedintutor.html', username=username)
    else:
        return render_template('login.html')


# Define a route for the registration form

@app.route('/signup.html', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        age = request.form['age']
        contact = request.form['contact']
        languages = request.form.getlist('languages')
        image = request.files['image']

        # Handle multiple interests
        if 'interests' in request.form:
            interests = request.form.getlist('interests')
            interests_str = ','.join(interests)

        # Save image file
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert data into database
        insert_student(fname, lname, email, password, age, gender, contact, filename, languages, interests_str)
        username = fname + ' ' + lname
        session['username'] = email
        session['user_type']= 'student'
        return render_template('loggedin.html', student=get_student_instance(email), username=username)
    else:
        cursor = conn.cursor()
        # execute SQL query to select interests from the STUDENT table
        cursor.execute('SELECT subjects FROM TUTOR')
        # retrieve all the interests and store them in a list
        interests_list = [row[0] for row in cursor.fetchall() if row[0] is not None]
        # remove commas and create a set of unique interests
        interests = set(','.join(interests_list).split(','))
        return render_template('signup.html', interests=interests)


@app.route('/becomeatutor.html', methods=['GET', 'POST'])
def signup_form2():
    if request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        age = request.form['age']
        contact = request.form['contact']
        languages = request.form.getlist('languages')
        image = request.files['image']
        newinterest = request.form['newinterest']

        # Handle multiple interests
        if 'interests' in request.form:
            interests = request.form.getlist('interests')
            interests.append(newinterest)
            interests_str = ','.join(interests)
        else:
            interests_str = newinterest

        # Save image file
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert data into database
        insert_tutor(fname, lname, email, password, age, gender, contact, filename, languages, interests_str)
        username = fname + ' ' + lname
        return render_template('loggedintutor.html', username=username)
    else:
        cursor = conn.cursor()
        # execute SQL query to select interests from the STUDENT table
        cursor.execute('SELECT subjects FROM TUTOR')
        # retrieve all the interests and store them in a list
        interests_list = [row[0] for row in cursor.fetchall() if row[0] is not None]
        # remove commas and create a set of unique interests
        interests = set(','.join(interests_list).split(','))
        return render_template('becomeatutor.html', interests=interests)


@app.route('/editstudent.html', methods=['GET', 'POST'])
def editstudent_form():
    username = session['username']

    user = get_student_instance(username)

    if request.method == 'POST':
        fname = request.form.get('fname', '')
        lname = request.form.get('lname', '')
        password = request.form.get('password', '')
        gender = request.form.get('gender', '')
        age = request.form.get('age', '')
        contact = request.form.get('contact', '')
        languages = request.form.getlist('languages')
        image = request.files['image']

        if not image:
            image = user['picture']
        else:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = filename

        interests_str = ''
        if 'interests' in request.form:
            all_interests = request.form.getlist('interests')
            interests_str = ','.join(all_interests)

        user_exists = get_student_instance(username) is not None

        # Insert or update data into database
        if user_exists:
            update_student(username, fname, lname, password, age, gender, contact, image, languages,
                           interests_str)
        else:
            insert_student(fname, lname, username, password, age, gender, contact, filename, languages, interests_str)

        user = get_student_instance(username)
        return render_template('studentprofile.html', student=user)
    else:
        cursor = conn.cursor()
        # execute SQL query to select interests from the STUDENT table
        cursor.execute('SELECT subjects FROM TUTOR')
        # retrieve all the interests and store them in a list
        interests_list = [row[0] for row in cursor.fetchall() if row[0] is not None]
        # remove commas and create a set of unique interests
        all_interests = set(','.join(interests_list).split(','))
        cursor.close()
        return render_template('editstudent.html', student=user, all_interests=all_interests)


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


# Define route for search results page
@app.route('/results.html', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # Get search query from form
        query = request.form['query']

        # Perform search in database
        cur = conn.cursor()
        cur.execute(
            "SELECT fullname, bio FROM tutor WHERE fullname LIKE %s OR bio LIKE %s",
            ('%' + query + '%', '%' + query + '%')
        )
        results = cur.fetchall()
        cur.close()

        # Render search results template with results
        return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()
