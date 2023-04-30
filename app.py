from flask import Flask, render_template, request, redirect, url_for, session, send_file
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
app.config['CV'] = 'static/CV'
app.config['Docs'] = 'static/Docs'


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


def insert_tutor(fname, lname, email, password, age, gender, contact, image, languages, newsubjects, bio, education,
                 years_of_experience, location, availability, minprice, maxprice, deliverymethod, avgrating, cvname,
                 docs):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    subjects_str = ', '.join(newsubjects)
    cur.execute(
        "INSERT INTO USER (username, password, picture, fullname, age, gender, languages, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages, contact)
    )
    cur.execute(
        "INSERT INTO TUTOR (username, password, picture, fullname, age, gender, languages, contact, bio, education, yearsofexperience, location, subjects, availability, minprice, maxprice, deliverymethod, avgrating, cv, docs, useruser, userpass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            email, password, image, fullname, age, gender, languages, contact, bio, education, years_of_experience,
            location, subjects_str, availability, minprice, maxprice, deliverymethod, avgrating, cvname, docs, email,
            password)
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


def update_tutor(username, fname, lname, password, age, gender, contact, image, languages, bio, education,
                 yearsofexperience, location, interests_str, availability, minprice, maxprice, deliverymethod, cv,
                 docs):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    languages_str = ', '.join(languages)
    location_str = ', '.join(location)
    deliverymethod_str = ', '.join(deliverymethod)
    cur.execute(
        "UPDATE USER SET password = %s, picture = %s, fullname = %s, age = %s, gender = %s, languages = %s, contact = %s WHERE username = %s",
        (password, image, fullname, age, gender, languages_str, contact, username)
    )
    cur.execute(
        "UPDATE TUTOR SET password = %s, picture = %s, fullname = %s, age = %s, gender = %s, languages = %s, bio = %s, education = %s, yearsofexperience = %s, location = %s, subjects = %s, availability = %s, minprice = %s, maxprice = %s, deliverymethod = %s,  cv = %s, docs = %s WHERE useruser = %s AND userpass = %s",
        (password, image, fullname, age, gender, languages_str, bio, education, yearsofexperience, location_str,
         interests_str, availability, minprice, maxprice, deliverymethod_str, cv, docs, username, password)
    )
    conn.commit()
    cur.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    return render_template("home.html")


@app.route('/studentprofile.html')
def profile():
    username = session['username']

    student = get_student_instance(username)

    if student:
        return render_template('studentprofile.html', student=student)
    else:
        return "Error: student not found"


@app.route('/tutorsearch.html')
def tutorsearch():
    username = request.args.get('username')
    tutor = get_tutor_instance(username)

    if tutor:
        return render_template('tutorsearch.html', tutor=tutor)
    else:
        return "Error: tutor not found"


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
                return render_template('loggedintutor.html', tutor=get_tutor_instance(email))
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
        return render_template('loggedin.html', username=username)
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
        languages = ','.join(request.form.getlist('languages'))
        image = request.files['image']
        newinterest = request.form['newinterest']
        bio = request.form['bio']
        education = request.form['education']
        years_of_experience = request.form['yearsofexperience']
        location = ','.join(request.form.getlist('location'))
        availability = request.form['availability']
        delivery_method = ','.join(request.form.getlist('deliverymethod'))
        cv = request.files['cv']
        docs = request.files['docs']
        min_price = request.form['minprice']
        max_price = request.form['maxprice']
        avgrating = 0

        # Handle multiple interests
        if 'interests' in request.form:
            interests = request.form.getlist('interests')
            interests.append(newinterest)
            interests_str = ','.join(interests)
        else:
            interests_str = newinterest

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save cv file
        cvname = secure_filename(cv.filename)
        cv.save(os.path.join(app.config['CV'], cvname))

        # Save docs file
        docsname = secure_filename(docs.filename)
        docs.save(os.path.join(app.config['Docs'], docsname))

        # Insert data into database
        insert_tutor(fname, lname, email, password, age, gender, contact, filename, languages, bio, education,
                     years_of_experience, location, interests_str, availability, min_price, max_price, delivery_method,
                     avgrating, cvname, docsname)
        username = fname + ' ' + lname
        session['username'] = email
        return render_template('loggedintutor.html', tutor=get_tutor_instance(email), username=username)
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


