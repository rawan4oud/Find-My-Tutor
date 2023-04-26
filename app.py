from flask import Flask, request, render_template
import mysql.connector
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


# Define database connection parameters
conn = mysql.connector.connect(
    host="localhost",
    database="fmt",
    user="root",
    password="root"
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
        email, password, image, fullname, age, gender, newinterest, contact, email, password, "", "", 0, "", "", "", "",
        0.0, "", "")
    )
    conn.commit()
    cur.close()




@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/loggedin.html', methods=['GET', 'POST'])
def signout():
    return render_template("home.html")

@app.route('/loggedintutor.html', methods=['GET', 'POST'])
def signouttutor():
    return render_template("home.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    fullname = None
    conn = mysql.connector.connect(
        host="localhost",
        database="fmt",
        user="root",
        password="root"
    )
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
                return render_template('loggedintutor.html', username=fullname)
            else:
                return render_template('loggedin.html', username=fullname)
        conn.commit()
        conn.close()
    return render_template('login.html', error=error)


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
        return render_template('loggedin.html', username=username)
    else:  
        cursor = conn.cursor()
       # execute SQL query to select interests from the STUDENT table
        cursor.execute('SELECT subjects FROM TUTOR')
        # retrieve all the interests and store them in a list
        interests_list = [row[0] for row in cursor.fetchall() if row[0] is not None]
        # remove commas and create a set of unique interests
        interests = set(','.join(interests_list).split(','))
        return render_template('signup.html',interests=interests)



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
        insert_tutor(fname, lname, email, password, age, gender, contact, filename, languages,interests_str)
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
        return render_template('becomeatutor.html',interests=interests)





@app.route('/search.html', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

# Define route for search results page
@app.route('/results.html', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        #Get search query from form
        query = request.form['query']

        # Perform search in database
        cur = conn.cursor()
        cur.execute(
            "SELECT first_name, bio FROM tutor WHERE first_name LIKE %s OR bio LIKE %s",
            ('%' + query + '%', '%' + query + '%')
        )
        results = cur.fetchall()
        cur.close()

        # Render search results template with results
        return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()