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
    password=""
)

app.config['UPLOAD_FOLDER'] = 'static/UPLOAD_FOLDER'

# Define a function to insert a new student record into the database
def insert_student(fname, lname, email, password, age, gender, contact, image, languages):
    cur = conn.cursor()
    fullname = f"{fname} {lname}"
    languages_str = ', '.join(languages) 
    cur.execute(
        "INSERT INTO USER (username, password, picture, fullname, age, gender, languages, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages_str, contact)
    )
    cur.execute(
        "INSERT INTO STUDENT (username, password, picture, fullname, age, gender, languages, contact, useruser, userpass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (email, password, image, fullname, age, gender, languages_str, contact, email, password)
    )
    conn.commit()
    cur.close()



def insert_tutor(fname, lname, email, password, city, country):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tutor (first_name, last_name, email, password, city, country) VALUES (%s, %s, %s, %s, %s, %s)",
        (fname, lname, email, password, city, country)
    )
    conn.commit()
    cur.close()




@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


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

        # Save image file
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert data into database
        insert_student(fname, lname, email, password, age, gender, contact, filename, languages)
        return render_template('loggedin.html')
    else:
        return render_template('signup.html')



@app.route('/becomeatutor.html', methods=['GET', 'POST'])
def signup_form2():
    if request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        country = request.form['country']
       # user = request.form['user']
        # Insert data into database
        insert_tutor(fname, lname, email, password, city, country)
        return render_template('home.html')
    else:
        return render_template('becomeatutor.html')




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