@app.route('/edittutor.html', methods=['GET', 'POST'])
def edittutor_form():
    username = session['username']

    user = get_tutor_instance(username)

    if request.method == 'POST':
        fname = request.form.get('fname', '')
        lname = request.form.get('lname', '')
        password = request.form.get('password', '')
        gender = request.form.get('gender', '')
        age = request.form.get('age', '')
        contact = request.form.get('contact', '')
        languages = request.form.getlist('languages')
        bio = request.form.get('bio', '')
        newinterest = request.form.get('newinterest', '')
        education = request.form.get('education', '')
        yearsofexperience = request.form.get('yearsofexperience', '')
        location = request.form.getlist('location')
        availability = request.form.get('availability', '')
        minprice = request.form.get('minprice', '')
        maxprice = request.form.get('maxprice', '')
        deliverymethod = request.form.getlist('deliverymethod')
        image = request.files['image']
        cv = request.files['cv']
        docs = request.files['docs']

        if not image:
            image = user['picture']
        else:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = filename

        if not cv:
            cv = user['cv']
        else:
            filename = secure_filename(cv.filename)
            cv.save(os.path.join(app.config['CV'], filename))
            cv = filename

        if not docs:
            docs = user['docs']
        else:
            filename = secure_filename(docs.filename)
            docs.save(os.path.join(app.config['Docs'], filename))
            docs = filename

        # Handle multiple interests
        if 'interests' in request.form:
            interests = request.form.getlist('interests')
            interests.append(newinterest)
            interests_str = ','.join(interests)
        else:
            interests_str = newinterest

        user_exists = get_tutor_instance(username) is not None

        # Insert or update data into database
        if user_exists:
            update_tutor(username, fname, lname, password, age, gender, contact, image, languages, bio, education,
                         yearsofexperience, location, interests_str, availability, minprice, maxprice, deliverymethod,
                         cv, docs)
        else:
            insert_student(fname, lname, username, password, age, gender, contact, filename, languages, interests_str)

        user = get_tutor_instance(username)
        return render_template('tutorprofile.html', tutor=user)
    else:
        cursor = conn.cursor()
        # execute SQL query to select interests from the STUDENT table
        cursor.execute('SELECT subjects FROM TUTOR')
        # retrieve all the interests and store them in a list
        interests_list = [row[0] for row in cursor.fetchall() if row[0] is not None]
        # remove commas and create a set of unique interests
        all_interests = set(','.join(interests_list).split(','))
        cursor.close()
        return render_template('edittutor.html', tutor=user, all_interests=all_interests)


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


# Define route for search results page
@app.route('/results.html', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # Get search query from form
        query = request.form['query']

        location1 = request.form.getlist('location1')
        location2 = request.form.getlist('location2')
        location3 = request.form.getlist('location3')
        location4 = request.form.getlist('location4')
        location5 = request.form.getlist('location5')

        location = [loc for loc in [location1, location2, location3, location4, location5] if loc != []]
        min_price = request.form.get('minPrice')
        max_price = request.form.get('maxPrice')
        min_age = request.form.get('minAge')
        max_age = request.form.get('maxAge')

        # age_range = request.args.get('age_range')

        if ((not location) and (not min_price) and (not max_price)):
            print("1")
            # Perform search in database with location filter
            cur = conn.cursor()
            cur.execute(
                "SELECT fullname, bio, subjects, picture, username FROM tutor WHERE (fullname LIKE %s OR bio LIKE %s OR subjects LIKE %s)",
                ('%' + query + '%', '%' + query + '%', '%' + query + '%')
            )
            results = cur.fetchall()
            cur.close()

            # Render search results template with results
            return render_template('results.html', results=results)

        elif ((min_price is not None) and (max_price is not None) and (min_age is not None) and (
                max_age is not None) and (not location)):
            print("2")

            cur = conn.cursor()
            cur.execute(
                "SELECT fullname, bio, subjects, picture , username FROM tutor WHERE ((fullname LIKE %s OR bio LIKE %s OR subjects LIKE %s) AND minprice >= %s AND maxprice <= %s AND age >= %s AND age <= %s)",
                ('%' + query + '%', '%' + query + '%', '%' + query + '%', min_price, max_price, min_age, max_age)
            )

            results = cur.fetchall()

            cur.close()
            return render_template('results.html', results=results)

        else:
            print("3")
            cur = conn.cursor()
            cur.execute(
                "SELECT fullname, bio, subjects, picture , username FROM tutor WHERE (fullname LIKE %s OR bio LIKE %s OR subjects LIKE %s) AND (minprice >= %s AND maxprice <= %s) AND location IN ({})".format(
                    ','.join(['%s' for _ in range(len(location))])),
                ('%' + query + '%', '%' + query + '%', '%' + query + '%', min_price, max_price) + tuple(
                    [x[0] for x in location])
            )

            results = cur.fetchall()
            cur.close()
            # Render search results template with results
            return render_template('results.html', results=results)
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


@app.route('/download-cv/<cv_name>')
def download_cv(cv_name):
    # Construct the file path
    file_path = os.path.join(app.config['CV'], cv_name)

    # Return the file to the user for download
    return send_file(file_path, as_attachment=True)


@app.route('/download-doc/<doc_name>')
def download_doc(doc_name):
    # Construct the file path
    file_path = os.path.join(app.config['Docs'], doc_name)

    # Return the file to the user for download
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run()
